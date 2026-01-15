"""Progress - A beautiful macOS wallpaper showing your yearly progress."""

__version__ = "1.0.0"
__author__ = "Progress Contributors"

from .generator import WallpaperGenerator
from .config import DEFAULT_CONFIG, MODE_CONFIG

__all__ = ["WallpaperGenerator", "DEFAULT_CONFIG", "MODE_CONFIG"]
