"""Process manager for rclone subprocess lifecycle with graceful cleanup."""

from __future__ import annotations

import asyncio
import os
import signal
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog

from rclone.models import GRACE_PERIODS, ErrorEvent, ProgressEvent
from rclone.parser import parse_json_log_line

logger = structlog.get_logger()


class ProcessManager:
    """Manages rclone subprocess lifecycle with configurable grace periods."""

    def __init__(self) -> None:
        """Initialize process manager."""
        self._active_processes: dict[int, asyncio.subprocess.Process] = {}

    @asynccontextmanager
    async def run_command(
        self,
        cmd: list[str],
        env: dict[str, str],
        command_name: str = "default",
    ) -> AsyncIterator[asyncio.subprocess.Process]:
        """
        Context manager for subprocess with command-specific cleanup.

        Args:
            cmd: Command and arguments to execute
            env: Environment variables
            command_name: Name of rclone command for grace period lookup

        Yields:
            Running subprocess
        """
        grace_period = GRACE_PERIODS.get(command_name, GRACE_PERIODS["default"])

        logger.info(
            "process.starting",
            command=command_name,
            cmd=cmd[:3],  # Only log first 3 args for brevity
            grace_period=grace_period,
        )

        # Merge with current environment
        full_env = os.environ.copy()
        full_env.update(env)

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=full_env,
            )

            # Track active process
            if process.pid:
                self._active_processes[process.pid] = process
                logger.info("process.started", pid=process.pid, command=command_name)

            try:
                yield process
            finally:
                # Graceful shutdown with command-specific grace period
                if process.returncode is None:
                    logger.info("process.terminating", pid=process.pid, grace_period=grace_period)
                    process.terminate()

                    try:
                        await asyncio.wait_for(process.wait(), timeout=grace_period)
                        logger.info("process.terminated_gracefully", pid=process.pid)
                    except TimeoutError:
                        # Force kill if grace period exceeded
                        logger.warning(
                            "process.force_killing", pid=process.pid, grace_period=grace_period
                        )
                        process.kill()
                        await process.wait()
                        logger.warning("process.killed", pid=process.pid)

        finally:
            # Remove from tracking
            if process.pid and process.pid in self._active_processes:
                del self._active_processes[process.pid]
                logger.debug("process.cleaned_up", pid=process.pid)

    async def stream_progress(
        self, process: asyncio.subprocess.Process
    ) -> AsyncIterator[ProgressEvent | ErrorEvent]:
        """
        Stream progress and error events from rclone stderr.

        Args:
            process: Running subprocess

        Yields:
            ProgressEvent or ErrorEvent instances
        """
        if not process.stderr:
            logger.warning("process.no_stderr", pid=process.pid)
            return

        logger.debug("process.streaming_progress", pid=process.pid)

        async for line in process.stderr:
            event = parse_json_log_line(line)
            if event:
                logger.debug(
                    "process.event",
                    pid=process.pid,
                    event_type=event.type,
                    progress=getattr(event, "progress", None),
                )
                yield event

    async def read_output(self, process: asyncio.subprocess.Process) -> tuple[str, str]:
        """
        Read stdout and stderr from process.

        Args:
            process: Running subprocess

        Returns:
            Tuple of (stdout, stderr) as strings
        """
        stdout_data = b""
        stderr_data = b""

        if process.stdout:
            stdout_data = await process.stdout.read()
        if process.stderr:
            stderr_data = await process.stderr.read()

        stdout = stdout_data.decode("utf-8", errors="replace")
        stderr = stderr_data.decode("utf-8", errors="replace")

        logger.debug(
            "process.output_read",
            pid=process.pid,
            stdout_len=len(stdout),
            stderr_len=len(stderr),
        )

        return stdout, stderr

    async def cancel_process(self, pid: int, timeout: float = 5.0) -> bool:
        """
        Cancel a running process gracefully.

        Args:
            pid: Process ID to cancel
            timeout: Timeout for graceful termination

        Returns:
            True if cancelled successfully
        """
        if pid not in self._active_processes:
            logger.warning("process.not_found_for_cancel", pid=pid)
            return False

        process = self._active_processes[pid]
        logger.info("process.cancelling", pid=pid)

        try:
            process.terminate()
            await asyncio.wait_for(process.wait(), timeout=timeout)
            logger.info("process.cancelled_gracefully", pid=pid)
            return True
        except TimeoutError:
            logger.warning("process.cancel_timeout_killing", pid=pid)
            process.kill()
            await process.wait()
            logger.warning("process.cancelled_force", pid=pid)
            return True
        except Exception as e:
            logger.error("process.cancel_failed", pid=pid, error=str(e))
            return False

    def get_active_processes(self) -> list[int]:
        """
        Get list of active process IDs.

        Returns:
            List of PIDs
        """
        return list(self._active_processes.keys())

    async def cleanup_orphaned_processes(self) -> None:
        """Clean up any orphaned rclone processes."""
        import psutil

        try:
            for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                try:
                    if proc.info["name"] == "rclone":
                        pid = proc.info["pid"]
                        if pid not in self._active_processes:
                            logger.warning("process.orphaned_found", pid=pid)
                            # Send SIGTERM to orphaned rclone process
                            os.kill(pid, signal.SIGTERM)
                            logger.info("process.orphaned_terminated", pid=pid)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except ImportError:
            logger.debug("process.psutil_not_available")
