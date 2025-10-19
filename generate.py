#!/usr/bin/env python3
"""
Code generator for rclone-adapter.

Reads rclone_help.json and generates Pydantic models for all command options.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent, indent


def clean_flag_name(flag: str) -> str:
    """Convert flag name to valid Python identifier."""
    # Remove -- prefix and convert to snake_case
    name = flag.lstrip("-").replace("-", "_")
    # Handle special cases
    if not name:
        return "flag"
    if name[0].isdigit():
        name = f"flag_{name}"
    return name


def infer_flag_type(flag: str, description: str) -> str:
    """Infer the type of a flag from its name and description."""
    flag_lower = flag.lower()
    desc_lower = description.lower()

    # Boolean flags (no value)
    if not "=" in flag and not any(
        x in desc_lower for x in ["number", "size", "count", "duration", "time"]
    ):
        return "bool"

    # Integer types
    if any(x in desc_lower for x in ["number", "count", "int"]):
        return "int"

    # Size types
    if any(x in desc_lower for x in ["size", "bytes"]):
        return "int"  # Size in bytes

    # Duration/time types
    if any(x in desc_lower for x in ["duration", "time", "seconds", "timeout"]):
        return "float"

    # Default to string
    return "str"


def generate_option_model(command: str, flags: list[dict]) -> str:
    """Generate Pydantic model for a command's options."""
    class_name = f"{command.capitalize()}Options"
    lines = [
        f"class {class_name}(BaseModel):",
        f'    """Options for the \'rclone {command}\' command."""',
        "",
    ]

    # Group flags by type for better organization
    bool_flags = []
    other_flags = []

    for flag_info in flags:
        flag = flag_info["flag"]
        description = flag_info["description"]

        # Skip if it's just showing shorthand like "-h, --help"
        if flag == "-h," or "help for" in description:
            continue

        # Extract the actual flag name (handle "-h, --help" format)
        if "," in flag:
            parts = flag.split(",")
            flag = parts[-1].strip()  # Use the long form

        flag_name = clean_flag_name(flag)
        flag_type = infer_flag_type(flag, description)

        # Escape quotes in description
        description = description.replace('"', '\\"')

        if flag_type == "bool":
            bool_flags.append((flag_name, description, flag))
        else:
            other_flags.append((flag_name, description, flag, flag_type))

    # Add boolean flags first
    for flag_name, description, orig_flag in bool_flags:
        lines.append(
            f'    {flag_name}: bool = Field(False, description="{description}")'
        )

    # Add other flags
    for flag_name, description, orig_flag, flag_type in other_flags:
        if flag_type == "str":
            default = '""'
        elif flag_type == "int":
            default = "0"
        elif flag_type == "float":
            default = "0.0"
        else:
            default = "None"

        lines.append(
            f'    {flag_name}: {flag_type} | None = Field({default}, description="{description}")'
        )

    # If no fields, add a pass statement
    if len(lines) == 3:
        lines.append("    pass")

    return "\n".join(lines)


def categorize_commands(commands: dict) -> dict[str, list[str]]:
    """Categorize commands into logical groups."""
    categories = {
        "sync": ["sync", "copy", "move", "bisync", "copyto", "moveto"],
        "listing": ["ls", "lsd", "lsl", "lsjson", "lsf", "tree", "ncdu"],
        "check": ["check", "checksum", "cryptcheck", "hashsum", "md5sum", "sha1sum"],
        "config": ["config", "authorize", "obscure", "listremotes"],
        "serve": ["serve", "mount", "nfsmount", "rcd"],
        "utility": [],  # Everything else
    }

    result = {cat: [] for cat in categories}

    for cmd in commands:
        placed = False
        for category, cmd_list in categories.items():
            if cmd in cmd_list:
                result[category].append(cmd)
                placed = True
                break
        if not placed:
            result["utility"].append(cmd)

    return result


def generate_category_file(
    category: str, commands: list[str], all_commands: dict
) -> str:
    """Generate a Python file for a category of commands."""
    lines = [
        '"""Generated Pydantic models for rclone commands."""',
        "# AUTO-GENERATED - DO NOT EDIT",
        "",
        "from pydantic import BaseModel, Field",
        "",
        "",
    ]

    for command in commands:
        if command in all_commands:
            flags = all_commands[command].get("flags", [])
            model_code = generate_option_model(command, flags)
            lines.append(model_code)
            lines.append("\n\n")

    return "\n".join(lines)


def generate_init_file(categories: dict[str, list[str]]) -> str:
    """Generate __init__.py for _generated package."""
    lines = [
        '"""Generated Pydantic models for rclone commands."""',
        "# AUTO-GENERATED - DO NOT EDIT",
        "",
        "from typing import TYPE_CHECKING, Type",
        "",
        "from pydantic import BaseModel",
        "",
    ]

    # Type checking imports
    lines.append("if TYPE_CHECKING:")
    for category, commands in categories.items():
        if commands:
            module_name = f"{category}_commands"
            class_names = [f"{cmd.capitalize()}Options" for cmd in commands]
            lines.append(f"    from .{module_name} import {', '.join(class_names)}")

    lines.append("")
    lines.append("")

    # Lazy loading function
    lines.extend([
        "def get_command_options(command: str) -> Type[BaseModel] | None:",
        '    """Lazy load command options only when needed."""',
    ])

    for category, commands in categories.items():
        if not commands:
            continue
        module_name = f"{category}_commands"
        for cmd in commands:
            class_name = f"{cmd.capitalize()}Options"
            lines.extend([
                f'    if command == "{cmd}":',
                f"        from .{module_name} import {class_name}",
                f"        return {class_name}",
            ])

    lines.append("    return None")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    """Generate code from rclone_help.json."""
    print("🔧 Generating rclone-adapter code...")

    # Load rclone help data
    json_path = Path(__file__).parent / "rclone_help.json"
    with open(json_path) as f:
        data = json.load(f)

    commands = data.get("subcommands", {})
    print(f"📦 Found {len(commands)} rclone subcommands")

    # Categorize commands
    categories = categorize_commands(commands)

    # Create _generated directory
    gen_dir = Path(__file__).parent / "rclone" / "_generated"
    gen_dir.mkdir(exist_ok=True)

    # Generate common.py for shared options
    common_code = dedent('''
        """Common options shared across commands."""
        # AUTO-GENERATED - DO NOT EDIT

        from pydantic import BaseModel, Field


        class CommonOptions(BaseModel):
            """Common options available for all rclone commands."""

            verbose: int = Field(0, description="Print lots more stuff (repeat for more)")
            quiet: bool = Field(False, description="Print as little stuff as possible")
            dry_run: bool = Field(False, description="Do a trial run with no permanent changes")
            interactive: bool = Field(False, description="Enable interactive mode")
            progress: bool = Field(False, description="Show progress during transfer")
    ''').strip()

    with open(gen_dir / "common.py", "w") as f:
        f.write(common_code)
        f.write("\n")

    print("✅ Generated common.py")

    # Generate category files
    for category, cmd_list in categories.items():
        if not cmd_list:
            continue

        filename = f"{category}_commands.py"
        code = generate_category_file(category, cmd_list, commands)

        with open(gen_dir / filename, "w") as f:
            f.write(code)

        print(f"✅ Generated {filename} ({len(cmd_list)} commands)")

    # Generate __init__.py
    init_code = generate_init_file(categories)
    with open(gen_dir / "__init__.py", "w") as f:
        f.write(init_code)

    print("✅ Generated __init__.py")

    print(f"\n🎉 Code generation complete! Generated models for {len(commands)} commands")


if __name__ == "__main__":
    main()
