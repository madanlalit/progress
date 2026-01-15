"""Configuration defaults for progress wallpaper generator."""

# Default color palette
DEFAULT_CONFIG = {
    "bg": (18, 18, 20),  # Pure dark background
    "past": (90, 90, 95),  # Subtle gray for past
    "future": (255, 255, 255, 30),  # Very subtle white for future
    "current": (255, 115, 80),  # Vibrant coral for current
    "text_primary": (245, 245, 250),  # Almost white
    "text_secondary": (140, 140, 150),  # Dimmed text
    "text_accent": (255, 115, 80),  # Coral accent
}

# Resolution defaults
DEFAULT_WIDTH = 5120
DEFAULT_HEIGHT = 2880

# Mode-specific configuration
MODE_CONFIG = {
    "day": {"dots_per_row": 73, "dot_size": 14, "gap": 24},
    "week": {"dots_per_row": 52, "dot_size": 22, "gap": 55},
    "month": {"dots_per_row": 12, "dot_size": 50, "gap": 140},
}
