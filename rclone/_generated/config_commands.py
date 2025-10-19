"""Generated Pydantic models for rclone commands."""
# AUTO-GENERATED - DO NOT EDIT

from pydantic import BaseModel, Field


class AuthorizeOptions(BaseModel):
    """Options for the 'rclone authorize' command."""

    auth_no_open_browser: bool = Field(False, description="Do not automatically open auth link in default browser")
    template: bool = Field(False, description="string        The path to a custom Go template for generating HTML responses")



class ConfigOptions(BaseModel):
    """Options for the 'rclone config' command."""

    pass



class ListremotesOptions(BaseModel):
    """Options for the 'rclone listremotes' command."""

    description: bool = Field(False, description="string   Filter remotes by description")
    json: bool = Field(False, description="Format output as JSON")
    long: bool = Field(False, description="Show type and description in addition to name")
    name: bool = Field(False, description="string          Filter remotes by name")
    order_by: bool = Field(False, description="string      Instructions on how to order the result, e.g. 'type,name=descending'")
    source: bool = Field(False, description="string        Filter remotes by source, e.g. 'file' or 'environment'")
    type: bool = Field(False, description="string          Filter remotes by type")



class ObscureOptions(BaseModel):
    """Options for the 'rclone obscure' command."""

    pass


