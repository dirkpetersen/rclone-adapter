"""Tests for Pydantic models."""

import pytest
from pydantic import ValidationError

from rclone.models import (
    AdaptiveProgressConfig,
    ErrorEvent,
    ProgressEvent,
    RCloneConfig,
)


class TestRCloneConfig:
    """Test RCloneConfig validation."""

    def test_config_with_valid_env_vars(self, mock_rclone_config):
        """Test config accepts valid environment variables."""
        assert mock_rclone_config.env_vars == {"RCLONE_S3_PROVIDER": "AWS"}

    def test_config_rejects_invalid_env_vars(self):
        """Test config rejects invalid environment variables."""
        from unittest.mock import patch

        with patch("shutil.which", return_value="/usr/bin/rclone"):
            with pytest.raises(ValidationError) as exc_info:
                RCloneConfig(env_vars={"INVALID_VAR": "value"})

            assert "Invalid env var" in str(exc_info.value)

    def test_config_validates_rclone_path(self):
        """Test config validates rclone executable exists."""
        from unittest.mock import patch

        with patch("shutil.which", return_value=None):
            with pytest.raises(ValidationError) as exc_info:
                RCloneConfig(rclone_path="/nonexistent/rclone")

            assert "rclone not found" in str(exc_info.value)

    def test_config_is_immutable(self, mock_rclone_config):
        """Test config cannot be modified after creation."""
        with pytest.raises(ValidationError):
            mock_rclone_config.rclone_path = "/new/path"


class TestProgressEvent:
    """Test ProgressEvent model."""

    def test_progress_event_from_stats(self):
        """Test creating ProgressEvent from rclone stats."""
        stats = {
            "bytes": 5000,
            "totalBytes": 10000,
            "speed": 100,
            "transfers": 1,
            "transferring": [{"name": "file.txt"}],
        }

        event = ProgressEvent.from_rclone_stats(stats)

        assert event.bytes_transferred == 5000
        assert event.total_bytes == 10000
        assert event.progress == 0.5
        assert event.transfer_rate == 100
        assert event.current_file == "file.txt"
        assert event.files_transferred == 1

    def test_progress_event_calculates_eta(self):
        """Test ETA calculation in ProgressEvent."""
        stats = {
            "bytes": 1000,
            "totalBytes": 10000,
            "speed": 100,  # 100 bytes/sec
        }

        event = ProgressEvent.from_rclone_stats(stats)

        # Remaining: 9000 bytes at 100 bytes/sec = 90 seconds
        assert event.eta_seconds == 90


class TestErrorEvent:
    """Test ErrorEvent model."""

    def test_error_event_categorizes_network_errors(self):
        """Test error categorization for network errors."""
        error = {"msg": "connection timeout", "object": "file.txt"}

        event = ErrorEvent.from_rclone_error(error)

        assert event.error_category == "network"
        assert event.is_retryable is True
        assert event.file == "file.txt"

    def test_error_event_categorizes_permission_errors(self):
        """Test error categorization for permission errors."""
        error = {"msg": "permission denied", "object": "file.txt"}

        event = ErrorEvent.from_rclone_error(error)

        assert event.error_category == "permission"
        assert event.is_retryable is False

    def test_error_event_categorizes_not_found_errors(self):
        """Test error categorization for not found errors."""
        error = {"msg": "file not found", "object": "missing.txt"}

        event = ErrorEvent.from_rclone_error(error)

        assert event.error_category == "not_found"
        assert event.is_retryable is False


class TestAdaptiveProgressConfig:
    """Test adaptive progress configuration."""

    def test_calculate_interval_for_small_files(self):
        """Test progress interval for small files."""
        config = AdaptiveProgressConfig()

        # Small file (1MB)
        interval = config.calculate_interval(
            total_bytes=100 * 1024 * 1024,  # 100MB total
            transfer_rate=1024 * 1024,  # 1MB/s
            current_file_size=1024 * 1024,  # 1MB current file
        )

        assert interval == config.min_interval

    def test_calculate_interval_for_large_operations(self):
        """Test progress interval scales for large operations."""
        config = AdaptiveProgressConfig()

        # Large operation (10GB)
        interval = config.calculate_interval(
            total_bytes=10 * 1024**3,  # 10GB
            transfer_rate=100 * 1024**2,  # 100MB/s
            current_file_size=None,
        )

        # Should be between min and max
        assert config.min_interval <= interval <= config.max_interval

    def test_calculate_interval_for_unknown_rate(self):
        """Test progress interval with unknown transfer rate."""
        config = AdaptiveProgressConfig()

        interval = config.calculate_interval(
            total_bytes=10 * 1024**3,
            transfer_rate=0,  # Unknown
            current_file_size=None,
        )

        assert interval == 10.0  # Default fallback
