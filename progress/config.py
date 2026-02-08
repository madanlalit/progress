"""Configuration defaults for progress wallpaper generator."""

# Default color palette
# Color Themes
THEMES = {
    "dark": {
        "bg": (12, 14, 20),  # Ink Black
        "past": (56, 63, 78),  # Slate Grey
        "future": (245, 248, 255, 24),  # Frost White Tint
        "current": (255, 132, 98),  # Ember Coral
        "void": (30, 34, 45),  # Grid filler dots
        "text_primary": (245, 247, 255),
        "text_secondary": (136, 145, 170),
        "text_accent": (255, 151, 122),
        "vignette_color": (1, 5, 12),
        "vignette_strength": 0.48,
        "noise_amount": 22,
        "noise_alpha": 12,
        "bloom": (255, 150, 124, 220),
        "bloom_radius": 1.45,
    },
    "light": {
        "bg": (247, 249, 255),  # Soft Paper White
        "past": (199, 210, 229),  # Cool Mist
        "future": (31, 45, 74, 24),  # Indigo Tint
        "current": (87, 116, 255),  # Periwinkle Blue
        "void": (229, 236, 248),  # Subtle filler dots
        "text_primary": (20, 31, 51),  # Midnight Ink
        "text_secondary": (104, 117, 143),  # Muted Slate
        "text_accent": (87, 116, 255),
        "vignette_color": (187, 198, 225),
        "vignette_strength": 0.22,
        "noise_amount": 16,
        "noise_alpha": 8,
        "bloom": (126, 151, 255, 170),
        "bloom_radius": 1.2,
    },
    "ocean": {
        "bg": (38, 70, 83),  # #264653
        "past": (40, 114, 113),  # #287271
        "future": (233, 196, 106, 24),  # #e9c46a
        "current": (42, 157, 143),  # #2a9d8f
        "void": (28, 56, 67),  # Deepened #264653
        "text_primary": (232, 244, 243),
        "text_secondary": (137, 181, 179),
        "text_accent": (244, 162, 97),  # #f4a261
        "vignette_color": (19, 43, 51),
        "vignette_strength": 0.34,
        "noise_amount": 20,
        "noise_alpha": 11,
        "bloom": (82, 190, 177, 205),
        "bloom_radius": 1.35,
    },
    "forest": {
        "bg": (27, 55, 46),  # Deepened blend from #287271/#2a9d8f
        "past": (95, 148, 121),  # #8ab17d shifted darker
        "future": (233, 196, 106, 22),  # #e9c46a
        "current": (138, 177, 125),  # #8ab17d
        "void": (39, 70, 59),
        "text_primary": (230, 241, 234),
        "text_secondary": (151, 184, 169),
        "text_accent": (239, 179, 102),  # #efb366
        "vignette_color": (11, 31, 24),
        "vignette_strength": 0.36,
        "noise_amount": 20,
        "noise_alpha": 12,
        "bloom": (177, 208, 145, 200),
        "bloom_radius": 1.4,
    },
    "sunset": {
        "bg": (56, 40, 41),  # Warm dusk base
        "past": (121, 86, 80),  # Muted clay
        "future": (244, 162, 97, 24),  # #f4a261
        "current": (231, 111, 81),  # #e76f51
        "void": (74, 55, 56),
        "text_primary": (255, 238, 229),
        "text_secondary": (212, 162, 145),
        "text_accent": (244, 162, 97),  # #f4a261
        "vignette_color": (28, 16, 16),
        "vignette_strength": 0.35,
        "noise_amount": 21,
        "noise_alpha": 12,
        "bloom": (243, 146, 108, 210),
        "bloom_radius": 1.4,
    },
    "mono": {
        "bg": (30, 32, 36),  # Neutral graphite
        "past": (97, 101, 112),  # Cool gray
        "future": (231, 234, 242, 22),  # Silver mist
        "current": (247, 248, 251),  # Bright silver
        "void": (49, 52, 59),
        "text_primary": (246, 248, 251),
        "text_secondary": (168, 174, 187),
        "text_accent": (247, 248, 251),
        "vignette_color": (8, 9, 11),
        "vignette_strength": 0.44,
        "noise_amount": 18,
        "noise_alpha": 9,
        "bloom": (246, 248, 252, 165),
        "bloom_radius": 1.3,
    },
    "linen": {
        "bg": (244, 237, 237),  # #f4eded
        "past": (214, 201, 199),  # Warm paper tone
        "future": (70, 77, 119, 22),  # #464d77
        "current": (54, 130, 127),  # #36827f
        "void": (229, 217, 215),
        "text_primary": (64, 70, 101),
        "text_secondary": (135, 113, 102),  # #877666
        "text_accent": (249, 219, 109),  # #f9db6d
        "vignette_color": (224, 209, 207),
        "vignette_strength": 0.2,
        "noise_amount": 14,
        "noise_alpha": 7,
        "bloom": (80, 156, 152, 170),
        "bloom_radius": 1.15,
    },
    "pastel": {
        "bg": (255, 255, 255),  # #ffffff
        "past": (212, 212, 252),  # #d4d4fd
        "future": (204, 227, 216, 28),  # #cce3d8
        "current": (255, 192, 192),  # #ffd4d4 adjusted for contrast
        "void": (255, 242, 230),  # #ffeed6 tint
        "text_primary": (65, 71, 94),
        "text_secondary": (133, 141, 170),
        "text_accent": (227, 127, 152),
        "vignette_color": (226, 230, 245),
        "vignette_strength": 0.16,
        "noise_amount": 12,
        "noise_alpha": 6,
        "bloom": (255, 205, 205, 155),
        "bloom_radius": 1.05,
    },
    "bloom": {
        "bg": (235, 244, 248),  # #ebf4f8
        "past": (187, 205, 217),  # Mist blue
        "future": (13, 66, 100, 22),  # #0d4264
        "current": (240, 81, 145),  # #f05191
        "void": (218, 231, 237),
        "text_primary": (23, 53, 78),
        "text_secondary": (100, 123, 143),
        "text_accent": (192, 114, 145),  # #c07291
        "vignette_color": (186, 205, 216),
        "vignette_strength": 0.18,
        "noise_amount": 13,
        "noise_alpha": 7,
        "bloom": (240, 104, 160, 175),
        "bloom_radius": 1.1,
    },
    "candy": {
        "bg": (198, 222, 225),  # #c6dee1
        "past": (160, 188, 191),  # Muted cyan
        "future": (41, 115, 115, 18),  # #297373
        "current": (233, 109, 97),  # #e96d61
        "void": (180, 207, 210),
        "text_primary": (26, 68, 68),
        "text_secondary": (79, 112, 112),
        "text_accent": (247, 179, 43),  # #f7b32b
        "vignette_color": (151, 181, 185),
        "vignette_strength": 0.2,
        "noise_amount": 14,
        "noise_alpha": 7,
        "bloom": (240, 134, 124, 175),
        "bloom_radius": 1.12,
    },
    "cream": {
        "bg": (255, 241, 230),  # #fff1e6
        "past": (230, 214, 198),  # Warm neutral
        "future": (38, 70, 83, 20),  # #264653
        "current": (244, 162, 97),  # #f4a261
        "void": (245, 230, 216),
        "text_primary": (67, 72, 83),
        "text_secondary": (130, 121, 112),
        "text_accent": (231, 111, 81),  # #e76f51
        "vignette_color": (231, 215, 197),
        "vignette_strength": 0.18,
        "noise_amount": 12,
        "noise_alpha": 6,
        "bloom": (246, 182, 126, 160),
        "bloom_radius": 1.08,
    },
}

DEFAULT_THEME = "dark"
DEFAULT_CONFIG = THEMES[DEFAULT_THEME]

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
