"""Generated Pydantic models for rclone commands."""
# AUTO-GENERATED - DO NOT EDIT

from pydantic import BaseModel, Field


class LsOptions(BaseModel):
    """Options for the 'rclone ls' command."""

    pass



class LsdOptions(BaseModel):
    """Options for the 'rclone lsd' command."""

    flag: bool = Field(False, description="--recursive   Recurse into the listing")



class LsfOptions(BaseModel):
    """Options for the 'rclone lsf' command."""

    absolute: bool = Field(False, description="Put a leading / in front of path names")
    csv: bool = Field(False, description="Output in CSV format")
    flag: bool = Field(False, description="--dir-slash            Append a slash to directory names (default true)")
    dirs_only: bool = Field(False, description="Only list directories")
    files_only: bool = Field(False, description="Only list files")
    hash: bool = Field(False, description="h               Use this hash when h is used in the format MD5|SHA-1|DropboxHash (default \"md5\")")
    flag: bool = Field(False, description="--recursive            Recurse into the listing")
    flag: bool = Field(False, description="--separator string     Separator for the items in the format (default \";\")")
    flag: float | None = Field(0.0, description="--time-format string   Specify a custom time format, or 'max' for max precision supported by remote (default: 2006-01-02 15:04:05)")



class LsjsonOptions(BaseModel):
    """Options for the 'rclone lsjson' command."""

    dirs_only: bool = Field(False, description="Show only directories in the listing")
    encrypted: bool = Field(False, description="Show the encrypted names")
    files_only: bool = Field(False, description="Show only files in the listing")
    hash: bool = Field(False, description="Include hashes in the output (may take longer)")
    hash_type: bool = Field(False, description="stringArray   Show only this hash type (may be repeated)")
    flag: bool = Field(False, description="--metadata                Add metadata to the listing")
    no_mimetype: bool = Field(False, description="Don't read the mime type (can speed things up)")
    original: bool = Field(False, description="Show the ID of the underlying Object")
    flag: bool = Field(False, description="--recursive               Recurse into the listing")
    stat: bool = Field(False, description="Just return the info for the pointed to file")
    no_modtime: float | None = Field(0.0, description="Don't read the modification time (can speed things up)")



class LslOptions(BaseModel):
    """Options for the 'rclone lsl' command."""

    pass



class NcduOptions(BaseModel):
    """Options for the 'rclone ncdu' command."""

    pass



class TreeOptions(BaseModel):
    """Options for the 'rclone tree' command."""

    flag: bool = Field(False, description="--all             All files are listed (list . files too)")
    flag: bool = Field(False, description="--dirs-only       List directories only")
    dirsfirst: bool = Field(False, description="List directories before files (-U disables)")
    full_path: bool = Field(False, description="Print the full path prefix for each file")
    level: bool = Field(False, description="int       Descend only level directories deep")
    noindent: bool = Field(False, description="Don't print indentation lines")
    flag: bool = Field(False, description="--output string   Output to file instead of stdout")
    flag: bool = Field(False, description="--protections     Print the protections for each file.")
    flag: bool = Field(False, description="--quote           Quote filenames with double quotes.")
    flag: bool = Field(False, description="--sort-reverse    Reverse the order of the sort")
    flag: bool = Field(False, description="--unsorted        Leave files unsorted")
    version: bool = Field(False, description="Sort files alphanumerically by version")
    flag: int | None = Field(0, description="--modtime         Print the date of last modification.")
    noreport: int | None = Field(0, description="Turn off file/directory count at end of tree listing")
    flag: int | None = Field(0, description="--size            Print the size in bytes of each file.")
    sort: int | None = Field(0, description="string     Select sort: name,version,size,mtime,ctime")
    sort_ctime: float | None = Field(0.0, description="Sort files by last status change time")
    flag: float | None = Field(0.0, description="--sort-modtime    Sort files by last modification time")


