#!/usr/bin/env python3
"""
Progress streaming example.

Shows how to monitor real-time progress during transfers.
"""

import asyncio

from rclone import ErrorEvent, ProgressEvent, RClone


async def main() -> None:
    """Stream progress during sync operation."""
    rc = RClone()

    print("Starting sync with progress monitoring...")
    print()

    async for event in rc.sync_stream(
        source="/path/to/source",
        dest="remote:bucket/dest",
    ):
        if isinstance(event, ProgressEvent):
            # Progress update
            progress_pct = event.progress * 100
            mb_transferred = event.bytes_transferred / 1024 / 1024
            mb_total = event.total_bytes / 1024 / 1024
            speed_mbps = event.transfer_rate / 1024 / 1024

            print(
                f"\r📊 Progress: {progress_pct:5.1f}% | "
                f"{mb_transferred:,.1f}/{mb_total:,.1f} MB | "
                f"Speed: {speed_mbps:.2f} MB/s | "
                f"File: {event.current_file or 'N/A'}",
                end="",
                flush=True,
            )

        elif isinstance(event, ErrorEvent):
            # Error during transfer
            print()
            print(f"⚠️  Error: {event.message} (file: {event.file})")
            print(f"   Category: {event.error_category}, Retryable: {event.is_retryable}")

        else:
            # Final result
            print()
            print()
            print("✅ Transfer complete!")
            print(f"  Files: {event.files_transferred}")
            print(f"  Size: {event.bytes_transferred / 1024 / 1024:.2f} MB")
            print(f"  Duration: {event.duration_seconds:.1f}s")
            print(f"  Errors: {len(event.errors)}")


if __name__ == "__main__":
    asyncio.run(main())
