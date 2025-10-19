#!/usr/bin/env python3
"""
Synchronous wrapper example.

Shows how to use rclone-adapter in non-async code.
"""

from rclone import RClone


def main() -> None:
    """Run sync with blocking wrapper."""
    # Initialize client with defaults
    rc = RClone()

    # Use blocking wrapper (runs async code internally)
    print("Starting sync (blocking)...")
    result = rc.sync_blocking(
        source="/path/to/source",
        dest="/path/to/dest",
    )

    if result.success:
        print("✅ Sync successful!")
        print(f"  Transferred: {result.files_transferred} files")
        print(f"  Size: {result.bytes_transferred / 1024 / 1024:.2f} MB")
        print(f"  Time: {result.duration_seconds:.2f}s")
    else:
        print(f"❌ Sync failed with code {result.return_code}")
        for error in result.errors:
            print(f"  Error: {error.message}")


if __name__ == "__main__":
    main()
