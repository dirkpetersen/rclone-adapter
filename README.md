# rclone-adapter

[![PyPI](https://img.shields.io/pypi/v/rclone-adapter.svg)](https://pypi.org/project/rclone-adapter/)
[![Downloads](https://img.shields.io/pypi/dm/rclone-adapter.svg)](https://pypi.org/project/rclone-adapter/)
[![License](https://img.shields.io/github/license/dirkpetersen/rclone-adapter)](https://raw.githubusercontent.com/dirkpetersen/rclone-adapter/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/rclone-adapter.svg)](https://pypi.org/project/rclone-adapter/)
[![Build Status](https://github.com/dirkpetersen/rclone-adapter/workflows/Test/badge.svg)](https://github.com/dirkpetersen/rclone-adapter/actions)

A modern, async-first Python wrapper for [rclone](https://rclone.org/) with comprehensive type hints, progress tracking, and structured logging.

## Overview

**rclone-adapter** provides a Pythonic, async-first interface to rclone for cloud storage operations. Instead of running shell commands, you can use intuitive Python methods and async/await patterns to interact with cloud storage providers.

### Key Features

- **🚀 Async-First Design**: Full async/await support with AsyncIterator for streaming progress
- **📦 Bundled rclone**: Latest rclone binary included in wheels for all platforms
- **🎯 Type Safe**: Comprehensive type hints for IDE autocomplete and type checking
- **📊 Progress Tracking**: Real-time progress events with adaptive interval throttling
- **🔧 Full Command Support**: All 54 rclone subcommands with auto-generated type-safe options
- **📝 Structured Logging**: Built-in structured logging with structlog
- **🌈 Pretty Output**: Terminal-friendly progress bars and formatted output with rich
- **⚙️ Flexible Configuration**: Support for environment variables and rclone config files
- **🎓 Well Documented**: Comprehensive CLAUDE.md guide for developers

## Installation

```bash
pip install rclone-adapter
```

### Platform-Specific Details

**Linux (x86_64, ARM64)**:
- Wheels include bundled rclone binaries - no separate installation needed
- `pip install rclone-adapter` is all you need!

**macOS, Windows**:
- Source distribution (`sdist`) available, but no pre-built wheels yet
- Install rclone separately: https://rclone.org/install/
- Then: `pip install rclone-adapter`

**Using system rclone (any platform)**:
- If you prefer your system's rclone installation, it will be used automatically
- The bundled binary is used as a fallback if system rclone is not found

## Supported Python Versions

- Python 3.10, 3.11, 3.12, 3.13, 3.14+

## Quick Start

### Async Usage (Recommended)

```python
import asyncio
from rclone import RClone, RCloneConfig

async def main():
    # Create config (uses bundled rclone binary automatically)
    config = RCloneConfig(
        env_vars={
            "RCLONE_S3_PROVIDER": "AWS",
            "RCLONE_S3_REGION": "us-west-2",
        }
    )

    # Initialize client
    rc = RClone(config)

    # Simple API - returns only final result
    result = await rc.sync(source="/local/path", dest="s3:mybucket/path")
    print(f"Transferred: {result.files_transferred} files ({result.bytes_transferred} bytes)")

    # Streaming API - get real-time progress events
    async for event in rc.sync_stream(source="/local", dest="s3:mybucket/"):
        if hasattr(event, 'progress'):
            print(f"Progress: {event.progress:.1%}")
        elif hasattr(event, 'message'):
            print(f"Info: {event.message}")

asyncio.run(main())
```

### Sync Usage

```python
from rclone import RClone

# For non-async code
rc = RClone()

# Blocking wrapper
result = rc.sync_blocking(
    source="/local/path",
    dest="s3:mybucket/path"
)

if result.success:
    print(f"✓ Success! Transferred {result.files_transferred} files")
else:
    print(f"✗ Failed with {len(result.errors)} errors")
```

## Usage Examples

### Copy with Progress Tracking

```python
import asyncio
from rclone import RClone, ProgressEvent, ErrorEvent

async def copy_with_progress():
    rc = RClone()

    async for event in rc.copy_stream(
        source="/source/path",
        dest="/dest/path"
    ):
        if isinstance(event, ProgressEvent):
            print(f"Progress: {event.bytes_transferred:,} / {event.total_bytes:,} bytes")
        elif isinstance(event, ErrorEvent):
            print(f"Error: {event.message}")

asyncio.run(copy_with_progress())
```

### Using Environment Variables

```python
from rclone import RClone, RCloneConfig

config = RCloneConfig(
    env_vars={
        "RCLONE_S3_PROVIDER": "AWS",
        "RCLONE_S3_ACCESS_KEY_ID": "your-key",
        "RCLONE_S3_SECRET_ACCESS_KEY": "your-secret",
    }
)

rc = RClone(config)
result = await rc.sync(source="s3:bucket1/", dest="s3:bucket2/")
```

### Using rclone Config File

```python
from pathlib import Path
from rclone import RClone, RCloneConfig

config = RCloneConfig(
    config_file=Path("~/.config/rclone/rclone.conf")
)

rc = RClone(config)
result = await rc.sync(source="gdrive:/", dest="/local/backup/")
```

## Architecture

### Core Design

- **Async-First**: All main operations are async-first with sync wrappers available
- **Event Streaming**: Operations yield events for progress, errors, and completion
- **Type Safe**: Pydantic v2 for configuration validation, dataclass models for results
- **Modular**: Separate modules for client, models, process management, and parsing

### Bundled Binary

The wheels include platform-specific rclone binaries:
- Linux x86_64, ARM64
- macOS Intel, Apple Silicon
- Windows x86_64

The `find_rclone_binary()` utility automatically selects the correct binary for your platform.

### Generated Command Options

All 54 rclone subcommands are supported with auto-generated Pydantic models:
- `SyncOptions`, `CopyOptions`, `MoveOptions` - File transfer operations
- `LsOptions`, `LsdOptions`, `LsjsonOptions` - Listing operations
- `CheckOptions`, `ChecksumOptions` - Verification operations
- And more!

## Development

### Setting Up Development Environment

```bash
# Clone and install in editable mode
git clone https://github.com/dirkpetersen/rclone-adapter.git
cd rclone-adapter

# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run linting
ruff check rclone/ tests/
mypy rclone/ --strict
```

### Project Structure

```
rclone-adapter/
├── rclone/
│   ├── __init__.py          # Main package exports
│   ├── client.py            # RClone async client
│   ├── models.py            # Pydantic models (config, events, results)
│   ├── process.py           # Subprocess management
│   ├── parser.py            # rclone log parsing
│   ├── util.py              # Utility functions
│   ├── exceptions.py        # Exception hierarchy
│   ├── py.typed             # PEP 561 marker for type hints
│   ├── bin/                 # Platform-specific rclone binaries
│   └── _generated/          # Auto-generated command options
├── tests/                   # Test suite
├── examples/                # Usage examples
├── CLAUDE.md               # Developer guide
└── README.md               # This file
```

### Running Tests

```bash
# All tests
pytest tests/

# Unit tests only (no integration tests)
pytest tests/ -m "not integration"

# With coverage
pytest tests/ --cov=rclone --cov-report=html

# Specific test file
pytest tests/test_client.py -v
```

## API Reference

### RClone Client

Main async client for rclone operations.

```python
class RClone:
    async def sync(
        source: str,
        dest: str,
        options: SyncOptions | None = None
    ) -> SyncResult

    async def sync_stream(
        source: str,
        dest: str,
        options: SyncOptions | None = None
    ) -> AsyncIterator[ProgressEvent | ErrorEvent | SyncResult]

    def sync_blocking(
        source: str,
        dest: str,
        options: SyncOptions | None = None
    ) -> SyncResult

    # Similar methods for: copy, move, ls, lsd, check, etc.
```

### RCloneConfig

Configuration for the client with validation.

```python
config = RCloneConfig(
    config_file=Path("~/.config/rclone/rclone.conf"),  # Optional
    env_vars={                                           # Optional
        "RCLONE_S3_PROVIDER": "AWS",
        "RCLONE_S3_REGION": "us-west-2",
    },
    rclone_path="/usr/bin/rclone",  # Optional, auto-detected
    log_level="INFO",                # Optional
)
```

### Events

Operations yield typed events for progress and errors:

```python
class ProgressEvent:
    bytes_transferred: int
    total_bytes: int
    progress: float  # 0.0 to 1.0
    transfer_rate: int  # bytes/sec
    eta_seconds: Optional[int]
    current_file: Optional[str]

class ErrorEvent:
    message: str
    file: Optional[str]
    error_category: str  # "network", "permission", "not_found", etc.
    is_retryable: bool
```

### Results

Operations return typed result objects:

```python
class SyncResult:
    success: bool
    return_code: int
    bytes_transferred: int
    files_transferred: int
    errors: list[ErrorEvent]
    duration_seconds: float
    stats: dict  # Full rclone stats
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Run linting and type checking:
   ```bash
   ruff check --fix rclone/ tests/
   mypy rclone/ --strict
   pytest tests/
   ```
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

See [CLAUDE.md](CLAUDE.md) for detailed development guidance.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/dirkpetersen/rclone-adapter/issues)
- **Discussions**: [GitHub Discussions](https://github.com/dirkpetersen/rclone-adapter/discussions)
- **rclone Documentation**: [rclone.org](https://rclone.org/)

## Related Projects

- [rclone](https://github.com/rclone/rclone) - The main rclone project
- [python-pwalk](https://github.com/dirkpetersen/python-pwalk) - Modern Python packaging template
- [froster](https://github.com/dirkpetersen/froster) - Previous rclone wrapper (being replaced)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history and version changes.

---

**Status**: Alpha (0.1.0) - API is stable but may receive enhancements before 1.0 release.

**Latest Release**: [v0.1.0](https://github.com/dirkpetersen/rclone-adapter/releases/tag/v0.1.0) (2025-10-19)
- Initial public release on PyPI
- Full async/await support
- All 54 rclone subcommands
- Linux wheels with bundled rclone binaries
- Comprehensive test suite and CI/CD
