"""
rclone-adapter: Modern async Python wrapper for rclone.

This package provides a Pythonic interface to rclone with async/await support,
type hints, progress tracking, and structured logging.
"""

from rclone.client import RClone
from rclone.exceptions import (
    RCloneCancelledError,
    RCloneConfigError,
    RCloneError,
    RCloneNotFoundError,
    RCloneProcessError,
    RCloneTimeoutError,
)
from rclone.models import (
    AdaptiveProgressConfig,
    CommandResult,
    CopyResult,
    ErrorEvent,
    ListResult,
    MoveResult,
    ProgressEvent,
    RCloneConfig,
    SyncResult,
)

__version__ = "0.1.0"

__all__ = [
    # Main client
    "RClone",
    # Configuration
    "RCloneConfig",
    "AdaptiveProgressConfig",
    # Events
    "ProgressEvent",
    "ErrorEvent",
    # Results
    "CommandResult",
    "SyncResult",
    "CopyResult",
    "MoveResult",
    "ListResult",
    # Exceptions
    "RCloneError",
    "RCloneNotFoundError",
    "RCloneProcessError",
    "RCloneConfigError",
    "RCloneTimeoutError",
    "RCloneCancelledError",
]
