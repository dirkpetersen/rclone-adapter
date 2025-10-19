"""Generated Pydantic models for rclone commands."""
# AUTO-GENERATED - DO NOT EDIT

from typing import TYPE_CHECKING, Type

from pydantic import BaseModel

if TYPE_CHECKING:
    from .check_commands import (
        CheckOptions,
        ChecksumOptions,
        CryptcheckOptions,
        HashsumOptions,
        Md5sumOptions,
        Sha1sumOptions,
    )
    from .config_commands import AuthorizeOptions, ConfigOptions, ListremotesOptions, ObscureOptions
    from .listing_commands import (
        LsdOptions,
        LsfOptions,
        LsjsonOptions,
        LslOptions,
        LsOptions,
        NcduOptions,
        TreeOptions,
    )
    from .serve_commands import MountOptions, NfsmountOptions, RcdOptions, ServeOptions
    from .sync_commands import (
        BisyncOptions,
        CopyOptions,
        CopytoOptions,
        MoveOptions,
        MovetoOptions,
        SyncOptions,
    )
    from .utility_commands import (
        AboutOptions,
        BackendOptions,
        CatOptions,
        CleanupOptions,
        CompletionOptions,
        ConvmvOptions,
        CopyurlOptions,
        CryptdecodeOptions,
        DedupeOptions,
        DeletefileOptions,
        DeleteOptions,
        GendocsOptions,
        GitannexOptions,
        HelpOptions,
        LinkOptions,
        MkdirOptions,
        PurgeOptions,
        RcatOptions,
        RcOptions,
        RmdirOptions,
        RmdirsOptions,
        SelfupdateOptions,
        SettierOptions,
        SizeOptions,
        TestOptions,
        TouchOptions,
        VersionOptions,
    )


def get_command_options(command: str) -> type[BaseModel] | None:
    """Lazy load command options only when needed."""
    if command == "bisync":
        from .sync_commands import BisyncOptions
        return BisyncOptions
    if command == "copy":
        from .sync_commands import CopyOptions
        return CopyOptions
    if command == "copyto":
        from .sync_commands import CopytoOptions
        return CopytoOptions
    if command == "move":
        from .sync_commands import MoveOptions
        return MoveOptions
    if command == "moveto":
        from .sync_commands import MovetoOptions
        return MovetoOptions
    if command == "sync":
        from .sync_commands import SyncOptions
        return SyncOptions
    if command == "ls":
        from .listing_commands import LsOptions
        return LsOptions
    if command == "lsd":
        from .listing_commands import LsdOptions
        return LsdOptions
    if command == "lsf":
        from .listing_commands import LsfOptions
        return LsfOptions
    if command == "lsjson":
        from .listing_commands import LsjsonOptions
        return LsjsonOptions
    if command == "lsl":
        from .listing_commands import LslOptions
        return LslOptions
    if command == "ncdu":
        from .listing_commands import NcduOptions
        return NcduOptions
    if command == "tree":
        from .listing_commands import TreeOptions
        return TreeOptions
    if command == "check":
        from .check_commands import CheckOptions
        return CheckOptions
    if command == "checksum":
        from .check_commands import ChecksumOptions
        return ChecksumOptions
    if command == "cryptcheck":
        from .check_commands import CryptcheckOptions
        return CryptcheckOptions
    if command == "hashsum":
        from .check_commands import HashsumOptions
        return HashsumOptions
    if command == "md5sum":
        from .check_commands import Md5sumOptions
        return Md5sumOptions
    if command == "sha1sum":
        from .check_commands import Sha1sumOptions
        return Sha1sumOptions
    if command == "authorize":
        from .config_commands import AuthorizeOptions
        return AuthorizeOptions
    if command == "config":
        from .config_commands import ConfigOptions
        return ConfigOptions
    if command == "listremotes":
        from .config_commands import ListremotesOptions
        return ListremotesOptions
    if command == "obscure":
        from .config_commands import ObscureOptions
        return ObscureOptions
    if command == "mount":
        from .serve_commands import MountOptions
        return MountOptions
    if command == "nfsmount":
        from .serve_commands import NfsmountOptions
        return NfsmountOptions
    if command == "rcd":
        from .serve_commands import RcdOptions
        return RcdOptions
    if command == "serve":
        from .serve_commands import ServeOptions
        return ServeOptions
    if command == "about":
        from .utility_commands import AboutOptions
        return AboutOptions
    if command == "backend":
        from .utility_commands import BackendOptions
        return BackendOptions
    if command == "cat":
        from .utility_commands import CatOptions
        return CatOptions
    if command == "cleanup":
        from .utility_commands import CleanupOptions
        return CleanupOptions
    if command == "completion":
        from .utility_commands import CompletionOptions
        return CompletionOptions
    if command == "convmv":
        from .utility_commands import ConvmvOptions
        return ConvmvOptions
    if command == "copyurl":
        from .utility_commands import CopyurlOptions
        return CopyurlOptions
    if command == "cryptdecode":
        from .utility_commands import CryptdecodeOptions
        return CryptdecodeOptions
    if command == "dedupe":
        from .utility_commands import DedupeOptions
        return DedupeOptions
    if command == "delete":
        from .utility_commands import DeleteOptions
        return DeleteOptions
    if command == "deletefile":
        from .utility_commands import DeletefileOptions
        return DeletefileOptions
    if command == "gendocs":
        from .utility_commands import GendocsOptions
        return GendocsOptions
    if command == "gitannex":
        from .utility_commands import GitannexOptions
        return GitannexOptions
    if command == "help":
        from .utility_commands import HelpOptions
        return HelpOptions
    if command == "link":
        from .utility_commands import LinkOptions
        return LinkOptions
    if command == "mkdir":
        from .utility_commands import MkdirOptions
        return MkdirOptions
    if command == "purge":
        from .utility_commands import PurgeOptions
        return PurgeOptions
    if command == "rc":
        from .utility_commands import RcOptions
        return RcOptions
    if command == "rcat":
        from .utility_commands import RcatOptions
        return RcatOptions
    if command == "rmdir":
        from .utility_commands import RmdirOptions
        return RmdirOptions
    if command == "rmdirs":
        from .utility_commands import RmdirsOptions
        return RmdirsOptions
    if command == "selfupdate":
        from .utility_commands import SelfupdateOptions
        return SelfupdateOptions
    if command == "settier":
        from .utility_commands import SettierOptions
        return SettierOptions
    if command == "size":
        from .utility_commands import SizeOptions
        return SizeOptions
    if command == "test":
        from .utility_commands import TestOptions
        return TestOptions
    if command == "touch":
        from .utility_commands import TouchOptions
        return TouchOptions
    if command == "version":
        from .utility_commands import VersionOptions
        return VersionOptions
    return None
