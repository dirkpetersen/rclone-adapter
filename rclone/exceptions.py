"""Exception hierarchy for rclone-adapter."""


class RCloneError(Exception):
    """Base exception for all rclone-adapter errors."""

    pass


class RCloneNotFoundError(RCloneError):
    """Raised when rclone executable is not found on the system."""

    def __init__(self, path: str = "rclone") -> None:
        """Initialize with the path that was searched."""
        self.path = path
        super().__init__(f"rclone executable not found at: {path}")


class RCloneProcessError(RCloneError):
    """Raised when an rclone process fails."""

    def __init__(self, return_code: int, message: str, command: str | None = None) -> None:
        """Initialize with process details."""
        self.return_code = return_code
        self.message = message
        self.command = command
        error_msg = f"rclone failed with code {return_code}: {message}"
        if command:
            error_msg = f"{error_msg} (command: {command})"
        super().__init__(error_msg)


class RCloneConfigError(RCloneError):
    """Raised when configuration is invalid."""

    pass


class RCloneTimeoutError(RCloneError):
    """Raised when an operation times out."""

    def __init__(self, timeout: float, operation: str | None = None) -> None:
        """Initialize with timeout details."""
        self.timeout = timeout
        self.operation = operation
        msg = f"Operation timed out after {timeout} seconds"
        if operation:
            msg = f"{msg}: {operation}"
        super().__init__(msg)


class RCloneCancelledError(RCloneError):
    """Raised when an operation is cancelled by the user."""

    def __init__(self, job_id: str | None = None) -> None:
        """Initialize with optional job ID."""
        self.job_id = job_id
        msg = "Operation was cancelled"
        if job_id:
            msg = f"{msg} (job_id: {job_id})"
        super().__init__(msg)
