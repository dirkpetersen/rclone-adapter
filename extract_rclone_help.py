#!/usr/bin/env python3
"""Extract rclone subcommands and their help text into JSON and YAML files."""

import subprocess
import json
import re
from pathlib import Path

def get_rclone_help():
    """Get the main rclone help output."""
    result = subprocess.run(['rclone', '--help'], capture_output=True, text=True)
    return result.stdout + result.stderr

def extract_subcommands(help_text):
    """Extract subcommand names from help text."""
    subcommands = []
    in_commands_section = False

    for line in help_text.split('\n'):
        if 'Available commands:' in line:
            in_commands_section = True
            continue

        if in_commands_section:
            if line.startswith('Use "'):
                break
            if line.strip() and not line.startswith(' '):
                break

            # Parse command line: "  command       Description here"
            match = re.match(r'\s+(\w+)\s+(.+)', line)
            if match:
                subcommands.append(match.group(1).strip())

    return subcommands

def get_subcommand_help(subcommand):
    """Get help text for a specific subcommand."""
    result = subprocess.run(['rclone', subcommand, '--help'],
                          capture_output=True, text=True, timeout=10)
    return result.stdout + result.stderr

def extract_flags_from_help(help_text):
    """Extract flags and options from help text."""
    flags = []
    in_flags_section = False

    for line in help_text.split('\n'):
        if 'Flags:' in line or 'Global Flags:' in line:
            in_flags_section = True
            continue

        if in_flags_section:
            if line.startswith('Use "') or (line and not line.startswith(' ')):
                break

            # Parse flag line: "  -f, --flag      Description"
            match = re.match(r'\s+(-\S+(?:,\s+-?-\S+)?)\s+(.+)', line)
            if match:
                flag_str = match.group(1).strip()
                description = match.group(2).strip()
                flags.append({
                    'flag': flag_str,
                    'description': description
                })

    return flags

def main():
    print("Extracting rclone help structure...")

    # Get main help
    main_help = get_rclone_help()
    subcommands_list = extract_subcommands(main_help)

    print(f"Found {len(subcommands_list)} subcommands")

    # Build structure
    rclone_structure = {
        'version': '1.0',
        'subcommands': {}
    }

    for i, subcommand in enumerate(subcommands_list, 1):
        print(f"[{i}/{len(subcommands_list)}] Extracting help for '{subcommand}'...")
        try:
            subcommand_help = get_subcommand_help(subcommand)
            flags = extract_flags_from_help(subcommand_help)

            # Extract short description from help text
            description = ""
            for line in subcommand_help.split('\n')[:5]:
                if line.strip() and not line.startswith('Usage:'):
                    description = line.strip()
                    break

            rclone_structure['subcommands'][subcommand] = {
                'description': description,
                'help_text': subcommand_help,
                'flags': flags
            }
        except subprocess.TimeoutExpired:
            print(f"  ⚠ Timeout for '{subcommand}'")
        except Exception as e:
            print(f"  ⚠ Error for '{subcommand}': {e}")

    # Save to JSON
    json_path = Path('/home/dp/gh/rclone-adapter/rclone_help.json')
    with open(json_path, 'w') as f:
        json.dump(rclone_structure, f, indent=2)
    print(f"\n✓ Saved to {json_path}")
    print(f"Extracted {len(rclone_structure['subcommands'])} subcommands successfully!")

if __name__ == '__main__':
    main()
