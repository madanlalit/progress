"""
Core wallpaper generation logic - Perfect Grid Edition.
"""

import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import datetime
import math
from typing import Tuple, Optional
from pathlib import Path

from .config import (
    THEMES,
    DEFAULT_THEME,
    MODE_CONFIG,
    FONTS,
    DEFAULT_WIDTH,
    DEFAULT_HEIGHT,
)


class WallpaperGenerator:
    """Generates ultra-minimal year calendar wallpapers."""

    @staticmethod
    def _clamp_byte(value: int) -> int:
        return max(0, min(255, int(value)))

    @classmethod
    def _as_rgba(
        cls, color: Tuple[int, ...], fallback_alpha: int = 255
    ) -> Tuple[int, int, int, int]:
        if len(color) == 4:
            r, g, b, a = color
            return (
                cls._clamp_byte(r),
                cls._clamp_byte(g),
                cls._clamp_byte(b),
                cls._clamp_byte(a),
            )

        if len(color) == 3:
            r, g, b = color
            return (
                cls._clamp_byte(r),
                cls._clamp_byte(g),
                cls._clamp_byte(b),
                cls._clamp_byte(fallback_alpha),
            )

        raise ValueError("Color values must be RGB or RGBA tuples")

    def __init__(
        self,
        mode: str = "week",
        theme: str = DEFAULT_THEME,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        bg_color: Optional[Tuple[int, int, int]] = None,
        past_color: Optional[Tuple[int, int, int]] = None,
        current_color: Optional[Tuple[int, int, int]] = None,
        future_color: Optional[Tuple[int, ...]] = None,
        dot_size: Optional[int] = None,
    ):
        """Initialize the wallpaper generator."""
        self.mode = mode
        self.scale_factor = 4
        self.target_width = width
        self.target_height = height
        self.width = width * self.scale_factor
        self.height = height * self.scale_factor

        if theme not in THEMES:
            raise ValueError(
                f"Invalid theme: {theme}. Available: {', '.join(THEMES.keys())}"
            )

        theme_cfg = THEMES[theme]

        # Colors
        self.bg_color = bg_color or theme_cfg["bg"]
        self.past_color = past_color or theme_cfg["past"]
        self.current_color = current_color or theme_cfg["current"]
        future_fallback_alpha = theme_cfg.get("future_alpha", 24)
        self.future_color = self._as_rgba(
            future_color or theme_cfg["future"], fallback_alpha=future_fallback_alpha
        )
        # The color for dots that exist just to fill the grid square
        self.void_color = theme_cfg.get("void", (25, 25, 25))

        self.text_primary = theme_cfg["text_primary"]
        self.text_secondary = theme_cfg["text_secondary"]
        self.text_accent = theme_cfg["text_accent"]

        if current_color is not None:
            self.bloom_color = self._as_rgba(current_color, fallback_alpha=210)
        else:
            self.bloom_color = self._as_rgba(
                theme_cfg.get("bloom", self.current_color), fallback_alpha=210
            )
        self.bloom_radius = float(theme_cfg.get("bloom_radius", 1.5))

        self.vignette_color = theme_cfg.get("vignette_color", (0, 0, 0))
        self.vignette_strength = max(0.0, min(1.0, theme_cfg.get("vignette_strength", 0.5)))

        self.noise_amount = max(1, int(theme_cfg.get("noise_amount", 25)))
        self.noise_alpha = self._clamp_byte(theme_cfg.get("noise_alpha", 15))

        if mode not in MODE_CONFIG:
            raise ValueError(f"Invalid mode: {mode}")

        mode_cfg = MODE_CONFIG[mode]
        self.dots_per_row = mode_cfg["dots_per_row"]

        base_size = dot_size or mode_cfg["dot_size"]
        self.dot_size = base_size * self.scale_factor
        self.gap = mode_cfg["gap"] * self.scale_factor

        self.today = datetime.date.today()
        self.year = self.today.year
        self.day_of_year = self.today.timetuple().tm_yday
        self.current_week = self.today.isocalendar().week
        self.current_month = self.today.month

        if mode == "day":
            self.total = 365
            self.current = self.day_of_year
            self.label = "Day"
        elif mode == "week":
            self.total = 52
            self.current = self.current_week
            self.label = "Week"
        else:
            self.total = 12
            self.current = self.current_month
            self.label = "Month"

    def _get_font(self, font_key: str, size: int) -> ImageFont.ImageFont:
        font_dir = Path.home() / ".progress" / "fonts"
        font_dir.mkdir(parents=True, exist_ok=True)
        font_info = FONTS[font_key]
        font_path = font_dir / font_info["filename"]

        if not font_path.exists():
            print(f"⬇️  Downloading {font_info['filename']}...")
            try:
                urllib.request.urlretrieve(font_info["url"], font_path)
            except Exception:
                return ImageFont.load_default()

        try:
            return ImageFont.truetype(str(font_path), size * self.scale_factor)
        except OSError:
            return ImageFont.load_default()

    def _draw_vignette(self, img: Image.Image) -> None:
        gradient = Image.new("L", (self.width, self.height), 0)
        draw = ImageDraw.Draw(gradient)
        cx, cy = self.width // 2, self.height // 2
        max_radius = int(math.sqrt(cx**2 + cy**2))

        step = max(1, max_radius // 150)
        for r in range(max_radius, 0, -step):
            alpha = int(255 * (1 - (r / max_radius) ** 1.5))
            alpha = 255 - alpha
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=alpha)

        overlay = Image.new("RGB", (self.width, self.height), self.vignette_color)
        mask = gradient.point(lambda p: int(p * self.vignette_strength))
        img.paste(overlay, (0, 0), mask)

    def _add_noise(self, img: Image.Image) -> Image.Image:
        width, height = img.size
        noise = Image.effect_noise((width, height), self.noise_amount)
        noise = noise.convert("RGBA")
        img = img.convert("RGBA")
        noise.putalpha(self.noise_alpha)
        return Image.alpha_composite(img, noise).convert("RGB")

    def _create_bloom(self, size: int, color: Tuple[int, ...]) -> Image.Image:
        pad = size * 6
        glow_img = Image.new("RGBA", (pad * 2, pad * 2), (0, 0, 0, 0))
        draw = ImageDraw.Draw(glow_img)
        draw.ellipse(
            (pad - size, pad - size, pad + size, pad + size),
            fill=self._as_rgba(color, fallback_alpha=210),
        )
        blur_radius = size * self.bloom_radius
        return glow_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    def generate(self, output_path: str = "progress_wallpaper.png") -> str:
        img = Image.new("RGB", (self.width, self.height), self.bg_color)
        self._draw_vignette(img)
        draw = ImageDraw.Draw(img, "RGBA")

        title_font = self._get_font("hero", 260)
        date_font = self._get_font("data", 90)
        info_font = self._get_font("data", 45)

        # --- TEXT MEASUREMENT ---
        year_text = str(self.year)
        year_bbox = draw.textbbox((0, 0), year_text, font=title_font)
        year_w = year_bbox[2] - year_bbox[0]
        year_h = year_bbox[3] - year_bbox[1]

        date_text = self.today.strftime("%B %d").upper()
        date_bbox = draw.textbbox((0, 0), date_text, font=date_font)
        date_w = date_bbox[2] - date_bbox[0]
        date_h = date_bbox[3] - date_bbox[1]

        progress_pct = (self.current / self.total) * 100
        bottom_text = f"{self.label.upper()} {self.current} / {self.total}   //   {progress_pct:.1f}%"
        bottom_bbox = draw.textbbox((0, 0), bottom_text, font=info_font)
        bottom_w = bottom_bbox[2] - bottom_bbox[0]
        bottom_h = bottom_bbox[3] - bottom_bbox[1]

        # --- GRID CALCULATION (PERFECT RECTANGLE LOGIC) ---
        # 1. Calculate how many rows we need for the actual data
        rows = (self.total + self.dots_per_row - 1) // self.dots_per_row

        # 2. To make equal dots, we must draw the full rectangle
        # Total slots = rows * columns
        total_slots_in_grid = rows * self.dots_per_row

        grid_width = (self.dots_per_row - 1) * self.gap + (self.dot_size * 2)
        grid_height = (rows - 1) * self.gap + (self.dot_size * 2)

        # --- SPACING ---
        s = self.scale_factor
        # INCREASED GAP HERE:
        year_date_gap = 120 * s  # Increased from 50 to 120
        header_gap = 200 * s
        footer_gap = 160 * s

        total_content_height = (
            year_h
            + year_date_gap
            + date_h
            + header_gap
            + grid_height
            + footer_gap
            + bottom_h
        )
        start_y = (self.height - total_content_height) // 2

        # --- POSITIONING ---
        year_x = (self.width - year_w) // 2
        year_y = start_y

        date_x = (self.width - date_w) // 2
        date_y = year_y + year_h + year_date_gap

        grid_start_x = (self.width - grid_width) // 2 + self.dot_size
        grid_start_y = date_y + date_h + header_gap + self.dot_size

        bottom_x = (self.width - bottom_w) // 2
        bottom_y = grid_start_y + grid_height - self.dot_size + footer_gap

        # --- DRAW TEXT ---
        draw.text((year_x, year_y), year_text, fill=self.text_primary, font=title_font)
        draw.text((date_x, date_y), date_text, fill=self.text_accent, font=date_font)

        # --- DRAW DOTS ---
        bloom_layer = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))

        # Loop through the FULL GRID (total_slots_in_grid) to ensure a perfect rectangle
        for i in range(1, total_slots_in_grid + 1):
            row = (i - 1) // self.dots_per_row
            col = (i - 1) % self.dots_per_row

            cx = grid_start_x + col * self.gap
            cy = grid_start_y + row * self.gap
            bbox = (
                cx - self.dot_size,
                cy - self.dot_size,
                cx + self.dot_size,
                cy + self.dot_size,
            )

            if i <= self.total:
                # Actual Calendar Days
                if i < self.current:
                    draw.ellipse(bbox, fill=self.past_color)
                elif i == self.current:
                    bloom = self._create_bloom(self.dot_size, self.bloom_color)
                    bw, bh = bloom.size
                    bloom_layer.paste(
                        bloom, (int(cx - bw / 2), int(cy - bh / 2)), bloom
                    )
                    draw.ellipse(bbox, fill=self.current_color)
                else:
                    draw.ellipse(bbox, fill=self.future_color)
            else:
                # "Ghost Dots" (Fillers to make the grid rectangular)
                # We draw them using the 'void' color so they are barely visible
                # but maintain the structure
                draw.ellipse(bbox, fill=self.void_color)

        img = Image.alpha_composite(img.convert("RGBA"), bloom_layer)

        draw = ImageDraw.Draw(img)
        draw.text(
            (bottom_x, bottom_y), bottom_text, fill=self.text_secondary, font=info_font
        )

        img = self._add_noise(img)
        final_img = img.resize(
            (self.target_width, self.target_height), resample=Image.Resampling.LANCZOS
        )

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        final_img.save(output_path, quality=100, optimize=True)

        return output_path
