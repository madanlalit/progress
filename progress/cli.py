"""CLI interface for progress wallpaper generator."""

import argparse
import sys
import os
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Tuple

from . import __version__
from .generator import WallpaperGenerator


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def set_wallpaper_macos(image_path: str) -> bool:
    """Set wallpaper on macOS using AppleScript via System Events (supports multiple displays)."""
    abs_path = os.path.abspath(image_path)
    script = f'tell application "System Events" to tell every desktop to set picture to POSIX file "{abs_path}"'

    try:
        subprocess.run(["osascript", "-e", script], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def install_launchagent() -> bool:
    """Install LaunchAgent for daily wallpaper updates."""
    home = Path.home()
    launch_agents_dir = home / "Library" / "LaunchAgents"
    plist_path = launch_agents_dir / "com.progress.daily.plist"

    # Get the progress executable path
    progress_bin = shutil.which("progress")
    if not progress_bin:
        print("Error: Could not find progress command in PATH")
        return False

    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.progress.daily</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>{progress_bin}</string>
        <string>generate</string>
    </array>
    
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>0</integer>
        <key>Minute</key>
        <integer>1</integer>
    </dict>
    
    <key>StandardOutPath</key>
    <string>{home}/.progress/logs/stdout.log</string>
    
    <key>StandardErrorPath</key>
    <string>{home}/.progress/logs/stderr.log</string>
    
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""

    try:
        # Create log directory
        log_dir = home / ".progress" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Write plist file
        launch_agents_dir.mkdir(parents=True, exist_ok=True)
        plist_path.write_text(plist_content)

        # Load the LaunchAgent
        subprocess.run(["launchctl", "load", str(plist_path)], check=True)

        print(f"✓ LaunchAgent installed successfully")
        print(f"  Wallpaper will update daily at 12:01 AM")
        print(f"  Logs: {log_dir}")
        return True
    except Exception as e:
        print(f"✗ Failed to install LaunchAgent: {e}")
        return False


def uninstall_launchagent() -> bool:
    """Uninstall the LaunchAgent."""
    plist_path = Path.home() / "Library" / "LaunchAgents" / "com.progress.daily.plist"

    try:
        if plist_path.exists():
            # Unload first
            subprocess.run(
                ["launchctl", "unload", str(plist_path)], capture_output=True
            )
            # Remove file
            plist_path.unlink()
            print("✓ LaunchAgent uninstalled successfully")
        else:
            print("LaunchAgent not found (already uninstalled)")
        return True
    except Exception as e:
        print(f"✗ Failed to uninstall LaunchAgent: {e}")
        return False


def generate_command(args):
    """Handle the generate command."""
    # Parse custom colors if provided
    bg_color = hex_to_rgb(args.bg_color) if args.bg_color else None
    past_color = hex_to_rgb(args.past_color) if args.past_color else None
    current_color = hex_to_rgb(args.current_color) if args.current_color else None

    # Create generator
    try:
        generator = WallpaperGenerator(
            mode=args.mode,
            bg_color=bg_color,
            past_color=past_color,
            current_color=current_color,
            dot_size=args.dot_size,
        )

        # Generate wallpaper
        output_path = generator.generate(args.output)

        progress_pct = (generator.current / generator.total) * 100
        print(f"✨ Wallpaper generated successfully!")
        print(f"   Mode: {args.mode.upper()}")
        print(f"   {generator.label} {generator.current} of {generator.total}")
        print(f"   Progress: {progress_pct:.1f}%")
        print(f"   Output: {output_path}")

        # Set as wallpaper unless --no-set flag is used
        if not args.no_set:
            if set_wallpaper_macos(output_path):
                print(f"✓ Wallpaper set successfully")
            else:
                print(f"✗ Failed to set wallpaper (run with --no-set to only generate)")

        return 0
    except Exception as e:
        print(f"✗ Error generating wallpaper: {e}", file=sys.stderr)
        return 1


def install_command(args):
    """Handle the install command."""
    if not install_launchagent():
        return 1

    # Generate initial wallpaper immediately
    print("\n✨ Generating initial wallpaper...")
    try:
        # Default to week mode for initial run
        generator = WallpaperGenerator(mode="day")

        # Use the standard path
        output_dir = Path.home() / ".progress"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(output_dir / "wallpaper.png")

        # Generate and set
        generator.generate(output_path)
        if set_wallpaper_macos(output_path):
            print(f"✓ Initial wallpaper set successfully")

    except Exception as e:
        print(f"⚠ Could not generate initial wallpaper: {e}")

    return 0


def uninstall_command(args):
    """Handle the uninstall command."""
    return 0 if uninstall_launchagent() else 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="progress",
        description="Generate beautiful year calendar wallpapers showing your progress",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  progress generate                                    # Generate day mode wallpaper (365 dots)
  progress generate --mode week                        # Generate week mode (52 dots)
  progress generate --mode month --output ~/wall.png   # Month mode with custom path
  progress generate --bg-color "#1a1a1c"               # Custom background color
  progress install                                     # Install daily auto-update
  progress uninstall                                   # Remove auto-update
        """,
    )

    parser.add_argument(
        "--version", action="version", version=f"progress {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate wallpaper")
    generate_parser.add_argument(
        "--mode",
        "-m",
        choices=["day", "week", "month"],
        default="day",
        help="Display mode (default: day)",
    )
    generate_parser.add_argument(
        "--output",
        "-o",
        default="progress_wallpaper.png",
        help="Output file path (default: progress_wallpaper.png)",
    )
    generate_parser.add_argument(
        "--bg-color", help='Background color (hex, e.g., "#1a1a1c")'
    )
    generate_parser.add_argument("--past-color", help="Past periods color (hex)")
    generate_parser.add_argument("--current-color", help="Current period color (hex)")
    generate_parser.add_argument("--dot-size", type=int, help="Override dot size")
    generate_parser.add_argument(
        "--no-set", action="store_true", help="Generate only, don't set as wallpaper"
    )
    generate_parser.set_defaults(func=generate_command)

    # Install command
    install_parser = subparsers.add_parser("install", help="Install daily auto-update")
    install_parser.set_defaults(func=install_command)

    # Uninstall command
    uninstall_parser = subparsers.add_parser(
        "uninstall", help="Uninstall daily auto-update"
    )
    uninstall_parser.set_defaults(func=uninstall_command)

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # Execute command
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
