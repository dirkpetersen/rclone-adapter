"""Generated Pydantic models for rclone commands."""
# AUTO-GENERATED - DO NOT EDIT

from pydantic import BaseModel, Field


class AboutOptions(BaseModel):
    """Options for the 'rclone about' command."""

    json: bool = Field(False, description="Format output as JSON")
    full: int | None = Field(0, description="Full numbers instead of human-readable")



class BackendOptions(BaseModel):
    """Options for the 'rclone backend' command."""

    json: bool = Field(False, description="Always output in JSON format")
    flag: bool = Field(False, description="--option stringArray   Option in the form name=value or name")



class CatOptions(BaseModel):
    """Options for the 'rclone cat' command."""

    count: bool = Field(False, description="int          Only print N characters (default -1)")
    discard: bool = Field(False, description="Discard the output instead of printing")
    head: bool = Field(False, description="int           Only print the first N characters")
    offset: bool = Field(False, description="int         Start printing at offset N (or from end if -ve)")
    separator: bool = Field(False, description="string   Separator to use between objects when printing multiple files")
    tail: bool = Field(False, description="int           Only print the last N characters")



class CleanupOptions(BaseModel):
    """Options for the 'rclone cleanup' command."""

    pass



class CompletionOptions(BaseModel):
    """Options for the 'rclone completion' command."""

    pass



class ConvmvOptions(BaseModel):
    """Options for the 'rclone convmv' command."""

    create_empty_src_dirs: bool = Field(False, description="Create empty source dirs on destination after move")
    delete_empty_src_dirs: bool = Field(False, description="Delete empty source dirs after move")



class CopyurlOptions(BaseModel):
    """Options for the 'rclone copyurl' command."""

    flag: bool = Field(False, description="--auto-filename     Get the file name from the URL and use it for destination file path")
    header_filename: bool = Field(False, description="Get the file name from the Content-Disposition header")
    no_clobber: bool = Field(False, description="Prevent overwriting file with same name")
    flag: bool = Field(False, description="--print-filename    Print the resulting name from --auto-filename")
    stdout: bool = Field(False, description="Write the output to stdout rather than a file")



class CryptdecodeOptions(BaseModel):
    """Options for the 'rclone cryptdecode' command."""

    reverse: bool = Field(False, description="Reverse cryptdecode, encrypts filenames")



class DedupeOptions(BaseModel):
    """Options for the 'rclone dedupe' command."""

    by_hash: bool = Field(False, description="Find identical hashes rather than names")
    dedupe_mode: bool = Field(False, description="string   Dedupe mode interactive|skip|first|newest|oldest|largest|smallest|rename (default \"interactive\")")



class DeleteOptions(BaseModel):
    """Options for the 'rclone delete' command."""

    rmdirs: bool = Field(False, description="rmdirs removes empty directories but leaves root intact")



class DeletefileOptions(BaseModel):
    """Options for the 'rclone deletefile' command."""

    pass



class GendocsOptions(BaseModel):
    """Options for the 'rclone gendocs' command."""

    pass



class GitannexOptions(BaseModel):
    """Options for the 'rclone gitannex' command."""

    pass



class HelpOptions(BaseModel):
    """Options for the 'rclone help' command."""

    pass



class LinkOptions(BaseModel):
    """Options for the 'rclone link' command."""

    unlink: bool = Field(False, description="Remove existing public link to file/folder")
    expire: float | None = Field(0.0, description="Duration   The amount of time that the link will be valid (default off)")



class MkdirOptions(BaseModel):
    """Options for the 'rclone mkdir' command."""

    pass



class PurgeOptions(BaseModel):
    """Options for the 'rclone purge' command."""

    pass



class RcOptions(BaseModel):
    """Options for the 'rclone rc' command."""

    flag: bool = Field(False, description="--arg stringArray      Argument placed in the \"arg\" array")
    json: bool = Field(False, description="string          Input JSON - use instead of key=value args")
    loopback: bool = Field(False, description="If set connect to this rclone instance not via HTTP")
    no_output: bool = Field(False, description="If set, don't output the JSON result")
    flag: bool = Field(False, description="--opt stringArray      Option in the form name=value or name placed in the \"opt\" array")
    pass: bool = Field(False, description="string          Password to use to connect to rclone remote control")
    unix_socket: bool = Field(False, description="string   Path to a unix domain socket to dial to, instead of opening a TCP connection directly")
    url: bool = Field(False, description="string           URL to connect to rclone remote control (default \"http://localhost:5572/\")")
    user: bool = Field(False, description="string          Username to use to rclone remote control")



class RcatOptions(BaseModel):
    """Options for the 'rclone rcat' command."""

    size: int | None = Field(0, description="int   File size hint to preallocate (default -1)")



class RmdirOptions(BaseModel):
    """Options for the 'rclone rmdir' command."""

    pass



class RmdirsOptions(BaseModel):
    """Options for the 'rclone rmdirs' command."""

    leave_root: bool = Field(False, description="Do not remove root directory if empty")



class SelfupdateOptions(BaseModel):
    """Options for the 'rclone selfupdate' command."""

    beta: bool = Field(False, description="Install beta release")
    check: bool = Field(False, description="Check for latest release, do not download")
    output: bool = Field(False, description="string    Save the downloaded binary at a given path (default: replace running binary)")
    package: bool = Field(False, description="string   Package format: zip|deb|rpm (default: zip)")
    stable: bool = Field(False, description="Install stable release (this is the default)")
    version: bool = Field(False, description="string   Install the given rclone version (default: latest)")



class SettierOptions(BaseModel):
    """Options for the 'rclone settier' command."""

    pass



class SizeOptions(BaseModel):
    """Options for the 'rclone size' command."""

    json: bool = Field(False, description="Format output as JSON")



class TestOptions(BaseModel):
    """Options for the 'rclone test' command."""

    pass



class TouchOptions(BaseModel):
    """Options for the 'rclone touch' command."""

    flag: bool = Field(False, description="--no-create          Do not create the file if it does not exist (implied with --recursive)")
    flag: bool = Field(False, description="--recursive          Recursively touch all files")
    localtime: float | None = Field(0.0, description="Use localtime for timestamp, not UTC")
    flag: float | None = Field(0.0, description="--timestamp string   Use specified time instead of the current time of day")



class VersionOptions(BaseModel):
    """Options for the 'rclone version' command."""

    check: bool = Field(False, description="Check for new version")
    deps: bool = Field(False, description="Show the Go dependencies")


