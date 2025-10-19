"""Pydantic models for rclone-adapter."""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

from rclone.util import find_rclone_binary


class RCloneConfig(BaseModel):
    """Configuration for RClone client with validation."""

    config_file: Path | None = None
    env_vars: dict[str, str] = Field(default_factory=dict)
    rclone_path: str = "rclone"
    log_level: str = "INFO"
    default_flags: list[str] = Field(default_factory=list)

    @field_validator("rclone_path", mode="before")
    @classmethod
    def resolve_rclone_path(cls, v: str | None) -> str:
        """Resolve rclone executable, using bundled version if available."""
        if v is None or v == "rclone":
            # Use find_rclone_binary to prefer bundled version
            try:
                return find_rclone_binary()
            except FileNotFoundError:
                # Fall back to "rclone" if bundled not found
                return "rclone"

        # Use provided path, validate it exists
        if not shutil.which(v):
            msg = f"rclone not found at: {v}"
            raise ValueError(msg)
        return v

    @field_validator("config_file")
    @classmethod
    def validate_config_file(cls, v: Path | None) -> Path | None:
        """Validate config file exists and is readable."""
        if v and not v.exists():
            msg = f"Config file not found: {v}"
            raise ValueError(msg)
        if v and not v.is_file():
            msg = f"Config path is not a file: {v}"
            raise ValueError(msg)
        return v

    @field_validator("env_vars")
    @classmethod
    def validate_env_vars(cls, v: dict[str, str]) -> dict[str, str]:
        """Validate environment variables are valid rclone vars."""
        valid_prefixes = ("RCLONE_", "AWS_", "AZURE_", "GCS_", "GOOGLE_")
        for key in v:
            if not any(key.startswith(p) for p in valid_prefixes):
                msg = f"Invalid env var (must start with RCLONE_/AWS_/AZURE_/GCS_/GOOGLE_): {key}"
                raise ValueError(msg)
        return v

    model_config = {"frozen": True}  # Immutable after creation


class ProgressEvent(BaseModel):
    """Progress update event from rclone."""

    type: Literal["progress"] = "progress"
    timestamp: datetime = Field(default_factory=datetime.now)
    bytes_transferred: int = 0
    total_bytes: int = 0
    progress: float = 0.0  # 0.0 to 1.0
    transfer_rate: int = 0  # bytes/sec
    eta_seconds: int | None = None
    current_file: str | None = None
    files_transferred: int = 0
    total_files: int | None = None

    @classmethod
    def from_rclone_stats(cls, stats: dict[str, Any]) -> ProgressEvent:
        """Create ProgressEvent from rclone stats dict."""
        total_bytes = stats.get("totalBytes", 0)
        bytes_transferred = stats.get("bytes", 0)
        progress = bytes_transferred / total_bytes if total_bytes > 0 else 0.0

        # Calculate ETA
        speed = stats.get("speed", 0)
        eta_seconds = None
        if speed > 0 and total_bytes > bytes_transferred:
            remaining_bytes = total_bytes - bytes_transferred
            eta_seconds = int(remaining_bytes / speed)

        # Get current file from transferring list
        current_file = None
        transferring = stats.get("transferring", [])
        if transferring:
            current_file = transferring[0].get("name")

        return cls(
            bytes_transferred=bytes_transferred,
            total_bytes=total_bytes,
            progress=progress,
            transfer_rate=speed,
            eta_seconds=eta_seconds,
            current_file=current_file,
            files_transferred=stats.get("transfers", 0),
        )


class ErrorEvent(BaseModel):
    """Enhanced error event with context."""

    type: Literal["error"] = "error"
    timestamp: datetime = Field(default_factory=datetime.now)
    message: str
    file: str | None = None
    retry_attempt: int = 0
    max_retries: int = 3
    is_retryable: bool = False
    error_category: Literal[
        "network", "permission", "space", "not_found", "config", "unknown"
    ] = "unknown"
    error_code: str | None = None  # Rclone-specific error code

    @classmethod
    def from_rclone_error(cls, error_dict: dict[str, Any]) -> ErrorEvent:
        """Create ErrorEvent from rclone error dict."""
        message = error_dict.get("msg", "Unknown error")
        obj = error_dict.get("object")

        # Categorize error based on message
        category: Literal[
            "network", "permission", "space", "not_found", "config", "unknown"
        ] = "unknown"
        is_retryable = False

        message_lower = message.lower()
        if any(
            x in message_lower
            for x in ["network", "connection", "timeout", "temporary", "retry"]
        ):
            category = "network"
            is_retryable = True
        elif any(
            x in message_lower for x in ["permission", "denied", "forbidden", "unauthorized"]
        ):
            category = "permission"
        elif any(x in message_lower for x in ["space", "quota", "full", "storage"]):
            category = "space"
        elif any(x in message_lower for x in ["not found", "no such", "missing"]):
            category = "not_found"
        elif any(x in message_lower for x in ["config", "invalid", "malformed"]):
            category = "config"

        return cls(
            message=message,
            file=obj,
            error_category=category,
            is_retryable=is_retryable,
        )


class CommandResult(BaseModel):
    """Final result of an rclone command operation."""

    success: bool
    return_code: int
    bytes_transferred: int = 0
    files_transferred: int = 0
    errors: list[ErrorEvent] = Field(default_factory=list)
    duration_seconds: float = 0.0
    stats: dict[str, Any] = Field(default_factory=dict)
    stdout: str = ""
    stderr: str = ""


# Specific result types for different commands
class SyncResult(CommandResult):
    """Result of a sync operation."""

    pass


class CopyResult(CommandResult):
    """Result of a copy operation."""

    pass


class MoveResult(CommandResult):
    """Result of a move operation."""

    pass


class ListResult(BaseModel):
    """Result of a list operation."""

    items: list[dict[str, Any]] = Field(default_factory=list)
    total_count: int = 0
    total_size: int = 0


# Adaptive progress configuration
class AdaptiveProgressConfig(BaseModel):
    """Configuration for adaptive progress update intervals."""

    min_interval: float = 1.0  # Minimum seconds between updates
    max_interval: float = 60.0  # Maximum seconds between updates
    small_file_threshold: int = 10 * 1024 * 1024  # 10MB
    large_file_threshold: int = 1024 * 1024 * 1024  # 1GB

    def calculate_interval(
        self,
        total_bytes: int,
        transfer_rate: int,
        current_file_size: int | None = None,
    ) -> float:
        """Calculate optimal update interval based on operation size."""
        # Small files: update frequently
        if current_file_size and current_file_size < self.small_file_threshold:
            return self.min_interval

        # Large operations: scale interval with size
        if total_bytes > self.large_file_threshold:
            # Update every 1% of progress
            if transfer_rate > 0:
                one_percent_time = (total_bytes * 0.01) / transfer_rate
                return min(max(one_percent_time, self.min_interval), self.max_interval)
            return 10.0  # Default for unknown rate

        # Medium operations: fixed interval
        return 5.0


# Grace periods for different commands
GRACE_PERIODS: dict[str, float] = {
    "move": 30.0,  # Needs time to complete atomic operations
    "sync": 15.0,  # May be updating metadata
    "bisync": 20.0,  # Complex two-way sync
    "mount": 10.0,  # Needs clean unmount
    "serve": 10.0,  # Graceful server shutdown
    "rcd": 10.0,  # Remote control daemon
    "default": 5.0,  # Default for all others
}
