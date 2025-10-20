"""Pytest configuration and fixtures."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock

import pytest


@pytest.fixture(scope="session")
def event_loop_policy():
    """Use asyncio event loop policy."""
    return asyncio.DefaultEventLoopPolicy()


@pytest.fixture
def mock_rclone_config():
    """Mock RCloneConfig for testing."""
    from unittest.mock import patch

    from rclone.models import RCloneConfig

    # Mock both find_rclone_binary and shutil.which to return consistent values
    with (
        patch("rclone.models.find_rclone_binary", return_value="rclone"),
        patch("shutil.which", return_value="rclone"),
    ):
        config = RCloneConfig(
            rclone_path="rclone",
            env_vars={"RCLONE_S3_PROVIDER": "AWS"},
        )
    return config


@pytest.fixture
def mock_subprocess():
    """Mock subprocess for testing without actual rclone."""
    from collections.abc import AsyncIterator

    mock_process = AsyncMock()
    mock_process.pid = 12345
    mock_process.returncode = 0

    # Mock stderr as a stream that supports iteration and read()
    mock_progress_lines = [
        b'{"level":"info","msg":"Starting transfer","time":"2025-01-01T00:00:00Z"}',
        b'{"level":"info","msg":"Progress","stats":{"bytes":1000,"totalBytes":10000,"speed":100,"transfers":0},"time":"2025-01-01T00:00:01Z"}',
        b'{"level":"info","msg":"Progress","stats":{"bytes":5000,"totalBytes":10000,"speed":100,"transfers":0},"time":"2025-01-01T00:00:05Z"}',
        b'{"level":"info","msg":"Complete","stats":{"bytes":10000,"totalBytes":10000,"speed":100,"transfers":1},"time":"2025-01-01T00:00:10Z"}',
    ]

    class MockStderr(AsyncIterator):
        """Mock stderr that supports both async iteration and read()."""

        def __init__(self):
            self.lines = iter(mock_progress_lines)
            self.all_data = b"\n".join(mock_progress_lines)

        def __aiter__(self):
            return self

        async def __anext__(self):
            try:
                return next(self.lines)
            except StopIteration:
                raise StopAsyncIteration

        async def read(self):
            return self.all_data

    mock_process.stderr = MockStderr()
    mock_process.stdout = AsyncMock()
    mock_process.stdout.read = AsyncMock(return_value=b"")

    return mock_process


@pytest.fixture
def mock_process_manager(mock_subprocess):
    """Mock ProcessManager for testing."""
    from contextlib import asynccontextmanager
    from unittest.mock import patch

    @asynccontextmanager
    async def mock_run_command(cmd, env, command_name="default"):
        yield mock_subprocess

    with patch(
        "rclone.process.ProcessManager.run_command",
        side_effect=mock_run_command,
    ):
        yield


# Markers
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test requiring rclone installed",
    )
    config.addinivalue_line(
        "markers",
        "benchmark: mark test as performance/benchmark test",
    )
