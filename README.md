# rclone-adapter

A Pythonic interface to rclone for cloud storage operations.

## Overview

**rclone-adapter** provides a comprehensive Python wrapper around [rclone](https://rclone.org/), making it easy to interact with cloud storage providers from Python code. Instead of running shell commands, you can use natural Python methods and classes to copy, sync, mount, and manage files across various cloud services.

## Features

- **Pythonic API**: Work with rclone using intuitive Python classes and methods
- **Full Coverage**: Supports all rclone subcommands and their options
- **Dynamic Discovery**: Automatically adapts to your installed rclone version
- **Progress Indicators**: Visual feedback for long-running operations
- **Type Safe**: Full type hints for better IDE support and code quality

## Installation

```bash
pip install rclone-adapter
```

**Prerequisites**: rclone must be installed on your system. See [rclone installation guide](https://rclone.org/install/).

## Quick Start

```python
from rclone_adapter import RClone

# Initialize the adapter
rc = RClone()

# Copy files from local to remote
rc.copy('local/path', 'remote:bucket/path')

# Sync directories
rc.sync('source/', 'dest/', verbose=True)

# List remotes
remotes = rc.listremotes()
print(remotes)
```

## Requirements

- Python 3.7 or higher
- rclone installed and available in PATH

## Documentation

For detailed usage examples and API reference, see the [documentation](docs/).

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 


