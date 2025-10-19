"""Generated Pydantic models for rclone commands."""
# AUTO-GENERATED - DO NOT EDIT

from pydantic import BaseModel, Field


class CheckOptions(BaseModel):
    """Options for the 'rclone check' command."""

    flag: bool = Field(False, description="--checkfile string        Treat source:path as a SUM file with hashes of given type")
    combined: bool = Field(False, description="string         Make a combined report of changes to this file")
    differ: bool = Field(False, description="string           Report all non-matching files to this file")
    download: bool = Field(False, description="Check by downloading rather than with hash")
    error: bool = Field(False, description="string            Report all files with errors (hashing or reading) to this file")
    match: bool = Field(False, description="string            Report all matching files to this file")
    missing_on_dst: bool = Field(False, description="string   Report all files missing from the destination to this file")
    missing_on_src: bool = Field(False, description="string   Report all files missing from the source to this file")
    one_way: bool = Field(False, description="Check one way only, source files must exist on remote")



class ChecksumOptions(BaseModel):
    """Options for the 'rclone checksum' command."""

    combined: bool = Field(False, description="string         Make a combined report of changes to this file")
    differ: bool = Field(False, description="string           Report all non-matching files to this file")
    download: bool = Field(False, description="Check by hashing the contents")
    error: bool = Field(False, description="string            Report all files with errors (hashing or reading) to this file")
    match: bool = Field(False, description="string            Report all matching files to this file")
    missing_on_dst: bool = Field(False, description="string   Report all files missing from the destination to this file")
    missing_on_src: bool = Field(False, description="string   Report all files missing from the source to this file")
    one_way: bool = Field(False, description="Check one way only, source files must exist on remote")



class CryptcheckOptions(BaseModel):
    """Options for the 'rclone cryptcheck' command."""

    combined: bool = Field(False, description="string         Make a combined report of changes to this file")
    differ: bool = Field(False, description="string           Report all non-matching files to this file")
    error: bool = Field(False, description="string            Report all files with errors (hashing or reading) to this file")
    match: bool = Field(False, description="string            Report all matching files to this file")
    missing_on_dst: bool = Field(False, description="string   Report all files missing from the destination to this file")
    missing_on_src: bool = Field(False, description="string   Report all files missing from the source to this file")
    one_way: bool = Field(False, description="Check one way only, source files must exist on remote")



class HashsumOptions(BaseModel):
    """Options for the 'rclone hashsum' command."""

    base64: bool = Field(False, description="Output base64 encoded hashsum")
    flag: bool = Field(False, description="--checkfile string     Validate hashes against a given SUM file instead of printing them")
    download: bool = Field(False, description="Download the file and hash it locally; if this flag is not specified, the hash is requested from the remote")
    output_file: bool = Field(False, description="string   Output hashsums to a file rather than the terminal")



class Md5sumOptions(BaseModel):
    """Options for the 'rclone md5sum' command."""

    base64: bool = Field(False, description="Output base64 encoded hashsum")
    flag: bool = Field(False, description="--checkfile string     Validate hashes against a given SUM file instead of printing them")
    download: bool = Field(False, description="Download the file and hash it locally; if this flag is not specified, the hash is requested from the remote")
    output_file: bool = Field(False, description="string   Output hashsums to a file rather than the terminal")



class Sha1sumOptions(BaseModel):
    """Options for the 'rclone sha1sum' command."""

    base64: bool = Field(False, description="Output base64 encoded hashsum")
    flag: bool = Field(False, description="--checkfile string     Validate hashes against a given SUM file instead of printing them")
    download: bool = Field(False, description="Download the file and hash it locally; if this flag is not specified, the hash is requested from the remote")
    output_file: bool = Field(False, description="string   Output hashsums to a file rather than the terminal")


