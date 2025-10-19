"""Tests for rclone log parser."""


from rclone.models import ErrorEvent, ProgressEvent
from rclone.parser import (
    categorize_rclone_return_code,
    extract_final_stats,
    parse_json_log_line,
)


class TestParseJsonLogLine:
    """Test JSON log line parsing."""

    def test_parse_progress_event(self):
        """Test parsing progress event."""
        line = b'{"level":"info","stats":{"bytes":1000,"totalBytes":10000,"speed":100}}'

        event = parse_json_log_line(line)

        assert isinstance(event, ProgressEvent)
        assert event.bytes_transferred == 1000
        assert event.total_bytes == 10000

    def test_parse_error_event(self):
        """Test parsing error event."""
        line = b'{"level":"error","msg":"connection failed","object":"file.txt"}'

        event = parse_json_log_line(line)

        assert isinstance(event, ErrorEvent)
        assert "connection failed" in event.message

    def test_parse_invalid_json(self):
        """Test handling invalid JSON."""
        line = b"not json at all"

        event = parse_json_log_line(line)

        assert event is None

    def test_parse_empty_line(self):
        """Test handling empty lines."""
        line = b""

        event = parse_json_log_line(line)

        assert event is None

    def test_parse_unicode_decode_error(self):
        """Test handling unicode decode errors."""
        line = b"\xff\xfe invalid utf-8"

        event = parse_json_log_line(line)

        assert event is None


class TestExtractFinalStats:
    """Test extracting final stats from stderr."""

    def test_extract_final_stats(self):
        """Test extracting final stats from complete output."""
        stderr = """
{"level":"info","msg":"Start"}
{"level":"info","stats":{"bytes":1000,"totalBytes":10000}}
{"level":"info","stats":{"bytes":5000,"totalBytes":10000}}
{"level":"info","stats":{"bytes":10000,"totalBytes":10000}}
"""

        stats = extract_final_stats(stderr)

        assert stats is not None
        assert stats["bytes"] == 10000
        assert stats["total_bytes"] == 10000

    def test_extract_no_stats(self):
        """Test when there are no stats in output."""
        stderr = """
{"level":"info","msg":"No stats here"}
Some other output
"""

        stats = extract_final_stats(stderr)

        assert stats is None


class TestCategorizeReturnCode:
    """Test rclone return code categorization."""

    def test_categorize_success(self):
        """Test success return code."""
        info = categorize_rclone_return_code(0)

        assert info["code"] == 0
        assert info["category"] == "success"
        assert info["is_retryable"] is False

    def test_categorize_temporary_error(self):
        """Test temporary error is retryable."""
        info = categorize_rclone_return_code(5)

        assert info["category"] == "temporary"
        assert info["is_retryable"] is True

    def test_categorize_fatal_error(self):
        """Test fatal error is not retryable."""
        info = categorize_rclone_return_code(7)

        assert info["category"] == "fatal"
        assert info["is_retryable"] is False

    def test_categorize_unknown_code(self):
        """Test unknown return code."""
        info = categorize_rclone_return_code(99)

        assert info["category"] == "unknown"
        assert info["code"] == 99
