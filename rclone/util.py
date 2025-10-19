"""Utility functions for rclone-adapter."""

from __future__ import annotations

import platform
import shutil
from pathlib import Path
from importlib.resources import files


def find_rclone_binary() -> str:
    """
    Find rclone binary, preferring bundled version over system PATH.

    Uses importlib.resources to access bundled binaries in an installation-agnostic way.
    Supports wheel installs, editable installs, and zip imports.

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
    """
    Get path to bundled rclone binary based on current platform.

    Uses importlib.resources.files() for robust resource access across:
    - Wheel installations
    - Editable (development) installs
    - Zip imports
    - Traditional setuptools installs

    Returns:
        Path to rclone binary if it exists, None otherwise
    """
    try:
        # Get the bin package/resource directory
        bin_resources = files("rclone").joinpath("bin")

        system = platform.system()
        machine = platform.machine()

        # Map platform and architecture to bundled binary filename
        binary_name: str | None = None
        if system == "Linux":
            if machine == "x86_64":
                binary_name = "rclone-linux-amd64"
            elif machine == "aarch64":
                binary_name = "rclone-linux-arm64"
        elif system == "Darwin":  # macOS
            if machine == "x86_64":
                binary_name = "rclone-macos-x86_64"
            elif machine == "arm64":
                binary_name = "rclone-macos-arm64"
        elif system == "Windows":
            binary_name = "rclone-windows-amd64.exe"

        if not binary_name:
            return None

        # Get the resource
        binary_resource = bin_resources.joinpath(binary_name)

        # Check if resource exists and get its path
        # For wheel installs, this returns the actual file path
        # For editable installs, this returns the development directory path
        if hasattr(binary_resource, "is_file") and binary_resource.is_file():
            # For Traversable objects, convert to Path
            return Path(str(binary_resource))

        # Fallback: try to get as regular file path
        return Path(str(binary_resource)) if binary_resource.read_text is not None else None

    except (ImportError, AttributeError, TypeError):
        # Fallback to direct filesystem path if importlib.resources fails
        # This handles development/editable installs with direct file access
        pkg_bin = Path(__file__).parent / "bin"

        if not pkg_bin.exists():
            return None

        system = platform.system()
        machine = platform.machine()

        if system == "Linux":
            if machine == "x86_64":
                return pkg_bin / "rclone-linux-amd64"
            elif machine == "aarch64":
                return pkg_bin / "rclone-linux-arm64"
        elif system == "Darwin":
            if machine == "x86_64":
                return pkg_bin / "rclone-macos-x86_64"
            elif machine == "arm64":
                return pkg_bin / "rclone-macos-arm64"
        elif system == "Windows":
            return pkg_bin / "rclone-windows-amd64.exe"

        return None
