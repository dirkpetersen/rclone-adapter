"""Generated Pydantic models for rclone commands."""
# AUTO-GENERATED - DO NOT EDIT

from pydantic import BaseModel, Field


class BisyncOptions(BaseModel):
    """Options for the 'rclone bisync' command."""

    backup_dir1: bool = Field(False, description="string                   --backup-dir for Path1. Must be a non-overlapping path on the same remote.")
    backup_dir2: bool = Field(False, description="string                   --backup-dir for Path2. Must be a non-overlapping path on the same remote.")
    check_access: bool = Field(False, description="Ensure expected RCLONE_TEST files are found on both Path1 and Path2 filesystems, else abort.")
    check_filename: bool = Field(False, description="string                Filename for --check-access (default: RCLONE_TEST)")
    check_sync: bool = Field(False, description="string                    Controls comparison of final listings: true|false|only (default: true) (default \"true\")")
    conflict_loser: bool = Field(False, description="ConflictLoserAction   Action to take on the loser of a sync conflict (when there is a winner) or on both files (when there is no winner): , num, pathname, delete (default: num)")
    conflict_resolve: bool = Field(False, description="string              Automatically resolve conflicts by preferring the version that is: none, path1, path2, newer, older, larger, smaller (default: none) (default \"none\")")
    conflict_suffix: bool = Field(False, description="string               Suffix to use when renaming a --conflict-loser. Can be either one string or two comma-separated strings to assign different suffixes to Path1/Path2. (default: 'conflict')")
    create_empty_src_dirs: bool = Field(False, description="Sync creation and deletion of empty directories. (Not compatible with --remove-empty-dirs)")
    download_hash: bool = Field(False, description="Compute hash by downloading when otherwise unavailable. (warning: may be slow and use lots of data!)")
    filters_file: bool = Field(False, description="string                  Read filtering patterns from a file")
    force: bool = Field(False, description="Bypass --max-delete safety check and run the sync. Consider using with --verbose")
    ignore_listing_checksum: bool = Field(False, description="Do not use checksums for listings (add --ignore-checksum to additionally skip post-copy checksum checks)")
    no_cleanup: bool = Field(False, description="Retain working files (useful for troubleshooting and testing).")
    no_slow_hash: bool = Field(False, description="Ignore listing checksums only on backends where they are slow")
    recover: bool = Field(False, description="Automatically recover from interruptions without requiring --resync.")
    remove_empty_dirs: bool = Field(False, description="Remove ALL empty directories at the final cleanup step.")
    resilient: bool = Field(False, description="Allow future runs to retry after certain less-serious errors, instead of requiring --resync.")
    flag: bool = Field(False, description="--resync                               Performs the resync run. Equivalent to --resync-mode path1. Consider using --verbose or --dry-run first.")
    resync_mode: bool = Field(False, description="string                   During resync, prefer the version that is: path1, path2, newer, older, larger, smaller (default: path1 if --resync, otherwise none for no resync.) (default \"none\")")
    slow_hash_sync_only: bool = Field(False, description="Ignore slow checksums for listings and deltas, but still consider them during sync calls.")
    workdir: bool = Field(False, description="string                       Use custom working dir - useful for testing. (default: {WORKDIR})")
    compare: int | None = Field(0, description="string                       Comma-separated list of bisync-specific compare options ex. 'size,modtime,checksum' (default: 'size,modtime')")
    max_lock: float | None = Field(0.0, description="Duration                    Consider lock files older than this to be expired (default: 0 (never expire)) (minimum: 2m) (default 0s)")



class CopyOptions(BaseModel):
    """Options for the 'rclone copy' command."""

    absolute: bool = Field(False, description="Put a leading / in front of path names")
    combined: bool = Field(False, description="string         Make a combined report of changes to this file")
    create_empty_src_dirs: bool = Field(False, description="Create empty source dirs on destination after copy")
    csv: bool = Field(False, description="Output in CSV format")
    dest_after: bool = Field(False, description="string       Report all files that exist on the dest post-sync")
    differ: bool = Field(False, description="string           Report all non-matching files to this file")
    flag: bool = Field(False, description="--dir-slash               Append a slash to directory names (default true)")
    dirs_only: bool = Field(False, description="Only list directories")
    error: bool = Field(False, description="string            Report all files with errors (hashing or reading) to this file")
    files_only: bool = Field(False, description="Only list files (default true)")
    hash: bool = Field(False, description="h                  Use this hash when h is used in the format MD5|SHA-1|DropboxHash (default \"md5\")")
    match: bool = Field(False, description="string            Report all matching files to this file")
    missing_on_dst: bool = Field(False, description="string   Report all files missing from the destination to this file")
    missing_on_src: bool = Field(False, description="string   Report all files missing from the source to this file")
    flag: bool = Field(False, description="--separator string        Separator for the items in the format (default \";\")")
    flag: float | None = Field(0.0, description="--timeformat string       Specify a custom time format, or 'max' for max precision supported by remote (default: 2006-01-02 15:04:05)")



class CopytoOptions(BaseModel):
    """Options for the 'rclone copyto' command."""

    absolute: bool = Field(False, description="Put a leading / in front of path names")
    combined: bool = Field(False, description="string         Make a combined report of changes to this file")
    csv: bool = Field(False, description="Output in CSV format")
    dest_after: bool = Field(False, description="string       Report all files that exist on the dest post-sync")
    differ: bool = Field(False, description="string           Report all non-matching files to this file")
    flag: bool = Field(False, description="--dir-slash               Append a slash to directory names (default true)")
    dirs_only: bool = Field(False, description="Only list directories")
    error: bool = Field(False, description="string            Report all files with errors (hashing or reading) to this file")
    files_only: bool = Field(False, description="Only list files (default true)")
    hash: bool = Field(False, description="h                  Use this hash when h is used in the format MD5|SHA-1|DropboxHash (default \"md5\")")
    match: bool = Field(False, description="string            Report all matching files to this file")
    missing_on_dst: bool = Field(False, description="string   Report all files missing from the destination to this file")
    missing_on_src: bool = Field(False, description="string   Report all files missing from the source to this file")
    flag: bool = Field(False, description="--separator string        Separator for the items in the format (default \";\")")
    flag: float | None = Field(0.0, description="--timeformat string       Specify a custom time format, or 'max' for max precision supported by remote (default: 2006-01-02 15:04:05)")



class MoveOptions(BaseModel):
    """Options for the 'rclone move' command."""

    absolute: bool = Field(False, description="Put a leading / in front of path names")
    combined: bool = Field(False, description="string         Make a combined report of changes to this file")
    create_empty_src_dirs: bool = Field(False, description="Create empty source dirs on destination after move")
    csv: bool = Field(False, description="Output in CSV format")
    delete_empty_src_dirs: bool = Field(False, description="Delete empty source dirs after move")
    dest_after: bool = Field(False, description="string       Report all files that exist on the dest post-sync")
    differ: bool = Field(False, description="string           Report all non-matching files to this file")
    flag: bool = Field(False, description="--dir-slash               Append a slash to directory names (default true)")
    dirs_only: bool = Field(False, description="Only list directories")
    error: bool = Field(False, description="string            Report all files with errors (hashing or reading) to this file")
    files_only: bool = Field(False, description="Only list files (default true)")
    hash: bool = Field(False, description="h                  Use this hash when h is used in the format MD5|SHA-1|DropboxHash (default \"md5\")")
    match: bool = Field(False, description="string            Report all matching files to this file")
    missing_on_dst: bool = Field(False, description="string   Report all files missing from the destination to this file")
    missing_on_src: bool = Field(False, description="string   Report all files missing from the source to this file")
    flag: bool = Field(False, description="--separator string        Separator for the items in the format (default \";\")")
    flag: float | None = Field(0.0, description="--timeformat string       Specify a custom time format, or 'max' for max precision supported by remote (default: 2006-01-02 15:04:05)")



class MovetoOptions(BaseModel):
    """Options for the 'rclone moveto' command."""

    absolute: bool = Field(False, description="Put a leading / in front of path names")
    combined: bool = Field(False, description="string         Make a combined report of changes to this file")
    csv: bool = Field(False, description="Output in CSV format")
    dest_after: bool = Field(False, description="string       Report all files that exist on the dest post-sync")
    differ: bool = Field(False, description="string           Report all non-matching files to this file")
    flag: bool = Field(False, description="--dir-slash               Append a slash to directory names (default true)")
    dirs_only: bool = Field(False, description="Only list directories")
    error: bool = Field(False, description="string            Report all files with errors (hashing or reading) to this file")
    files_only: bool = Field(False, description="Only list files (default true)")
    hash: bool = Field(False, description="h                  Use this hash when h is used in the format MD5|SHA-1|DropboxHash (default \"md5\")")
    match: bool = Field(False, description="string            Report all matching files to this file")
    missing_on_dst: bool = Field(False, description="string   Report all files missing from the destination to this file")
    missing_on_src: bool = Field(False, description="string   Report all files missing from the source to this file")
    flag: bool = Field(False, description="--separator string        Separator for the items in the format (default \";\")")
    flag: float | None = Field(0.0, description="--timeformat string       Specify a custom time format, or 'max' for max precision supported by remote (default: 2006-01-02 15:04:05)")



class SyncOptions(BaseModel):
    """Options for the 'rclone sync' command."""

    absolute: bool = Field(False, description="Put a leading / in front of path names")
    combined: bool = Field(False, description="string         Make a combined report of changes to this file")
    create_empty_src_dirs: bool = Field(False, description="Create empty source dirs on destination after sync")
    csv: bool = Field(False, description="Output in CSV format")
    dest_after: bool = Field(False, description="string       Report all files that exist on the dest post-sync")
    differ: bool = Field(False, description="string           Report all non-matching files to this file")
    flag: bool = Field(False, description="--dir-slash               Append a slash to directory names (default true)")
    dirs_only: bool = Field(False, description="Only list directories")
    error: bool = Field(False, description="string            Report all files with errors (hashing or reading) to this file")
    files_only: bool = Field(False, description="Only list files (default true)")
    hash: bool = Field(False, description="h                  Use this hash when h is used in the format MD5|SHA-1|DropboxHash (default \"md5\")")
    match: bool = Field(False, description="string            Report all matching files to this file")
    missing_on_dst: bool = Field(False, description="string   Report all files missing from the destination to this file")
    missing_on_src: bool = Field(False, description="string   Report all files missing from the source to this file")
    flag: bool = Field(False, description="--separator string        Separator for the items in the format (default \";\")")
    flag: float | None = Field(0.0, description="--timeformat string       Specify a custom time format, or 'max' for max precision supported by remote (default: 2006-01-02 15:04:05)")


