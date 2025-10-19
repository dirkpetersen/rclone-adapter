# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-10-19

### Added

- **Comprehensive Changelog Maintenance Guide** in CLAUDE.md
  - Detailed release workflow with step-by-step instructions
  - Changelog best practices and format conventions
  - Automated PyPI publishing process documentation
  - Troubleshooting guide for common release issues
  - Semantic versioning guidelines

- **Enhanced Documentation**:
  - CHANGELOG.md with complete v0.1.0 release notes
  - Platform-specific installation instructions in README
  - Development notes on changelog maintenance in CLAUDE.md
  - Release process automation details

### Changed

- Updated README with clearer platform-specific installation guidance
  - Linux wheels include bundled rclone binaries
  - macOS/Windows source distribution approach
  - System rclone fallback behavior explanation

### Documentation

- Added complete release management section to CLAUDE.md
- Introduced Keep a Changelog format with examples
- Documented 4-step release workflow
- Added changelog best practices and conventions

## [0.1.0] - 2025-10-19

### Added

- **Initial public release** of rclone-adapter
- **Async-first Python wrapper** for rclone with full async/await support
- **All 54 rclone subcommands** supported with auto-generated type-safe Pydantic models
- **Bundled rclone binaries** for Linux (x86_64, ARM64) in wheels
- **AsyncIterator-based streaming API** for real-time progress events
- **Three API styles**:
  - `async for event in rc.sync_stream()` - Real-time progress streaming
  - `result = await rc.sync()` - Simple async with final result
  - `result = rc.sync_blocking()` - Sync wrapper for non-async code
- **Event types**: `ProgressEvent`, `ErrorEvent`, `SyncResult`, `CopyResult`, etc.
- **Adaptive progress throttling** with command-specific grace periods
- **Structured logging** with structlog integration
- **Terminal output** with rich library for progress bars
- **Type safety**: Full type hints for IDE autocomplete, mypy strict mode compliance
- **Configuration validation** with Pydantic v2
- **Comprehensive exception hierarchy**: `RCloneError`, `RCloneNotFoundError`, `RCloneProcessError`
- **Process management**: Graceful shutdown, signal handling, orphan cleanup
- **Subprocess streaming**: Non-blocking output reading with proper EOF handling
- **JSON log parsing**: Parse rclone's `--use-json-log` output
- **Platform detection**: Automatic selection of bundled rclone binary
- **Full test suite**:
  - Unit tests with mocked time for long-running operations
  - Integration tests (marked with `@pytest.mark.integration`)
  - Type checking with mypy strict mode
  - Code linting with ruff
- **GitHub Actions CI/CD**:
  - Test workflow for Python 3.10-3.14
  - Lint and type checking
  - Build workflow for Linux wheels (x86_64, ARM64)
  - Automated PyPI publishing with trusted publishers
  - GitHub release creation with artifacts
- **Package structure**:
  - Core async client (`client.py`)
  - Pydantic models for config, events, results (`models.py`)
  - Process management (`process.py`)
  - Log parsing (`parser.py`)
  - Utility functions (`util.py`)
  - Exception hierarchy (`exceptions.py`)
  - PEP 561 type marker (`py.typed`)
  - Auto-generated command options (`_generated/`)
- **Documentation**:
  - Comprehensive README with quick start examples
  - CLAUDE.md developer guide with architecture decisions
  - CHANGELOG.md (this file)
- **Package metadata**:
  - MIT License
  - Python 3.10, 3.11, 3.12, 3.13, 3.14+ support
  - Core dependencies: pydantic>=2.0, rich>=13.0, structlog>=24.0
  - Optional API extra: fastapi, rq, redis, uvicorn
  - Optional dev extra: pytest, mypy, ruff, freezegun, fakeredis

### Fixed

- Resolved PyPI trusted publisher authentication by removing intermediate `twine check` step
- Fixed rclone binary extraction from zip files with separate per-architecture directories
- Corrected workflow conditions for tag-based vs main-branch publishing

### Technical Details

**Architecture**:
- Async-first with `asyncio.create_subprocess_exec` for non-blocking execution
- Event-driven architecture using AsyncIterator for streaming results
- Modular code generation for 54 rclone subcommands via `generate.py`
- Lazy import pattern to minimize startup time

**Dependencies**:
- Pydantic v2 for configuration validation and structured data
- rich for terminal UI and progress bars
- structlog for structured logging
- setuptools_scm for dynamic versioning

**Quality Assurance**:
- 100% type hints with mypy in strict mode
- ruff for fast linting and formatting
- pytest for comprehensive test coverage
- Integration tests marked and skipped when rclone not available
- Time mocking with freezegun for testing long-running operations

**CI/CD**:
- GitHub Actions on push, PR, and tag creation
- Trusted publisher authentication (no tokens stored)
- Multi-architecture wheel building with cibuildwheel
- QEMU for cross-architecture builds (ARM64 on x86_64)
- Automated PyPI publishing on version tags

### Known Limitations

- Windows and macOS wheel builds skipped (source distribution available)
- rclone binary bundling currently Linux-only (users on macOS/Windows should install rclone separately)
- Long-running operations (days) require external job queue (RQ, ARQ, pg_boss) for production use

### Future Roadmap

- [ ] **v0.2.0**: macOS and Windows wheel support
- [ ] **v0.3.0**: FastAPI integration example with RQ job queue
- [ ] **v0.4.0**: Progress persistence to Redis/database
- [ ] **v1.0.0**: API stability guarantee, expanded documentation
- [ ] **Beyond**: CLI interface, monitoring dashboard, advanced caching

## Development Notes

### How to Maintain This Changelog

1. **Keep changelog up-to-date** with every release
2. **Format**: Follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) conventions
3. **Sections**: Added, Fixed, Changed, Deprecated, Removed, Security
4. **Before release**:
   - Update version in `pyproject.toml`
   - Add section for new version with date
   - Link to git tag at bottom
5. **After release**:
   - Create git tag: `git tag -a v0.X.Y -m "Release vX.Y.Z"`
   - Push tag: `git push origin v0.X.Y`
   - GitHub Actions automatically publishes to PyPI
   - Verify on https://pypi.org/project/rclone-adapter/

### Release Process

```bash
# 1. Update version in pyproject.toml
# Example: version = "0.2.0"

# 2. Update CHANGELOG.md with new section
# Add [0.2.0] - YYYY-MM-DD header and changes

# 3. Commit changes
git add pyproject.toml CHANGELOG.md
git commit -m "chore: Prepare release v0.2.0"

# 4. Create and push tag
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin main
git push origin v0.2.0

# 5. Verify on PyPI (within 2-3 minutes)
# https://pypi.org/project/rclone-adapter/0.2.0/
```

## Links

- **PyPI**: https://pypi.org/project/rclone-adapter/
- **GitHub**: https://github.com/dirkpetersen/rclone-adapter
- **Issues**: https://github.com/dirkpetersen/rclone-adapter/issues
- **Discussions**: https://github.com/dirkpetersen/rclone-adapter/discussions

---

**Status**: Alpha (0.1.0) - API is stable but may receive enhancements before 1.0 release.
