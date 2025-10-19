"""Parser for rclone --use-json-log output."""

from __future__ import annotations

import json
from typing import Any

import structlog

from rclone.models import ErrorEvent, ProgressEvent

logger = structlog.get_logger()


def parse_json_log_line(line: bytes | str) -> ProgressEvent | ErrorEvent | None:
    """
    Parse a single line from rclone --use-json-log output.

    Args:
        line: A line of JSON output from rclone stderr

    Returns:
        ProgressEvent, ErrorEvent, or None if line can't be parsed
    """
    if isinstance(line, bytes):
        try:
            line = line.decode("utf-8")
        except UnicodeDecodeError:
            logger.warning("parser.decode_failed", line=line)
            return None

    line = line.strip()
    if not line:
        return None

    try:
        data = json.loads(line)
    except json.JSONDecodeError as e:
        logger.debug("parser.json_decode_failed", line=line[:100], error=str(e))
        return None

    # Check what type of log entry this is
    level = data.get("level", "").lower()
    msg = data.get("msg", "")
    source = data.get("source", "")

    # Error event
    if level == "error" or "error" in msg.lower():
        return ErrorEvent.from_rclone_error(data)

    # Progress/stats event
    if "stats" in data:
        stats = data["stats"]
        # Only create progress events if we have useful stats
        if stats.get("totalBytes", 0) > 0 or stats.get("bytes", 0) > 0:
            return ProgressEvent.from_rclone_stats(stats)

    # Check if it's an accounting/stats source
    if "accounting/stats" in source:
        stats = data.get("stats", {})
        if stats:
            return ProgressEvent.from_rclone_stats(stats)

    # Not a recognized event type
    return None


def parse_stats_dict(stats: dict[str, Any]) -> dict[str, Any]:
    """
    Extract and normalize stats from rclone output.

    Args:
        stats: Raw stats dict from rclone

    Returns:
        Normalized stats dictionary
    """
    return {
        "bytes": stats.get("bytes", 0),
        "total_bytes": stats.get("totalBytes", 0),
        "speed": stats.get("speed", 0),
        "transfers": stats.get("transfers", 0),
        "checks": stats.get("checks", 0),
        "errors": stats.get("errors", 0),
        "deletes": stats.get("deletes", 0),
        "renames": stats.get("renames", 0),
        "elapsed_time": stats.get("elapsedTime", 0),
        "last_error": stats.get("lastError"),
        "transferring": stats.get("transferring", []),
        "checking": stats.get("checking", []),
    }


def parse_operations_dict(ops: dict[str, Any]) -> dict[str, Any]:
    """
    Extract and normalize operations from rclone output.

    Args:
        ops: Raw operations dict from rclone

    Returns:
        Normalized operations dictionary
    """
    return {
        "name": ops.get("name", ""),
        "size": ops.get("size", 0),
        "bytes": ops.get("bytes", 0),
        "checked": ops.get("checked", False),
        "started_at": ops.get("started_at"),
        "completed_at": ops.get("completed_at"),
        "error": ops.get("error"),
    }


def extract_final_stats(stderr: str) -> dict[str, Any] | None:
    """
    Extract the final stats from complete stderr output.

    This parses all JSON log lines and returns the last stats entry.

    Args:
        stderr: Complete stderr output from rclone

    Returns:
        Final stats dict or None if no stats found
    """
    final_stats = None

    for line in stderr.split("\n"):
        line = line.strip()
        if not line:
            continue

        try:
            data = json.loads(line)
            if "stats" in data:
                final_stats = data["stats"]
        except json.JSONDecodeError:
            continue

    return parse_stats_dict(final_stats) if final_stats else None


def categorize_rclone_return_code(code: int) -> dict[str, Any]:
    """
    Categorize rclone return codes into structured information.

    Args:
        code: rclone process return code

    Returns:
        Dictionary with code, category, description, and is_retryable
    """
    codes = {
        0: ("success", "Success", False),
        1: ("syntax", "Syntax or usage error", False),
        2: ("uncategorized", "Error not otherwise categorized", True),
        3: ("directory_not_found", "Directory not found", False),
        4: ("file_not_found", "File not found", False),
        5: ("temporary", "Temporary error (retries might fix)", True),
        6: ("less_serious", "Less serious errors (like 461 from dropbox)", True),
        7: ("fatal", "Fatal error (retries won't fix, like account suspended)", False),
        8: ("transfer_exceeded", "Transfer exceeded --max-transfer limit", False),
        9: ("no_files_transferred", "Operation successful but no files transferred", False),
    }

    category, description, is_retryable = codes.get(code, ("unknown", "Unknown error", False))

    return {
        "code": code,
        "category": category,
        "description": description,
        "is_retryable": is_retryable,
    }
