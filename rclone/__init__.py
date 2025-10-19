"""
rclone-adapter: Modern async Python wrapper for rclone.

This package provides a Pythonic interface to rclone with async/await support,
type hints, progress tracking, and structured logging.
"""

from __future__ import annotations

from importlib.metadata import version

from rclone.client import RClone
from rclone.exceptions import (
    RCloneCancelledError,
    RCloneConfigError,
    RCloneError,
    RCloneNotFoundError,
    RCloneProcessError,
    RCloneTimeoutError,
)
from rclone.models import (
    AdaptiveProgressConfig,
    CommandResult,
    CopyResult,
    ErrorEvent,
    ListResult,
    MoveResult,
    ProgressEvent,
    RCloneConfig,
    SyncResult,
)

# Get version from package metadata
try:
    __version__ = version("rclone-adapter")
except Exception:
    __version__ = "0.0.0+unknown"

__all__ = [
    # Main client
    "RClone",
    # Configuration
    "RCloneConfig",
    "AdaptiveProgressConfig",
    # Events
    "ProgressEvent",
    "ErrorEvent",
    # Results
    "CommandResult",
    "SyncResult",
    "CopyResult",
    "MoveResult",
    "ListResult",
    # Exceptions
    "RCloneError",
    "RCloneNotFoundError",
    "RCloneProcessError",
    "RCloneConfigError",
    "RCloneTimeoutError",
    "RCloneCancelledError",
]
