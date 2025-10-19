"""Main RClone client with async-first API."""

from __future__ import annotations

import asyncio
import time
from collections.abc import AsyncIterator, Callable

import structlog
from pydantic import BaseModel

from rclone.exceptions import RCloneProcessError
from rclone.models import (
    AdaptiveProgressConfig,
    CommandResult,
    CopyResult,
    ErrorEvent,
    MoveResult,
    ProgressEvent,
    RCloneConfig,
    SyncResult,
)
from rclone.parser import categorize_rclone_return_code, extract_final_stats
from rclone.process import ProcessManager

logger = structlog.get_logger()


class ProgressTracker:
    """Tracks and throttles progress updates based on adaptive configuration."""

    def __init__(self, config: AdaptiveProgressConfig | None = None) -> None:
        """Initialize progress tracker."""
        self.config = config or AdaptiveProgressConfig()
        self.last_update = 0.0
        self.current_interval = 5.0
        self.update_count = 0

    def should_update(self, event: ProgressEvent) -> bool:
        """Check if we should emit this progress update."""
        now = time.time()

        # Recalculate interval based on current metrics
        file_size = len(event.current_file) if event.current_file else None
        self.current_interval = self.config.calculate_interval(
            event.total_bytes,
            event.transfer_rate,
            file_size,
        )

        if now - self.last_update >= self.current_interval:
            self.last_update = now
            self.update_count += 1
            return True
        return False


class RClone:
    """
    Modern async rclone client.

    This is the main interface to rclone. It provides both streaming and simple APIs.
    """

    def __init__(self, config: RCloneConfig | None = None) -> None:
        """
        Initialize RClone client.

        Args:
            config: Optional configuration. If None, uses defaults.
        """
        self.config = config or RCloneConfig()
        self.process_manager = ProcessManager()
        self.logger = structlog.get_logger()

        self.logger.info(
            "client.initialized",
            rclone_path=self.config.rclone_path,
            config_file=str(self.config.config_file) if self.config.config_file else None,
        )

    def _build_command(
        self,
        subcommand: str,
        args: list[str],
        options: BaseModel | None = None,
        extra_flags: list[str] | None = None,
    ) -> list[str]:
        """
        Build rclone command with arguments and options.

        Args:
            subcommand: Rclone subcommand (sync, copy, etc.)
            args: Positional arguments (source, dest, etc.)
            options: Pydantic options model
            extra_flags: Additional flags to add

        Returns:
            Complete command list
        """
        cmd = [self.config.rclone_path, subcommand]

        # Add --use-json-log for structured logging
        cmd.append("--use-json-log")

        # Add config file if specified
        if self.config.config_file:
            cmd.extend(["--config", str(self.config.config_file)])

        # Add default flags
        cmd.extend(self.config.default_flags)

        # Add options from Pydantic model
        if options:
            for field_name, value in options.model_dump(exclude_none=True).items():
                if value is False or value == "":
                    continue  # Skip false booleans and empty strings

                flag = f"--{field_name.replace('_', '-')}"

                if isinstance(value, bool) and value:
                    cmd.append(flag)
                else:
                    cmd.extend([flag, str(value)])

        # Add extra flags
        if extra_flags:
            cmd.extend(extra_flags)

        # Add positional arguments
        cmd.extend(args)

        self.logger.debug("client.command_built", subcommand=subcommand, cmd_length=len(cmd))
        return cmd

    async def _execute_command(
        self,
        subcommand: str,
        args: list[str],
        options: BaseModel | None = None,
        extra_flags: list[str] | None = None,
        stream_progress: bool = False,
        progress_callback: Callable[[ProgressEvent], None] | None = None,
    ) -> AsyncIterator[ProgressEvent | ErrorEvent | CommandResult]:
        """
        Execute rclone command and yield events.

        Args:
            subcommand: Rclone subcommand
            args: Positional arguments
            options: Command options
            extra_flags: Additional flags
            stream_progress: Whether to stream progress events
            progress_callback: Optional callback for progress updates

        Yields:
            ProgressEvent, ErrorEvent, or final CommandResult
        """
        cmd = self._build_command(subcommand, args, options, extra_flags)
        start_time = time.time()
        all_errors: list[ErrorEvent] = []
        last_progress: ProgressEvent | None = None

        self.logger.info(
            "client.command_starting",
            subcommand=subcommand,
            args=args[:2],  # Only log first 2 args
        )

        async with self.process_manager.run_command(
            cmd, self.config.env_vars, subcommand
        ) as process:
            # Stream progress events
            tracker = ProgressTracker()

            async for event in self.process_manager.stream_progress(process):
                if isinstance(event, ProgressEvent):
                    last_progress = event

                    # Apply adaptive throttling
                    if not tracker.should_update(event):
                        continue

                    if stream_progress:
                        yield event

                    if progress_callback:
                        progress_callback(event)

                elif isinstance(event, ErrorEvent):
                    all_errors.append(event)
                    if stream_progress:
                        yield event

            # Wait for process to complete
            await process.wait()
            duration = time.time() - start_time

            # Read any remaining output
            stdout, stderr = await self.process_manager.read_output(process)

            # Extract final stats
            final_stats = extract_final_stats(stderr) or {}

            # Get return code info
            return_code_info = categorize_rclone_return_code(process.returncode or 0)

            self.logger.info(
                "client.command_completed",
                subcommand=subcommand,
                return_code=process.returncode,
                duration=duration,
                errors=len(all_errors),
            )

            # Build final result
            result = CommandResult(
                success=(process.returncode == 0),
                return_code=process.returncode or 0,
                bytes_transferred=last_progress.bytes_transferred if last_progress else 0,
                files_transferred=last_progress.files_transferred if last_progress else 0,
                errors=all_errors,
                duration_seconds=duration,
                stats=final_stats,
                stdout=stdout,
                stderr=stderr,
            )

            yield result

    async def sync_stream(
        self,
        source: str,
        dest: str,
        options: BaseModel | None = None,
    ) -> AsyncIterator[ProgressEvent | ErrorEvent | SyncResult]:
        """
        Sync source to dest with streaming progress.

        Args:
            source: Source path or remote:path
            dest: Destination path or remote:path
            options: Sync options (use SyncOptions from _generated)

        Yields:
            Progress events, error events, and final result
        """
        async for event in self._execute_command(
            "sync", [source, dest], options, stream_progress=True
        ):
            if isinstance(event, CommandResult):
                yield SyncResult(**event.model_dump())
            else:
                yield event

    async def sync(
        self,
        source: str,
        dest: str,
        options: BaseModel | None = None,
        progress_callback: Callable[[ProgressEvent], None] | None = None,
    ) -> SyncResult:
        """
        Sync source to dest (simple API, returns only final result).

        Args:
            source: Source path or remote:path
            dest: Destination path or remote:path
            options: Sync options
            progress_callback: Optional callback for progress updates

        Returns:
            Final sync result
        """
        result: SyncResult | None = None

        async for event in self._execute_command(
            "sync", [source, dest], options, progress_callback=progress_callback
        ):
            if isinstance(event, CommandResult):
                result = SyncResult(**event.model_dump())

        if result is None:
            raise RCloneProcessError(1, "No result returned from sync command")

        return result

    def sync_blocking(
        self,
        source: str,
        dest: str,
        options: BaseModel | None = None,
    ) -> SyncResult:
        """
        Synchronous wrapper for sync (blocks until complete).

        Args:
            source: Source path
            dest: Destination path
            options: Sync options

        Returns:
            Final sync result
        """
        return asyncio.run(self.sync(source, dest, options))

    # Similar methods for other commands...

    async def copy_stream(
        self,
        source: str,
        dest: str,
        options: BaseModel | None = None,
    ) -> AsyncIterator[ProgressEvent | ErrorEvent | CopyResult]:
        """Copy with streaming progress."""
        async for event in self._execute_command(
            "copy", [source, dest], options, stream_progress=True
        ):
            if isinstance(event, CommandResult):
                yield CopyResult(**event.model_dump())
            else:
                yield event

    async def copy(
        self,
        source: str,
        dest: str,
        options: BaseModel | None = None,
        progress_callback: Callable[[ProgressEvent], None] | None = None,
    ) -> CopyResult:
        """Copy source to dest (simple API)."""
        result: CopyResult | None = None

        async for event in self._execute_command(
            "copy", [source, dest], options, progress_callback=progress_callback
        ):
            if isinstance(event, CommandResult):
                result = CopyResult(**event.model_dump())

        if result is None:
            raise RCloneProcessError(1, "No result returned from copy command")

        return result

    async def move(
        self,
        source: str,
        dest: str,
        options: BaseModel | None = None,
    ) -> MoveResult:
        """Move source to dest."""
        result: MoveResult | None = None

        async for event in self._execute_command("move", [source, dest], options):
            if isinstance(event, CommandResult):
                result = MoveResult(**event.model_dump())

        if result is None:
            raise RCloneProcessError(1, "No result returned from move command")

        return result

    async def version(self) -> str:
        """Get rclone version."""
        result: CommandResult | None = None

        async for event in self._execute_command("version", []):
            if isinstance(event, CommandResult):
                result = event

        if result is None:
            raise RCloneProcessError(1, "No result returned from version command")

        return result.stdout.strip()
