#!/usr/bin/env python3
"""
Progress callback example.

Shows how to use callbacks for progress updates (useful for integrating with UIs).
"""

import asyncio

from rclone import ProgressEvent, RClone


class ProgressTracker:
    """Custom progress tracker for UI integration."""

    def __init__(self) -> None:
        """Initialize tracker."""
        self.last_progress = 0.0
        self.updates = 0

    def on_progress(self, event: ProgressEvent) -> None:
        """Handle progress update."""
        self.updates += 1

        # Only print every 10% change
        if event.progress - self.last_progress >= 0.1:
            print(
                f"📦 {event.progress * 100:.0f}% complete "
                f"({event.bytes_transferred / 1024 / 1024:.1f} MB)"
            )
            self.last_progress = event.progress


async def main() -> None:
    """Use callback for progress monitoring."""
    rc = RClone()
    tracker = ProgressTracker()

    print("Starting sync with callback...")

    result = await rc.sync(
        source="/path/to/source",
        dest="remote:bucket/dest",
        progress_callback=tracker.on_progress,
    )

    print()
    print("✅ Complete!")
    print(f"  Success: {result.success}")
    print(f"  Progress updates received: {tracker.updates}")
    print(f"  Files: {result.files_transferred}")
    print(f"  Duration: {result.duration_seconds:.1f}s")


if __name__ == "__main__":
    asyncio.run(main())
