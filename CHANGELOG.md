# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-19

### Added

- Initial public release of rclone-adapter
- **Async-first Python wrapper** for rclone with full async/await support
- **Core client library** with RClone class for all major operations
- **Type-safe API** with comprehensive type hints (PEP 561 compliant)
- **Bundled rclone binaries** in wheels for:
  - Linux: x86_64, ARM64
  - macOS: Intel x86_64, Apple Silicon ARM64
  - Windows: x86_64
- **Progress tracking** with:
  - Real-time event streaming via AsyncIterator
  - Adaptive progress interval throttling
  - Detailed error categorization
- **Full command coverage** for all 54 rclone subcommands with auto-generated options:
  - sync, copy, move, bisync operations
  - Listing commands (ls, lsd, lsl, lsjson, lsf, tree, ncdu)
  - Verification commands (check, checksum, cryptcheck, hashsum, md5sum, sha1sum)
  - Configuration commands (config, authorize, obscure, listremotes)
  - Serve commands (serve, mount, nfsmount, rcd)
  - Utility commands (40+ others)

- **Flexible configuration** supporting:
  - Environment variables (RCLONE_*, AWS_*, AZURE_*, GCS_*, GOOGLE_*)
  - rclone config files
  - Custom rclone executable paths
  - Auto-detection of bundled binary

- **Structured logging** with structlog integration
- **Pretty output** with rich terminal formatting
- **Dual API styles**:
  - Streaming API for real-time progress
  - Simple API for fire-and-forget operations
  - Blocking wrapper for non-async code

- **Comprehensive CI/CD**:
  - GitHub Actions workflows for testing (Python 3.10-3.14)
  - Multi-platform wheel building (Linux, macOS, Windows)
  - Automated PyPI publishing with trusted publishers
  - Automated TestPyPI deployment from main branch

- **Developer-friendly**:
  - CLAUDE.md with comprehensive development guide
  - Well-structured modular architecture
  - Full test suite with pytest
  - Modern Python tooling (ruff, mypy, pytest-asyncio)

### Technical Details

- **Python Support**: 3.10, 3.11, 3.12, 3.13, 3.14+
- **Core Dependencies**:
  - pydantic>=2.0 (data validation)
  - rich>=13.0 (terminal output)
  - structlog>=24.0 (structured logging)
- **Optional Dependencies** [api]:
  - fastapi>=0.110
  - rq>=1.16 (Redis Queue)
  - redis>=5.0
  - uvicorn>=0.27

### Architecture Highlights

- **Async subprocess management** with graceful shutdown and command-specific grace periods
- **JSON-based log parsing** from rclone's `--use-json-log` output
- **Dynamic command discovery** from rclone help text (generate.py)
- **importlib.resources** for robust bundled binary access across installation types
- **Pydantic v2** for all data models and validation
- **Event-driven architecture** for long-running operations

### Known Limitations

- API module (FastAPI/RQ integration) not yet implemented (planned for 0.2.0)
- Integration tests require rclone installed on system
- Some advanced rclone options may need documentation improvements

### Future Roadmap

- **0.2.0**: FastAPI + RQ integration for long-running jobs
- **0.3.0**: Enhanced progress tracking and resumable transfers
- **0.4.0**: Mount operations with FUSE support
- **1.0.0**: Stable API with full documentation

---

For detailed development information, see [CLAUDE.md](CLAUDE.md).
For usage examples, see [README.md](README.md).
