"""Progress - A beautiful macOS wallpaper showing your yearly progress."""

__version__ = "1.3.0"
__author__ = "Lalit Madan"
__license__ = "MIT"
__url__ = "https://github.com/madanlalit/progress"

from .generator import WallpaperGenerator, DEFAULT_CONFIG, MODE_CONFIG

__all__ = ["WallpaperGenerator", "DEFAULT_CONFIG", "MODE_CONFIG"]
