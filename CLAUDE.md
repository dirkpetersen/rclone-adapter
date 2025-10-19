# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**rclone-adapter** is a Python package that provides a Pythonic interface to rclone, the cloud storage command-line tool. The goal is to expose all rclone subcommands and their options as a comprehensive Python API that feels natural to Python developers.

### Key Goals
- Dynamically discover and wrap all rclone subcommands
- Support all flags and options for each subcommand
- Provide a Pythonic API (likely using classes and methods)
- Include pretty output and progress bars (inspired by existing wrapper implementations)
- **Support long-running jobs (days) under FastAPI** - This is a critical design requirement
- Eventually replace the wrapper currently used in the `froster` repository

### Reference Repositories
These repositories in the `others/` directory should be consulted for design inspiration:
- **rcloners**: Examples of existing rclone wrapper implementations with nice progress bars
- **froster**: Contains the existing Python rclone wrapper that this will eventually replace; reference the `RClone` class design
- **python-pwalk**: Template for modern Python packaging, CI/CD, DevOps practices, and multi-threaded support

## Current Project State

The project is in early stages. Currently generated:
- **extract_rclone_help.py**: A utility script that extracts all rclone subcommands and their help text
- **rclone_help.json**: Machine-readable structure of all 54 rclone subcommands with flags and help text

### Generated Data Structure
Each subcommand entry in rclone_help.json contains:
```json
{
  "description": "Short description",
  "help_text": "Full help output from 'rclone [command] --help'",
  "flags": [
    {
      "flag": "--flag-name",
      "description": "Flag description"
    }
  ]
}
```

## Development Notes

### Architecture Approach
The main challenge is building a Pythonic wrapper that:
1. Dynamically discovers available subcommands (query `rclone --help`)
2. For each subcommand, discovers available flags (query `rclone <subcommand> --help`)
3. Exposes this as clean Python classes/methods
4. The generated JSON/YAML files are reference data for this discovery

### Class Design Inspiration
Review the `RClone` class in the `froster` repository for patterns on how to structure the main wrapper class(es). The current adapter should improve upon and replace that design.

### Running the Extractor
To regenerate or update the rclone_help.json file after rclone updates:
```bash
python3 extract_rclone_help.py
```

Requires:
- rclone installed locally and on PATH
- No external Python dependencies (uses only stdlib)

## Dependencies and Setup

### Required
- Python 3.7+
- rclone (installed locally)

Check `python-pwalk` template repository for recommended CI/CD setup patterns.

## Architectural Decisions (Modern 2025 Design)

### Package Structure
- **Single package with optional dependencies**:
  - `pip install rclone-adapter` - Core async/sync wrapper
  - `pip install rclone-adapter[api]` - FastAPI/RQ for long-running jobs
- **Core dependencies** (minimal but modern):
  - `pydantic>=2.0` - Configuration validation and data models
  - `rich>=13.0` - Progress display and pretty output
  - `structlog>=24.0` - Structured logging
- **API extra dependencies**:
  - `fastapi>=0.110`
  - `rq>=1.16`
  - `redis>=5.0`
  - `uvicorn>=0.27`

### API Design - Async First with Dual Interfaces

**Core design**: Both streaming and simple APIs for flexibility.

```python
from rclone_adapter import RClone, RCloneConfig
from rclone_adapter.models import SyncResult, ProgressEvent

# Async-first (recommended)
async def main():
    config = RCloneConfig(
        env_vars={"RCLONE_S3_PROVIDER": "AWS"},
        config_file="~/.config/rclone/rclone.conf"
    )

    rc = RClone(config)

    # OPTION 1: Streaming API (for progress monitoring)
    async for event in rc.sync_stream(source="/local", dest="s3:bucket/"):
        if event.type == "progress":
            print(f"Progress: {event.progress}%")
        elif event.type == "error":
            print(f"Error: {event.message}")

    # OPTION 2: Simple API (just final result)
    result = await rc.sync(source="/local", dest="s3:bucket/")
    # Returns only SyncResult, no streaming

    # OPTION 3: Callback API (for integration)
    async def on_progress(event: ProgressEvent):
        print(f"Progress: {event.progress}%")

    result = await rc.sync(
        source="/local",
        dest="s3:bucket/",
        progress_callback=on_progress
    )

# Sync wrapper (for non-async code)
def sync_main():
    rc = RClone.sync_client(config)
    result = rc.sync_blocking(source="/local", dest="s3:bucket/")
```

### Code Generation Strategy - Modular Structure
1. **generate.py** creates **multiple files** to avoid one massive file:
   ```
   rclone_adapter/_generated/
   ├── __init__.py           # Exports all models and COMMAND_OPTIONS
   ├── common.py             # Shared options (dry_run, verbose, etc.)
   ├── sync_commands.py      # sync, copy, move, bisync
   ├── listing_commands.py   # ls, lsd, lsl, lsjson, lsf
   ├── check_commands.py     # check, checksum, hashsum, md5sum
   ├── config_commands.py    # config, authorize, obscure
   ├── serve_commands.py     # serve, mount, nfsmount
   └── utility_commands.py   # All other commands
   ```

2. **Generated code with lazy loading**:
```python
# _generated/__init__.py
from typing import TYPE_CHECKING, Type
from pydantic import BaseModel

if TYPE_CHECKING:
    from .sync_commands import SyncOptions, CopyOptions
    # ... type hints for IDE

# Lazy loading to reduce import time
def get_command_options(command: str) -> Type[BaseModel]:
    """Lazy load command options only when needed."""
    if command == "sync":
        from .sync_commands import SyncOptions
        return SyncOptions
    elif command == "copy":
        from .sync_commands import CopyOptions
        return CopyOptions
    # ... etc
```

### Configuration - Validated Pydantic Models

```python
from pydantic import BaseModel, Field, field_validator
from pathlib import Path
from typing import Optional, Dict
import shutil

class RCloneConfig(BaseModel):
    """Configuration for RClone client with validation."""
    config_file: Optional[Path] = None
    env_vars: Dict[str, str] = Field(default_factory=dict)
    rclone_path: str = "rclone"
    log_level: str = "INFO"
    default_flags: list[str] = Field(default_factory=list)

    @field_validator('rclone_path')
    def validate_rclone_exists(cls, v):
        """Validate rclone executable exists."""
        if not shutil.which(v):
            raise ValueError(f"rclone not found at: {v}")
        return v

    @field_validator('config_file')
    def validate_config_file(cls, v):
        """Validate config file exists and is readable."""
        if v and not v.exists():
            raise ValueError(f"Config file not found: {v}")
        if v and not v.is_file():
            raise ValueError(f"Config path is not a file: {v}")
        return v

    @field_validator('env_vars')
    def validate_env_vars(cls, v):
        """Validate environment variables are valid rclone vars."""
        valid_prefixes = ('RCLONE_', 'AWS_', 'AZURE_', 'GCS_')
        for key in v:
            if not any(key.startswith(p) for p in valid_prefixes):
                raise ValueError(f"Invalid env var: {key}")
        return v

    model_config = {"frozen": True}  # Immutable after creation
```

### Return Values - Pydantic Models

```python
from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class ProgressEvent(BaseModel):
    """Progress update event."""
    type: Literal["progress"] = "progress"
    timestamp: datetime
    bytes_transferred: int
    total_bytes: int
    progress: float  # 0.0 to 1.0
    transfer_rate: int  # bytes/sec
    eta_seconds: Optional[int] = None
    current_file: Optional[str] = None

class ErrorEvent(BaseModel):
    """Enhanced error event with context."""
    type: Literal["error"] = "error"
    timestamp: datetime
    message: str
    file: Optional[str] = None
    retry_attempt: int = 0
    max_retries: int = 3
    is_retryable: bool = False
    error_category: Literal["network", "permission", "space", "not_found", "config", "unknown"] = "unknown"
    error_code: Optional[str] = None  # Rclone-specific error code

class SyncResult(BaseModel):
    """Final result of sync operation."""
    success: bool
    return_code: int
    bytes_transferred: int
    files_transferred: int
    errors: list[ErrorEvent]
    duration_seconds: float
    stats: dict  # Full rclone stats
```

**Event Stream Pattern**: Methods return `AsyncIterator[Event]` for real-time updates.

### Exception Handling - Structured

```python
class RCloneError(Exception):
    """Base exception for rclone-adapter."""

class RCloneNotFoundError(RCloneError):
    """rclone executable not found."""

class RCloneProcessError(RCloneError):
    """rclone process failed."""
    def __init__(self, return_code: int, message: str):
        self.return_code = return_code
        self.message = message
        super().__init__(f"rclone failed with code {return_code}: {message}")

class RCloneConfigError(RCloneError):
    """Invalid configuration."""
```

**Philosophy**: Raise exceptions for errors, return results for completion.

### Subprocess Management - Modern Async with Configurable Grace

```python
import asyncio
from contextlib import asynccontextmanager
from typing import Dict

# Command-specific grace periods (seconds)
GRACE_PERIODS: Dict[str, float] = {
    "move": 30.0,      # Needs time to complete atomic operations
    "sync": 15.0,      # May be updating metadata
    "bisync": 20.0,    # Complex two-way sync
    "mount": 10.0,     # Needs clean unmount
    "serve": 10.0,     # Graceful server shutdown
    # Default for all others
    "default": 5.0
}

class ProcessManager:
    """Manages rclone subprocess lifecycle with configurable grace."""

    @asynccontextmanager
    async def run_command(
        self,
        cmd: list[str],
        env: dict,
        command_name: str
    ):
        """Context manager for subprocess with command-specific cleanup."""
        grace_period = GRACE_PERIODS.get(command_name, GRACE_PERIODS["default"])

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env
        )

        try:
            yield process
        finally:
            # Graceful shutdown with command-specific grace period
            if process.returncode is None:
                process.terminate()
                try:
                    await asyncio.wait_for(process.wait(), timeout=grace_period)
                except asyncio.TimeoutError:
                    # Force kill if grace period exceeded
                    process.kill()
                    await process.wait()

    async def stream_progress(self, process) -> AsyncIterator[ProgressEvent]:
        """Stream progress events from rclone stderr."""
        async for line in process.stderr:
            event = self._parse_json_log_line(line)
            if event:
                yield event
```

### Logging - Structured with structlog

```python
import structlog

logger = structlog.get_logger()

# Usage in code
logger.info(
    "rclone_command_started",
    command="sync",
    source="/local",
    dest="s3:bucket/",
    pid=process.pid
)

logger.error(
    "rclone_command_failed",
    command="sync",
    return_code=1,
    error="permission denied",
    duration=45.2
)
```

**Benefits**:
- JSON output for log aggregation
- Contextual logging (automatically includes request ID, user, etc.)
- Easy filtering and searching
- Integration with observability platforms

### Queue Backend - RQ with Modern Patterns

```python
from rq import Queue
from rq.job import Job
from redis import Redis
import asyncio

class RQAdapter:
    """Modern RQ integration with async support."""

    def __init__(self, redis_url: str):
        self.redis = Redis.from_url(redis_url)
        self.queue = Queue(connection=self.redis)

    async def enqueue_job(
        self,
        command: str,
        source: str,
        dest: str,
        options: dict
    ) -> str:
        """Enqueue job and return job ID."""
        job = self.queue.enqueue(
            'rclone_adapter.worker.run_rclone_command',
            command, source, dest, options,
            job_timeout='7d',  # Max 7 days for long jobs
            result_ttl='30d',  # Keep results for 30 days
            failure_ttl='90d'  # Keep failures for debugging
        )
        return job.id

    async def get_job_status(self, job_id: str) -> dict:
        """Get job status with progress."""
        job = Job.fetch(job_id, connection=self.redis)

        # Get real-time progress from Redis
        progress_key = f"rclone:progress:{job_id}"
        progress_data = self.redis.get(progress_key)

        return {
            "id": job_id,
            "status": job.get_status(),
            "progress": json.loads(progress_data) if progress_data else None,
            "result": job.result if job.is_finished else None,
            "error": str(job.exc_info) if job.is_failed else None
        }

    async def cancel_job(self, job_id: str):
        """Cancel running job gracefully."""
        job = Job.fetch(job_id, connection=self.redis)

        # Send cancellation signal
        cancel_key = f"rclone:cancel:{job_id}"
        self.redis.set(cancel_key, "1", ex=3600)

        # Worker checks this key and terminates gracefully
        job.cancel()
```

### Progress Updates - Adaptive Intervals

```python
from dataclasses import dataclass
from typing import Optional
import time

@dataclass
class AdaptiveProgressConfig:
    """Adaptive progress update intervals based on operation size."""
    min_interval: float = 1.0      # Minimum seconds between updates
    max_interval: float = 60.0     # Maximum seconds between updates
    small_file_threshold: int = 10 * 1024 * 1024  # 10MB
    large_file_threshold: int = 1024 * 1024 * 1024  # 1GB

    def calculate_interval(
        self,
        total_bytes: int,
        transfer_rate: int,
        current_file_size: Optional[int] = None
    ) -> float:
        """Calculate optimal update interval."""
        # Small files: update frequently
        if current_file_size and current_file_size < self.small_file_threshold:
            return self.min_interval

        # Large operations: scale interval with size
        if total_bytes > self.large_file_threshold:
            # Update every 1% of progress
            if transfer_rate > 0:
                one_percent_time = (total_bytes * 0.01) / transfer_rate
                return min(max(one_percent_time, self.min_interval), self.max_interval)
            return 10.0  # Default for unknown rate

        # Medium operations: fixed interval
        return 5.0

class ProgressTracker:
    """Tracks and throttles progress updates."""

    def __init__(self, config: AdaptiveProgressConfig):
        self.config = config
        self.last_update = 0.0
        self.current_interval = 5.0

    def should_update(self, event: ProgressEvent) -> bool:
        """Check if we should emit this progress update."""
        now = time.time()

        # Recalculate interval based on current metrics
        self.current_interval = self.config.calculate_interval(
            event.total_bytes,
            event.transfer_rate,
            len(event.current_file) if event.current_file else None
        )

        if now - self.last_update >= self.current_interval:
            self.last_update = now
            return True
        return False
```

Worker code with adaptive updates:
```python
async def run_rclone_command(command, source, dest, options, job_id):
    """Worker function with adaptive progress updates."""
    redis = Redis.from_url(settings.REDIS_URL)
    progress_key = f"rclone:progress:{job_id}"
    cancel_key = f"rclone:cancel:{job_id}"

    config = RCloneConfig(**options)
    rc = RClone(config)
    tracker = ProgressTracker(AdaptiveProgressConfig())

    async for event in rc.sync_stream(source, dest):
        # Check for cancellation
        if redis.get(cancel_key):
            raise Cancelled("Job cancelled by user")

        # Update progress with adaptive interval
        if event.type == "progress" and tracker.should_update(event):
            redis.setex(
                progress_key,
                300,  # 5 min TTL
                event.model_dump_json()
            )

    return event  # Final result
```

## Important Constraints

- **Do not modify the `froster` repository** (it's a reference only)
- **Minimal core dependencies**: Only `rich` for progress bars
- **Pythonic design**: Prioritize Python conventions over direct rclone command mirroring
- **Progress indicators**: Always use rich library for pretty output (core dependency)

## Reference Note

The `others/` directory contains older rclone wrapper implementations (rcloners, froster) and a packaging template (python-pwalk).

**We are NOT following those old patterns.** They use outdated 2020-era Python practices:
- No async support
- Dict-based returns instead of Pydantic models
- Boolean returns that lose information
- Tight coupling to specific UI libraries
- No structured logging

This modern 2025 implementation uses:
- Async-first with AsyncIterator for streaming
- Pydantic v2 for all data modeling
- Structured logging with structlog
- Full type hints with mypy strict mode
- Event-driven architecture
- Context managers for resource cleanup

## Data Format Decision

The project uses **JSON only** for storing rclone command metadata:
- `rclone_help.json` contains all subcommand information
- YAML format was removed to avoid duplication
- JSON is preferred for programmatic parsing in Python

## Long-Running Jobs Infrastructure

A critical requirement is supporting rclone operations that may run for days under FastAPI. Keep the infrastructure simple with three supported backends:

### Supported Task Queue Backends

Choose **one** based on your needs:

#### 1. RQ (Redis Queue)
- **Use case**: Simplest option, Redis-only
- **Pros**: Minimal setup, easy to understand, good for single-server
- **Cons**: Less feature-rich, no native async support
- **Storage**: Redis for everything (jobs, state, results)

#### 2. ARQ
- **Use case**: Modern async/await patterns with FastAPI
- **Pros**: Native async, clean API, lightweight
- **Cons**: Fewer ecosystem tools than RQ
- **Storage**: Redis for everything (jobs, state, results)

#### 3. pg_boss
- **Use case**: When you already have PostgreSQL
- **Pros**: No Redis dependency, SQL-based monitoring, ACID guarantees
- **Cons**: Requires Node.js wrapper or Python client
- **Storage**: PostgreSQL for everything (jobs, state, results)

**Recommendation**: Use **ARQ** if you want async/await integration with FastAPI, or **RQ** if you prefer simplicity and maturity.

### Core Features to Implement

#### Job Lifecycle States
```python
PENDING    # Job queued but not started
RUNNING    # Job in progress
COMPLETED  # Job finished successfully
FAILED     # Job encountered an error
CANCELLED  # User cancelled the job
```

#### Progress Tracking
- Parse rclone's `--progress` and `--stats` output
- Track: bytes transferred, files processed, current file, transfer rate
- Store progress updates in the queue backend (Redis/PostgreSQL)

#### Process Management
- Run rclone as subprocess with signal handling (SIGTERM for cancellation)
- Use `asyncio.create_subprocess_exec` for async operations
- Track PIDs to clean up orphaned processes
- Capture stdout/stderr for progress and logs

### Simple API Pattern

```python
# POST /jobs/sync - Create job
{"source": "local/path", "dest": "remote:path"}
# Returns: {"job_id": "uuid", "status": "pending"}

# GET /jobs/{job_id} - Check status
# Returns: {"job_id": "uuid", "status": "running", "progress": 45.2}

# DELETE /jobs/{job_id} - Cancel job
```

### Required Python Libraries

```python
# Choose one task queue
rq          # For RQ (Redis Queue)
arq         # For ARQ (async Redis queue)
# pg_boss requires Python client or Node.js integration

# Common dependencies
redis       # For RQ/ARQ
psycopg2    # For pg_boss (PostgreSQL)
fastapi     # Web framework
```

### Integration with rclone-adapter

The package should provide:
- **Async API**: Methods that work with `async/await`
- **Progress callbacks**: Hook for updating job progress
- **Process control**: Methods to cancel running jobs
- **Output parsing**: Extract progress from rclone output

## Development Plan (Modern 2025)

### Phase 1: Foundation
1. **Project setup**:
   ```bash
   # pyproject.toml with modern tooling
   [tool.ruff]
   target-version = "py311"
   select = ["E", "F", "I", "N", "UP", "ANN", "ASYNC", "S"]

   [tool.mypy]
   strict = true
   ```

2. **Core dependencies**:
   - `pydantic>=2.0` - Data validation
   - `rich>=13.0` - Terminal UI
   - `structlog>=24.0` - Structured logging

3. **Package structure**:
   ```
   rclone_adapter/
   ├── __init__.py
   ├── client.py          # RClone async client
   ├── models.py          # Pydantic models (Events, Config, Results)
   ├── process.py         # ProcessManager for subprocess handling
   ├── parser.py          # Parse rclone --use-json-log output
   ├── exceptions.py      # Exception hierarchy
   └── _generated.py      # Generated command options (from generate.py)
   ```

### Phase 2: Code Generation (generate.py)
1. **Read rclone_help.json** and generate:
   - Pydantic models for EACH command's options
   - Type hints for all parameters
   - Docstrings with full command help

2. **Example generated output** (`_generated.py`):
   ```python
   # AUTO-GENERATED - DO NOT EDIT
   from pydantic import BaseModel, Field

   class SyncOptions(BaseModel):
       """Options for the 'rclone sync' command."""
       create_empty_src_dirs: bool = Field(
           False,
           description="Create empty source directories"
       )
       # ... all options as fields

   class CopyOptions(BaseModel):
       """Options for the 'rclone copy' command."""
       # ... all copy options

   # Dict mapping commands to their option classes
   COMMAND_OPTIONS: dict[str, type[BaseModel]] = {
       "sync": SyncOptions,
       "copy": CopyOptions,
       # ... all 54 commands
   }
   ```

### Phase 3: Core Client (Async-First)
1. **RClone client** (`client.py`):
   ```python
   class RClone:
       """Modern async rclone client."""

       def __init__(self, config: RCloneConfig):
           self.config = config
           self.process_manager = ProcessManager()
           self.logger = structlog.get_logger()

       async def sync(
           self,
           source: str,
           dest: str,
           options: SyncOptions | None = None,
           show_progress: bool = True
       ) -> AsyncIterator[ProgressEvent | ErrorEvent | SyncResult]:
           """Async generator yielding events."""
           # Implementation

       def sync_blocking(self, *args, **kwargs) -> SyncResult:
           """Sync wrapper for non-async code."""
           return asyncio.run(self._collect_final_result(
               self.sync(*args, **kwargs)
           ))
   ```

2. **ProcessManager** (`process.py`):
   - Context manager for subprocess lifecycle
   - Graceful termination (SIGTERM → SIGKILL)
   - Async streaming of stdout/stderr
   - PID tracking and orphan cleanup

3. **Parser** (`parser.py`):
   ```python
   def parse_json_log_line(line: bytes) -> ProgressEvent | ErrorEvent | None:
       """Parse single line from --use-json-log."""
       try:
           data = json.loads(line)
           if "stats" in data:
               return ProgressEvent.from_rclone_stats(data)
           elif "error" in data:
               return ErrorEvent.from_rclone_error(data)
       except json.JSONDecodeError:
           return None
   ```

### Phase 4: Testing (pytest + pytest-asyncio + time mocking)
1. **Unit tests with mock time for long-running jobs**:
   ```python
   import pytest
   from unittest.mock import patch, AsyncMock
   import asyncio
   from freezegun import freeze_time

   @pytest.mark.asyncio
   @freeze_time("2025-01-01", auto_tick_seconds=1)
   async def test_long_running_job_with_time_progression():
       """Test multi-day job with accelerated time."""
       config = RCloneConfig()
       rc = RClone(config)

       # Mock subprocess that simulates 3-day transfer
       mock_process = AsyncMock()
       mock_process.stderr = AsyncIterator([
           b'{"stats": {"bytes": 0, "totalBytes": 1e12}}',      # Start
           b'{"stats": {"bytes": 3e11, "totalBytes": 1e12}}',   # Day 1
           b'{"stats": {"bytes": 6e11, "totalBytes": 1e12}}',   # Day 2
           b'{"stats": {"bytes": 1e12, "totalBytes": 1e12}}',   # Complete
       ])

       with patch('rclone_adapter.process.ProcessManager.run_command', return_value=mock_process):
           events = []
           async for event in rc.sync_stream("/src", "/dst"):
               events.append(event)
               # Simulate passage of time
               await asyncio.sleep(86400)  # 1 day in seconds

           assert len(events) == 4
           assert events[-1].type == "result"
           assert events[-1].duration_seconds == 259200  # 3 days
   ```

2. **Testing with mock Redis for job queue**:
   ```python
   from fakeredis import FakeRedis

   @pytest.mark.asyncio
   async def test_job_cancellation():
       """Test job cancellation after days of running."""
       redis = FakeRedis()
       job_id = "test-job-123"

       # Start long-running job
       task = asyncio.create_task(
           run_rclone_command("sync", "/src", "/dst", {}, job_id)
       )

       # Simulate time passing
       await asyncio.sleep(0.1)

       # Cancel after "2 days"
       redis.set(f"rclone:cancel:{job_id}", "1")

       # Verify cancellation
       with pytest.raises(Cancelled):
           await task
   ```

3. **Integration tests** (require rclone):
   - Marked with `@pytest.mark.integration`
   - Skip if rclone not available
   - Use local filesystem for testing
   - Use small test files to keep tests fast

4. **Type checking**:
   ```bash
   mypy rclone_adapter --strict
   ```

5. **Performance tests for large operations**:
   ```python
   @pytest.mark.benchmark
   async def test_large_file_progress_throttling():
       """Ensure progress updates are properly throttled."""
       tracker = ProgressTracker(AdaptiveProgressConfig())

       # Simulate 1TB file transfer
       for i in range(10000):
           event = ProgressEvent(
               bytes_transferred=i * 1e8,
               total_bytes=1e12,
               transfer_rate=1e8  # 100MB/s
           )
           should_update = tracker.should_update(event)

       # Should have throttled most updates
       assert tracker.update_count < 100  # Not 10000
   ```

### Phase 5: API Package (FastAPI + RQ)
1. **Structure**:
   ```
   rclone_adapter/api/
   ├── __init__.py
   ├── app.py             # FastAPI application
   ├── worker.py          # RQ worker with async support
   ├── models.py          # API request/response models
   └── queue.py           # RQAdapter class
   ```

2. **FastAPI app** with modern patterns:
   ```python
   from fastapi import FastAPI, BackgroundTasks
   from contextlib import asynccontextmanager

   @asynccontextmanager
   async def lifespan(app: FastAPI):
       # Startup: connect to Redis
       yield
       # Shutdown: cleanup

   app = FastAPI(lifespan=lifespan)

   @app.post("/jobs/sync")
   async def create_sync_job(req: SyncRequest) -> JobResponse:
       """Create background sync job."""
       # Use RQAdapter to enqueue
   ```

3. **Worker** that supports cancellation:
   ```python
   @job('default', timeout='7d')
   async def run_sync_job(job_id: str, source: str, dest: str, options: dict):
       """Worker function with cancellation support."""
       # Check Redis for cancel signal
       # Stream progress to Redis
       # Return result
   ```

### Phase 6: Documentation & Examples
1. **README.md** with:
   - Quick start (async and sync)
   - Configuration examples
   - Progress handling
   - FastAPI deployment

2. **Examples** directory:
   - `basic_async.py` - Simple async usage
   - `sync_wrapper.py` - Sync wrapper example
   - `custom_progress.py` - Custom progress handler
   - `fastapi_server.py` - Full API server

3. **API docs** (auto-generated):
   - Docstrings → Sphinx/MkDocs
   - OpenAPI spec from FastAPI

### Phase 7: Observability
1. **Metrics** (optional, for [api]):
   ```python
   from prometheus_client import Counter, Histogram

   rclone_commands = Counter('rclone_commands_total', 'Total commands')
   rclone_duration = Histogram('rclone_duration_seconds', 'Duration')
   ```

2. **Structured logging** everywhere:
   ```python
   logger.info("command_started", command="sync", job_id=job_id)
   logger.error("command_failed", error=str(e), return_code=rc)
   ```

### Phase 8: CI/CD (GitHub Actions)
1. **Test workflow**:
   - Matrix: Python 3.11, 3.12, 3.13
   - Ruff linting
   - Mypy type checking
   - Pytest with coverage
   - Test with/without rclone installed

2. **Release workflow**:
   - Build wheels with cibuildwheel
   - Publish to PyPI on tag push
   - Generate GitHub release notes

## File Structure (Final - Modern 2025)

```
rclone-adapter/
├── pyproject.toml                 # Modern Python packaging
├── README.md                      # User-facing documentation
├── CLAUDE.md                      # Developer guidance (this file)
├── LICENSE                        # MIT License
├── generate.py                    # Code generator for options
├── extract_rclone_help.py        # Extracts rclone command metadata
├── rclone_help.json              # Source data (54 commands)
│
├── rclone_adapter/               # Core package
│   ├── __init__.py               # Public API exports
│   ├── client.py                 # RClone async client (main class)
│   ├── models.py                 # Pydantic models (Config, Events, Results)
│   ├── process.py                # ProcessManager for subprocess
│   ├── parser.py                 # Parse --use-json-log output
│   ├── exceptions.py             # Exception hierarchy
│   ├── _generated.py             # Generated Pydantic option models
│   │
│   └── api/                      # Optional [api] extra
│       ├── __init__.py
│       ├── app.py                # FastAPI application
│       ├── worker.py             # RQ worker functions
│       ├── queue.py              # RQAdapter for job management
│       └── models.py             # API request/response models
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   ├── test_client.py            # Test RClone client
│   ├── test_parser.py            # Test log parsing
│   ├── test_process.py           # Test ProcessManager
│   ├── test_models.py            # Test Pydantic models
│   └── test_api/                 # API tests
│       ├── __init__.py
│       ├── test_worker.py
│       ├── test_queue.py
│       └── test_app.py
│
├── examples/                     # Usage examples
│   ├── 01_basic_async.py         # Simple async usage
│   ├── 02_sync_wrapper.py        # Sync wrapper
│   ├── 03_custom_progress.py     # Custom progress handler
│   ├── 04_config_patterns.py     # Configuration examples
│   └── 05_fastapi_server.py      # Full FastAPI server
│
├── docs/                         # Additional documentation
│   ├── index.md
│   ├── api_reference.md
│   ├── configuration.md
│   └── migration_from_froster.md
│
└── .github/
    └── workflows/
        ├── test.yml              # Test on push/PR
        ├── lint.yml              # Ruff + mypy
        ├── build.yml             # Build wheels
        └── release.yml           # Publish to PyPI
```

## Modern Python Tooling Stack (2025)

```toml
[project]
name = "rclone-adapter"
requires-python = ">=3.11"
dependencies = [
    "pydantic>=2.0",
    "rich>=13.0",
    "structlog>=24.0",
]

[project.optional-dependencies]
api = [
    "fastapi>=0.110",
    "rq>=1.16",
    "redis>=5.0",
    "uvicorn>=0.27",
]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "pytest-cov>=4.1",
    "mypy>=1.8",
    "ruff>=0.2",
]

[tool.ruff]
target-version = "py311"
select = ["ALL"]
ignore = ["D", "ANN101", "ANN102"]  # Ignore docstring rules for now

[tool.mypy]
strict = true
python_version = "3.11"

[tool.pytest.ini_options]
asyncio_mode = "auto"
markers = [
    "integration: marks tests requiring rclone (deselect with '-m \"not integration\"')"
]
```

## Changelog and Release Management

### Maintaining CHANGELOG.md

The project uses [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format for tracking all notable changes. This changelog is **automatically referenced** by PyPI and GitHub, so it must be kept current with every release.

#### Changelog Format

**File**: `CHANGELOG.md` at repository root

**Structure**:
- One top-level heading: `# Changelog`
- Version sections with format: `## [X.Y.Z] - YYYY-MM-DD`
- Subsections: `### Added`, `### Fixed`, `### Changed`, `### Deprecated`, `### Removed`, `### Security`
- Each change is a bullet point with context
- Unreleased section (optional) for in-progress work

**Example**:
```markdown
# Changelog

## [0.2.0] - 2025-11-15

### Added
- New feature description
- Another feature

### Fixed
- Bug fix description

### Changed
- Breaking change explanation

## [0.1.0] - 2025-10-19

### Added
- Initial public release
```

#### When to Update Changelog

1. **For every feature/bug fix**: Add entry immediately in development
2. **Before release**: Ensure all changes since last release are documented
3. **After release**: Section is finalized with date and version link

#### Release Workflow

**Step 1: Prepare Release**
```bash
# 1. Update version in pyproject.toml
# Example: version = "0.2.0"

# 2. Update CHANGELOG.md
# - Change [Unreleased] to [0.2.0] - 2025-11-15
# - Or create new [0.2.0] section with all changes since 0.1.0
# - Review all entries for clarity and completeness
```

**Step 2: Create Commit and Tag**
```bash
# Commit changes
git add pyproject.toml CHANGELOG.md
git commit -m "chore: Release version 0.2.0

- Update version to 0.2.0
- Update CHANGELOG.md with release notes

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

# Create annotated tag (required for GitHub release)
git tag -a v0.2.0 -m "Release version 0.2.0"

# Push to GitHub
git push origin main
git push origin v0.2.0
```

**Step 3: Verify Release**
- GitHub Actions automatically builds and publishes to PyPI (2-3 minutes)
- Check: https://pypi.org/project/rclone-adapter/0.2.0/
- Verify wheel and sdist are present
- Check that README and CHANGELOG are displayed correctly

**Step 4: Create GitHub Release**
```bash
# If not automatically created, manually create with:
gh release create v0.2.0 \
  --title "Release v0.2.0" \
  --notes "$(sed -n '/^## \[0.2.0\]/,/^## \[/p' CHANGELOG.md | head -n -1)"
```

#### Changelog Best Practices

1. **Use consistent terminology**:
   - "Add" / "Added" for new features
   - "Fix" / "Fixed" for bug fixes
   - "Change" / "Changed" for modifications
   - "Remove" / "Removed" for deprecations
   - "Security" for security patches

2. **Be descriptive but concise**:
   - ✅ "Add async progress streaming with adaptive throttling"
   - ❌ "Fix stuff" or "Improve things"

3. **Link to related issues/PRs** (optional but helpful):
   - "Fix deadlock in subprocess cleanup (#123)"
   - "Add type hints to parser module (#125)"

4. **Document breaking changes clearly**:
   - "BREAKING: Rename `SyncOptions.dry_run` to `SyncOptions.check` - update your code"

5. **Group logically related changes**:
   - All "Added" items together
   - All "Fixed" items together
   - Etc.

#### Unreleased Section (Optional)

For ongoing development, you can optionally maintain an `[Unreleased]` section:

```markdown
## [Unreleased]

### Added
- (in development) New feature being worked on

### Fixed
- (in development) Bug fix being tested

## [0.1.0] - 2025-10-19
...
```

When releasing, convert `[Unreleased]` to `[0.2.0] - YYYY-MM-DD`.

### Automated Release Process

The repository uses GitHub Actions to **automate PyPI publishing**:

1. **Tag push triggers build workflow**: `.github/workflows/build-wheels.yml`
   - Builds Linux wheels for all Python versions and architectures
   - Builds source distribution (sdist)
   - Uploads artifacts to GitHub Actions

2. **Artifacts trigger publish workflow**: `.github/workflows/publish-pypi.yml`
   - Downloads build artifacts
   - Publishes to PyPI using trusted publishers
   - Creates GitHub release with artifacts
   - Generates digital attestations (Sigstore)

3. **No manual intervention needed** - everything is automated!

### Troubleshooting Releases

**Problem**: "Package already exists on PyPI"
- **Solution**: Use unique version number. Can't republish same version.

**Problem**: GitHub Actions publish failed
- **Solution**: Check logs in Actions tab. Common issues:
  - Version mismatch in pyproject.toml vs tag
  - Missing CHANGELOG entry (metadata parsing issue)
  - Trusted publisher configuration issue

**Problem**: PyPI shows old README or CHANGELOG
- **Solution**: PyPI caches for 10 minutes. Refresh page or wait.

### Version Numbering

Use [Semantic Versioning](https://semver.org/):
- **MAJOR** (X.0.0): Breaking API changes
- **MINOR** (0.X.0): New features, backward compatible
- **PATCH** (0.0.X): Bug fixes only

Examples:
- 0.1.0 → 0.2.0 (feature release)
- 0.1.0 → 0.1.1 (patch release)
- 0.9.0 → 1.0.0 (major release, API stable)
