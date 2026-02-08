"""Progress - A beautiful macOS wallpaper showing your yearly progress."""

__version__ = "1.3.1"
__author__ = "Lalit Madan"
__license__ = "MIT"
__url__ = "https://github.com/madanlalit/progress"

from .config import DEFAULT_CONFIG, MODE_CONFIG
from .generator import WallpaperGenerator

__all__ = ["WallpaperGenerator", "DEFAULT_CONFIG", "MODE_CONFIG"]
