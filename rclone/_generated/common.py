"""Common options shared across commands."""
# AUTO-GENERATED - DO NOT EDIT

from pydantic import BaseModel, Field


class CommonOptions(BaseModel):
    """Common options available for all rclone commands."""

    verbose: int = Field(0, description="Print lots more stuff (repeat for more)")
    quiet: bool = Field(False, description="Print as little stuff as possible")
    dry_run: bool = Field(False, description="Do a trial run with no permanent changes")
    interactive: bool = Field(False, description="Enable interactive mode")
    progress: bool = Field(False, description="Show progress during transfer")
