#!/usr/bin/env python3
"""
Basic async usage example for rclone-adapter.

This example shows the simplest way to use rclone-adapter with async/await.
"""

import asyncio

from rclone import RClone, RCloneConfig


async def main() -> None:
    """Run a simple sync operation."""
    # Create configuration (optional - uses defaults if not provided)
    config = RCloneConfig(
        # Optional: specify custom rclone path
        # rclone_path="/custom/path/to/rclone",
        # Optional: add environment variables
        env_vars={
            "RCLONE_S3_PROVIDER": "AWS",
            "RCLONE_S3_REGION": "us-west-2",
        },
        # Optional: specify config file
        # config_file=Path("~/.config/rclone/rclone.conf"),
    )

    # Initialize client
    rc = RClone(config)

    # Simple sync - returns only final result
    print("Starting sync...")
    result = await rc.sync(
        source="/path/to/source",
        dest="remote:bucket/dest",
    )

    print("✅ Sync complete!")
    print(f"  Success: {result.success}")
    print(f"  Files transferred: {result.files_transferred}")
    print(f"  Bytes transferred: {result.bytes_transferred:,}")
    print(f"  Duration: {result.duration_seconds:.2f}s")
    print(f"  Errors: {len(result.errors)}")


if __name__ == "__main__":
    asyncio.run(main())
