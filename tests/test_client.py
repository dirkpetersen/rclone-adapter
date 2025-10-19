"""Tests for RClone client."""

import pytest

from rclone import RClone, RCloneConfig
from rclone.models import CopyResult, ProgressEvent, SyncResult


@pytest.mark.asyncio
class TestRCloneClient:
    """Test RClone client functionality."""

    async def test_client_initialization(self, mock_rclone_config):
        """Test client can be initialized."""
        client = RClone(mock_rclone_config)

        assert client.config == mock_rclone_config
        assert client.process_manager is not None

    async def test_build_command_basic(self, mock_rclone_config):
        """Test command building."""
        client = RClone(mock_rclone_config)

        cmd = client._build_command("sync", ["/source", "/dest"])

        assert cmd[0] == "rclone"
        assert cmd[1] == "sync"
        assert "--use-json-log" in cmd
        assert "/source" in cmd
        assert "/dest" in cmd

    async def test_build_command_with_config_file(self):
        """Test command building with config file."""
        import tempfile
        from pathlib import Path
        from unittest.mock import patch

        # Create a temporary config file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".conf") as f:
            config_path = Path(f.name)

        try:
            with patch("shutil.which", return_value="/usr/bin/rclone"):
                config = RCloneConfig(config_file=config_path)
                client = RClone(config)

                cmd = client._build_command("sync", ["/source", "/dest"])

                assert "--config" in cmd
                config_idx = cmd.index("--config")
                assert cmd[config_idx + 1] == str(config_path)
        finally:
            config_path.unlink()

    async def test_sync_stream_yields_events(self, mock_rclone_config, mock_subprocess):
        """Test sync_stream yields progress events."""
        from contextlib import asynccontextmanager
        from unittest.mock import patch

        @asynccontextmanager
        async def mock_run_command(cmd, env, command_name="default"):
            # Reset the async generator
            mock_progress_lines = [
                b'{"level":"info","stats":{"bytes":1000,"totalBytes":10000,"speed":100,"transfers":0}}',
                b'{"level":"info","stats":{"bytes":10000,"totalBytes":10000,"speed":100,"transfers":1}}',
            ]

            async def mock_stderr():
                for line in mock_progress_lines:
                    yield line

            mock_subprocess.stderr = mock_stderr()
            mock_subprocess.returncode = 0
            yield mock_subprocess

        with patch(
            "rclone.client.ProcessManager.run_command",
            side_effect=mock_run_command,
        ):
            client = RClone(mock_rclone_config)

            events = []
            async for event in client.sync_stream("/source", "/dest"):
                events.append(event)

            # Should have progress events and final result
            progress_events = [e for e in events if isinstance(e, ProgressEvent)]
            results = [e for e in events if isinstance(e, SyncResult)]

            assert len(progress_events) > 0
            assert len(results) == 1
            assert results[0].success is True

    async def test_sync_simple_returns_result(self, mock_rclone_config, mock_subprocess):
        """Test sync simple API returns only result."""
        from contextlib import asynccontextmanager
        from unittest.mock import patch

        @asynccontextmanager
        async def mock_run_command(cmd, env, command_name="default"):
            mock_progress_lines = [
                b'{"level":"info","stats":{"bytes":10000,"totalBytes":10000,"speed":100,"transfers":1}}',
            ]

            async def mock_stderr():
                for line in mock_progress_lines:
                    yield line

            mock_subprocess.stderr = mock_stderr()
            mock_subprocess.returncode = 0
            yield mock_subprocess

        with patch(
            "rclone.client.ProcessManager.run_command",
            side_effect=mock_run_command,
        ):
            client = RClone(mock_rclone_config)

            result = await client.sync("/source", "/dest")

            assert isinstance(result, SyncResult)
            assert result.success is True

    async def test_copy_returns_copy_result(self, mock_rclone_config, mock_subprocess):
        """Test copy command returns CopyResult."""
        from contextlib import asynccontextmanager
        from unittest.mock import patch

        @asynccontextmanager
        async def mock_run_command(cmd, env, command_name="default"):
            async def mock_stderr():
                yield b'{"level":"info","stats":{"bytes":1000,"totalBytes":1000}}'

            mock_subprocess.stderr = mock_stderr()
            mock_subprocess.returncode = 0
            yield mock_subprocess

        with patch(
            "rclone.client.ProcessManager.run_command",
            side_effect=mock_run_command,
        ):
            client = RClone(mock_rclone_config)

            result = await client.copy("/source", "/dest")

            assert isinstance(result, CopyResult)
            assert result.success is True

    async def test_version_command(self, mock_rclone_config, mock_subprocess):
        """Test version command."""
        from contextlib import asynccontextmanager
        from unittest.mock import AsyncMock, patch

        @asynccontextmanager
        async def mock_run_command(cmd, env, command_name="default"):
            async def mock_stderr():
                return
                yield  # Empty generator

            mock_subprocess.stderr = mock_stderr()
            mock_subprocess.stdout = AsyncMock()
            mock_subprocess.stdout.read = AsyncMock(return_value=b"rclone v1.65.0\n")
            mock_subprocess.returncode = 0
            yield mock_subprocess

        with patch(
            "rclone.client.ProcessManager.run_command",
            side_effect=mock_run_command,
        ):
            client = RClone(mock_rclone_config)

            version = await client.version()

            assert "rclone" in version or "1.65" in version


@pytest.mark.integration
class TestRCloneIntegration:
    """Integration tests requiring actual rclone installation."""

    async def test_rclone_version_real(self):
        """Test getting real rclone version."""
        import shutil

        if not shutil.which("rclone"):
            pytest.skip("rclone not installed")

        client = RClone()
        version = await client.version()

        assert "rclone" in version.lower() or "v" in version

    def test_sync_blocking_wrapper(self, mock_rclone_config, mock_subprocess):
        """Test synchronous wrapper for sync."""
        from contextlib import asynccontextmanager
        from unittest.mock import patch

        @asynccontextmanager
        async def mock_run_command(cmd, env, command_name="default"):
            async def mock_stderr():
                yield b'{"level":"info","stats":{"bytes":1000,"totalBytes":1000}}'

            mock_subprocess.stderr = mock_stderr()
            mock_subprocess.returncode = 0
            yield mock_subprocess

        with patch(
            "rclone.client.ProcessManager.run_command",
            side_effect=mock_run_command,
        ):
            client = RClone(mock_rclone_config)

            # This should block until complete
            result = client.sync_blocking("/source", "/dest")

            assert isinstance(result, SyncResult)
            assert result.success is True
