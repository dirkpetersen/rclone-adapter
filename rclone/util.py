"""Utility functions for rclone-adapter."""

from __future__ import annotations

import platform
import shutil
from pathlib import Path


def find_rclone_binary() -> str:
    """
    Find rclone binary, preferring bundled version over system PATH.

    Returns:
        Path to rclone executable

    Raises:
        FileNotFoundError: If rclone is not found
    """
    # Try bundled rclone binary first
    bundled_path = _get_bundled_rclone_path()
    if bundled_path and bundled_path.exists():
        return str(bundled_path)

    # Fall back to system PATH
    system_rclone = shutil.which("rclone")
    if system_rclone:
        return system_rclone

    raise FileNotFoundError(
        "rclone not found. Install rclone from https://rclone.org/install/ "
        "or use: pip install rclone-adapter"
    )


def _get_bundled_rclone_path() -> Path | None:
    """Get path to bundled rclone binary based on current platform."""
    # Get package bin directory
    pkg_bin = Path(__file__).parent / "bin"

    if not pkg_bin.exists():
        return None

    system = platform.system()
    machine = platform.machine()

    # Map platform and architecture to bundled binary
    if system == "Linux":
        if machine == "x86_64":
            return pkg_bin / "rclone-linux-amd64"
        elif machine == "aarch64":
            return pkg_bin / "rclone-linux-arm64"
    elif system == "Darwin":  # macOS
        if machine == "x86_64":
            return pkg_bin / "rclone-macos-x86_64"
        elif machine == "arm64":
            return pkg_bin / "rclone-macos-arm64"
    elif system == "Windows":
        return pkg_bin / "rclone-windows-amd64.exe"

    return None
