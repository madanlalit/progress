"""Configuration defaults for progress wallpaper generator."""

# Default color palette
DEFAULT_CONFIG = {
    "bg": (18, 18, 20),  # Deep Matte Black
    "past": (50, 50, 55),  # Dark Grey
    "future": (255, 255, 255, 15),  # Subtle White
    "current": (255, 115, 80),  # Coral
    "void": (25, 25, 28),  # NEW: Color for the empty dots to complete the grid
    "text_primary": (255, 255, 255),
    "text_secondary": (120, 120, 130),
    "text_accent": (255, 115, 80),
}

# Font URLs
FONTS = {
    "hero": {
        "url": "https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-ExtraBold.ttf",
        "filename": "Montserrat-ExtraBold.ttf",
    },
    "data": {
        "url": "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Bold.ttf",
        "filename": "JetBrainsMono-Bold.ttf",
    },
}

DEFAULT_WIDTH = 5120
DEFAULT_HEIGHT = 2880

# SPACIOUS / BOLD CONFIGURATION
MODE_CONFIG = {
    "day": {
        "dots_per_row": 28,  # 28 cols x 12 rows = 336 slots (Perfect for 365 days)
        "dot_size": 22,
        "gap": 70,
    },
    "week": {
        "dots_per_row": 13,  # 13 cols x 4 rows = 52 slots (Perfect square)
        "dot_size": 45,
        "gap": 130,
    },
    "month": {"dots_per_row": 6, "dot_size": 120, "gap": 280},
}
