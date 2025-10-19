"""Generated Pydantic models for rclone commands."""
# AUTO-GENERATED - DO NOT EDIT

from pydantic import BaseModel, Field


class MountOptions(BaseModel):
    """Options for the 'rclone mount' command."""

    allow_non_empty: bool = Field(False, description="Allow mounting over a non-empty directory (not supported on Windows)")
    allow_other: bool = Field(False, description="Allow access to other users (not supported on Windows)")
    allow_root: bool = Field(False, description="Allow access to root user (not supported on Windows)")
    async_read: bool = Field(False, description="Use asynchronous reads (not supported on Windows) (default true)")
    daemon: bool = Field(False, description="Run mount in background and exit parent process (as background output is suppressed, use --log-file with --log-format=pid,... to monitor) (not supported on Windows)")
    debug_fuse: bool = Field(False, description="Debug the FUSE internals - needs -v")
    default_permissions: bool = Field(False, description="Makes kernel enforce access control based on the file mode (not supported on Windows)")
    devname: bool = Field(False, description="string                         Set the device name - default is remote:path")
    dir_perms: bool = Field(False, description="FileMode                     Directory permissions (default 777)")
    direct_io: bool = Field(False, description="Use Direct IO, disables caching of data")
    file_perms: bool = Field(False, description="FileMode                    File permissions (default 666)")
    fuse_flag: bool = Field(False, description="stringArray                  Flags or arguments to be passed direct to libfuse/WinFsp (repeat if required)")
    gid: bool = Field(False, description="uint32                             Override the gid field set by the filesystem (not supported on Windows) (default 1000)")
    link_perms: bool = Field(False, description="FileMode                    Link permissions (default 666)")
    mount_case_insensitive: bool = Field(False, description="Tristate        Tell the OS the mount is case insensitive (true) or sensitive (false) regardless of the backend (auto) (default unset)")
    network_mode: bool = Field(False, description="Mount as remote network drive, instead of fixed disk drive (supported on Windows only)")
    no_checksum: bool = Field(False, description="Don't compare checksums on up/download")
    no_seek: bool = Field(False, description="Don't allow seeking in files")
    noappledouble: bool = Field(False, description="Ignore Apple Double (._) and .DS_Store files (supported on OSX only) (default true)")
    noapplexattr: bool = Field(False, description="Ignore all \"com.apple.*\" extended attributes (supported on OSX only)")
    flag: bool = Field(False, description="--option stringArray                     Option for libfuse/WinFsp (repeat if required)")
    read_only: bool = Field(False, description="Only allow read-only access")
    uid: bool = Field(False, description="uint32                             Override the uid field set by the filesystem (not supported on Windows) (default 1000)")
    umask: bool = Field(False, description="FileMode                         Override the permission bits set by the filesystem (not supported on Windows) (default 022)")
    vfs_block_norm_dupes: bool = Field(False, description="If duplicate filenames exist in the same directory (after normalization), log an error and hide the duplicates (may have a performance cost)")
    vfs_cache_mode: bool = Field(False, description="CacheMode               Cache mode off|minimal|writes|full (default off)")
    vfs_case_insensitive: bool = Field(False, description="If a file name not found, find a case insensitive match")
    vfs_fast_fingerprint: bool = Field(False, description="Use fast (less accurate) fingerprints for change detection")
    vfs_links: bool = Field(False, description="Translate symlinks to/from regular files with a '.rclonelink' extension for the VFS")
    vfs_metadata_extension: bool = Field(False, description="string          Set the extension to read metadata from")
    vfs_refresh: bool = Field(False, description="Refreshes the directory cache recursively in the background on start")
    volname: bool = Field(False, description="string                         Set the volume name (supported on Windows and OSX only)")
    write_back_cache: bool = Field(False, description="Makes kernel buffer writes before sending them to rclone (without this, writethrough caching is used) (not supported on Windows)")
    attr_timeout: float | None = Field(0.0, description="Duration                  Time for which file/directory attributes are cached (default 1s)")
    daemon_timeout: float | None = Field(0.0, description="Duration                Time limit for rclone to respond to kernel (not supported on Windows) (default 0s)")
    daemon_wait: float | None = Field(0.0, description="Duration                   Time to wait for ready mount from daemon (maximum time on Linux, constant sleep time on OSX/BSD) (not supported on Windows) (default 1m0s)")
    dir_cache_time: float | None = Field(0.0, description="Duration                Time to cache directory entries for (default 5m0s)")
    max_read_ahead: int | None = Field(0, description="SizeSuffix              The number of bytes that can be prefetched for sequential reads (not supported on Windows) (default 128Ki)")
    no_modtime: float | None = Field(0.0, description="Don't read/write the modification time (can speed things up)")
    poll_interval: float | None = Field(0.0, description="Duration                 Time to wait between polling for changes, must be smaller than dir-cache-time and only on supported remotes (set 0 to disable) (default 1m0s)")
    vfs_cache_max_age: float | None = Field(0.0, description="Duration             Max time since last access of objects in the cache (default 1h0m0s)")
    vfs_cache_max_size: int | None = Field(0, description="SizeSuffix          Max total size of objects in the cache (default off)")
    vfs_cache_min_free_space: int | None = Field(0, description="SizeSuffix    Target minimum free space on the disk containing the cache (default off)")
    vfs_cache_poll_interval: int | None = Field(0, description="Duration       Interval to poll the cache for stale objects (default 1m0s)")
    vfs_disk_space_total_size: int | None = Field(0, description="SizeSuffix   Specify the total space of disk (default off)")
    vfs_read_ahead: int | None = Field(0, description="SizeSuffix              Extra read ahead over --buffer-size when using cache-mode full")
    vfs_read_chunk_size: int | None = Field(0, description="SizeSuffix         Read the source objects in chunks (default 128Mi)")
    vfs_read_chunk_size_limit: int | None = Field(0, description="SizeSuffix   If greater than --vfs-read-chunk-size, double the chunk size after each chunk read, until the limit is reached ('off' is unlimited) (default off)")
    vfs_read_chunk_streams: int | None = Field(0, description="int             The number of parallel streams to read at once")
    vfs_read_wait: float | None = Field(0.0, description="Duration                 Time to wait for in-sequence read before seeking (default 20ms)")
    vfs_used_is_size: int | None = Field(0, description="rclone size           Use the rclone size algorithm for Used size")
    vfs_write_back: float | None = Field(0.0, description="Duration                Time to writeback files after last use when using cache (default 5s)")
    vfs_write_wait: float | None = Field(0.0, description="Duration                Time to wait for in-sequence write before giving error (default 1s)")



class NfsmountOptions(BaseModel):
    """Options for the 'rclone nfsmount' command."""

    addr: bool = Field(False, description="string                            IPaddress:Port or :Port to bind server to")
    allow_non_empty: bool = Field(False, description="Allow mounting over a non-empty directory (not supported on Windows)")
    allow_other: bool = Field(False, description="Allow access to other users (not supported on Windows)")
    allow_root: bool = Field(False, description="Allow access to root user (not supported on Windows)")
    async_read: bool = Field(False, description="Use asynchronous reads (not supported on Windows) (default true)")
    daemon: bool = Field(False, description="Run mount in background and exit parent process (as background output is suppressed, use --log-file with --log-format=pid,... to monitor) (not supported on Windows)")
    debug_fuse: bool = Field(False, description="Debug the FUSE internals - needs -v")
    default_permissions: bool = Field(False, description="Makes kernel enforce access control based on the file mode (not supported on Windows)")
    devname: bool = Field(False, description="string                         Set the device name - default is remote:path")
    dir_perms: bool = Field(False, description="FileMode                     Directory permissions (default 777)")
    direct_io: bool = Field(False, description="Use Direct IO, disables caching of data")
    file_perms: bool = Field(False, description="FileMode                    File permissions (default 666)")
    fuse_flag: bool = Field(False, description="stringArray                  Flags or arguments to be passed direct to libfuse/WinFsp (repeat if required)")
    gid: bool = Field(False, description="uint32                             Override the gid field set by the filesystem (not supported on Windows) (default 1000)")
    link_perms: bool = Field(False, description="FileMode                    Link permissions (default 666)")
    mount_case_insensitive: bool = Field(False, description="Tristate        Tell the OS the mount is case insensitive (true) or sensitive (false) regardless of the backend (auto) (default unset)")
    network_mode: bool = Field(False, description="Mount as remote network drive, instead of fixed disk drive (supported on Windows only)")
    nfs_cache_dir: bool = Field(False, description="string                   The directory the NFS handle cache will use if set")
    nfs_cache_handle_limit: bool = Field(False, description="int             max file handles cached simultaneously (min 5) (default 1000000)")
    nfs_cache_type: bool = Field(False, description="memory|disk|symlink     Type of NFS handle cache to use (default memory)")
    no_checksum: bool = Field(False, description="Don't compare checksums on up/download")
    no_seek: bool = Field(False, description="Don't allow seeking in files")
    noappledouble: bool = Field(False, description="Ignore Apple Double (._) and .DS_Store files (supported on OSX only) (default true)")
    noapplexattr: bool = Field(False, description="Ignore all \"com.apple.*\" extended attributes (supported on OSX only)")
    flag: bool = Field(False, description="--option stringArray                     Option for libfuse/WinFsp (repeat if required)")
    read_only: bool = Field(False, description="Only allow read-only access")
    sudo: bool = Field(False, description="Use sudo to run the mount/umount commands as root.")
    uid: bool = Field(False, description="uint32                             Override the uid field set by the filesystem (not supported on Windows) (default 1000)")
    umask: bool = Field(False, description="FileMode                         Override the permission bits set by the filesystem (not supported on Windows) (default 022)")
    vfs_block_norm_dupes: bool = Field(False, description="If duplicate filenames exist in the same directory (after normalization), log an error and hide the duplicates (may have a performance cost)")
    vfs_cache_mode: bool = Field(False, description="CacheMode               Cache mode off|minimal|writes|full (default off)")
    vfs_case_insensitive: bool = Field(False, description="If a file name not found, find a case insensitive match")
    vfs_fast_fingerprint: bool = Field(False, description="Use fast (less accurate) fingerprints for change detection")
    vfs_links: bool = Field(False, description="Translate symlinks to/from regular files with a '.rclonelink' extension for the VFS")
    vfs_metadata_extension: bool = Field(False, description="string          Set the extension to read metadata from")
    vfs_refresh: bool = Field(False, description="Refreshes the directory cache recursively in the background on start")
    volname: bool = Field(False, description="string                         Set the volume name (supported on Windows and OSX only)")
    write_back_cache: bool = Field(False, description="Makes kernel buffer writes before sending them to rclone (without this, writethrough caching is used) (not supported on Windows)")
    attr_timeout: float | None = Field(0.0, description="Duration                  Time for which file/directory attributes are cached (default 1s)")
    daemon_timeout: float | None = Field(0.0, description="Duration                Time limit for rclone to respond to kernel (not supported on Windows) (default 0s)")
    daemon_wait: float | None = Field(0.0, description="Duration                   Time to wait for ready mount from daemon (maximum time on Linux, constant sleep time on OSX/BSD) (not supported on Windows) (default 1m0s)")
    dir_cache_time: float | None = Field(0.0, description="Duration                Time to cache directory entries for (default 5m0s)")
    max_read_ahead: int | None = Field(0, description="SizeSuffix              The number of bytes that can be prefetched for sequential reads (not supported on Windows) (default 128Ki)")
    no_modtime: float | None = Field(0.0, description="Don't read/write the modification time (can speed things up)")
    poll_interval: float | None = Field(0.0, description="Duration                 Time to wait between polling for changes, must be smaller than dir-cache-time and only on supported remotes (set 0 to disable) (default 1m0s)")
    vfs_cache_max_age: float | None = Field(0.0, description="Duration             Max time since last access of objects in the cache (default 1h0m0s)")
    vfs_cache_max_size: int | None = Field(0, description="SizeSuffix          Max total size of objects in the cache (default off)")
    vfs_cache_min_free_space: int | None = Field(0, description="SizeSuffix    Target minimum free space on the disk containing the cache (default off)")
    vfs_cache_poll_interval: int | None = Field(0, description="Duration       Interval to poll the cache for stale objects (default 1m0s)")
    vfs_disk_space_total_size: int | None = Field(0, description="SizeSuffix   Specify the total space of disk (default off)")
    vfs_read_ahead: int | None = Field(0, description="SizeSuffix              Extra read ahead over --buffer-size when using cache-mode full")
    vfs_read_chunk_size: int | None = Field(0, description="SizeSuffix         Read the source objects in chunks (default 128Mi)")
    vfs_read_chunk_size_limit: int | None = Field(0, description="SizeSuffix   If greater than --vfs-read-chunk-size, double the chunk size after each chunk read, until the limit is reached ('off' is unlimited) (default off)")
    vfs_read_chunk_streams: int | None = Field(0, description="int             The number of parallel streams to read at once")
    vfs_read_wait: float | None = Field(0.0, description="Duration                 Time to wait for in-sequence read before seeking (default 20ms)")
    vfs_used_is_size: int | None = Field(0, description="rclone size           Use the rclone size algorithm for Used size")
    vfs_write_back: float | None = Field(0.0, description="Duration                Time to writeback files after last use when using cache (default 5s)")
    vfs_write_wait: float | None = Field(0.0, description="Duration                Time to wait for in-sequence write before giving error (default 1s)")



class RcdOptions(BaseModel):
    """Options for the 'rclone rcd' command."""

    pass



class ServeOptions(BaseModel):
    """Options for the 'rclone serve' command."""

    pass


