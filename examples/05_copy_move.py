#!/usr/bin/env python3
"""
Copy and move operations example.

Shows different rclone operations beyond sync.
"""

import asyncio

from rclone import RClone


async def main() -> None:
    """Demonstrate copy and move operations."""
    rc = RClone()

    # Copy files (source remains intact)
    print("🔄 Copying files...")
    copy_result = await rc.copy(
        source="/path/to/source",
        dest="remote:bucket/backup",
    )

    print(f"  Copied {copy_result.files_transferred} files")
    print(f"  Size: {copy_result.bytes_transferred / 1024 / 1024:.2f} MB")
    print()

    # Move files (source is removed after transfer)
    print("📦 Moving files...")
    move_result = await rc.move(
        source="/path/to/archive",
        dest="remote:bucket/archive",
    )

    print(f"  Moved {move_result.files_transferred} files")
    print(f"  Size: {move_result.bytes_transferred / 1024 / 1024:.2f} MB")
    print()

    # Get rclone version
    version = await rc.version()
    print(f"ℹ️  Using {version}")


if __name__ == "__main__":
    asyncio.run(main())
