"""
Core wallpaper generation logic - Perfect Grid Edition.
"""

import datetime
import math
import os
import urllib.request
from pathlib import Path
from typing import Dict, Optional, Tuple

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .config import (
    DEFAULT_HEIGHT,
    DEFAULT_THEME,
    DEFAULT_WIDTH,
    FONTS,
    LAYOUT_CONFIG,
    LAYOUT_SAFE_FRAME,
    MODE_CONFIG,
    THEMES,
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

    @staticmethod
    def _clamp(value: int, min_value: int, max_value: int) -> int:
        if min_value > max_value:
            return min_value
        return max(min_value, min(max_value, int(value)))

    @staticmethod
    def _measure_text(
        draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont
    ) -> Tuple[int, int]:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    def __init__(
        self,
        mode: str = "week",
        theme: str = DEFAULT_THEME,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        layout: str = "centered",
        show_metadata: bool = False,
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

        if layout not in LAYOUT_CONFIG:
            raise ValueError(
                f"Invalid layout: {layout}. Available: {', '.join(LAYOUT_CONFIG.keys())}"
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
        self.vignette_strength = max(
            0.0, min(1.0, theme_cfg.get("vignette_strength", 0.5))
        )

        self.noise_amount = max(1, int(theme_cfg.get("noise_amount", 25)))
        self.noise_alpha = self._clamp_byte(theme_cfg.get("noise_alpha", 15))

        if mode not in MODE_CONFIG:
            raise ValueError(f"Invalid mode: {mode}")

        mode_cfg = MODE_CONFIG[mode]
        self.layout = layout
        self.show_metadata = show_metadata
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

    def _safe_frame(self) -> Tuple[int, int, int, int]:
        safe_x = int(self.width * LAYOUT_SAFE_FRAME["x"])
        safe_y = int(self.height * LAYOUT_SAFE_FRAME["y"])
        safe_w = int(self.width * LAYOUT_SAFE_FRAME["w"])
        safe_h = int(self.height * LAYOUT_SAFE_FRAME["h"])
        return safe_x, safe_y, safe_w, safe_h

    def _compute_grid_metrics(self) -> Dict[str, int]:
        rows = (self.total + self.dots_per_row - 1) // self.dots_per_row
        total_slots_in_grid = rows * self.dots_per_row
        grid_width = (self.dots_per_row - 1) * self.gap + (self.dot_size * 2)
        grid_height = (rows - 1) * self.gap + (self.dot_size * 2)
        return {
            "rows": rows,
            "total_slots_in_grid": total_slots_in_grid,
            "grid_width": grid_width,
            "grid_height": grid_height,
        }

    def _build_metadata_text(self) -> str:
        weekday = self.today.strftime("%A").upper()
        iso_week = self.today.isocalendar().week
        remaining = max(self.total - self.current, 0)
        return (
            f"{weekday}  //  ISO WK {iso_week:02d}  //  "
            f"{remaining} {self.label.upper()} LEFT"
        )

    def _measure_text_blocks(
        self,
        draw: ImageDraw.ImageDraw,
        year_text: str,
        date_text: str,
        bottom_text: str,
        metadata_text: str,
        title_font: ImageFont.ImageFont,
        date_font: ImageFont.ImageFont,
        info_font: ImageFont.ImageFont,
        metadata_font: ImageFont.ImageFont,
    ) -> Dict[str, int]:
        year_w, year_h = self._measure_text(draw, year_text, title_font)
        date_w, date_h = self._measure_text(draw, date_text, date_font)
        bottom_w, bottom_h = self._measure_text(draw, bottom_text, info_font)
        metadata_w, metadata_h = self._measure_text(draw, metadata_text, metadata_font)
        return {
            "year_w": year_w,
            "year_h": year_h,
            "date_w": date_w,
            "date_h": date_h,
            "bottom_w": bottom_w,
            "bottom_h": bottom_h,
            "metadata_w": metadata_w,
            "metadata_h": metadata_h,
        }

    def _compute_positions(
        self, layout_name: str, metrics: Dict[str, int], show_metadata: bool
    ) -> Dict[str, Optional[int]]:
        if layout_name not in LAYOUT_CONFIG:
            raise ValueError(f"Invalid layout: {layout_name}")

        cfg = LAYOUT_CONFIG[layout_name]
        s = self.scale_factor

        year_w = metrics["year_w"]
        year_h = metrics["year_h"]
        date_w = metrics["date_w"]
        date_h = metrics["date_h"]
        bottom_w = metrics["bottom_w"]
        bottom_h = metrics["bottom_h"]
        metadata_w = metrics["metadata_w"]
        metadata_h = metrics["metadata_h"]
        grid_width = metrics["grid_width"]
        grid_height = metrics["grid_height"]

        safe_x, safe_y, safe_w, safe_h = self._safe_frame()
        safe_right = safe_x + safe_w
        safe_bottom = safe_y + safe_h

        metadata_x: Optional[int] = None
        metadata_y: Optional[int] = None

        if layout_name == "centered":
            year_date_gap = cfg["year_date_gap"] * s
            header_gap = cfg["header_gap"] * s
            footer_gap = cfg["footer_gap"] * s
            meta_gap = cfg["meta_gap"] * s

            total_content_height = (
                year_h
                + year_date_gap
                + date_h
                + (meta_gap + metadata_h if show_metadata else 0)
                + header_gap
                + grid_height
                + footer_gap
                + bottom_h
            )
            start_y = (self.height - total_content_height) // 2

            year_x = (self.width - year_w) // 2
            year_y = start_y

            date_x = (self.width - date_w) // 2
            date_y = year_y + year_h + year_date_gap

            if show_metadata:
                metadata_x = (self.width - metadata_w) // 2
                metadata_y = date_y + date_h + meta_gap
                grid_top = metadata_y + metadata_h + header_gap
            else:
                grid_top = date_y + date_h + header_gap

            grid_left = (self.width - grid_width) // 2
            bottom_x = (self.width - bottom_w) // 2
            bottom_y = grid_top + grid_height + footer_gap

        elif layout_name in {"split-left", "split-right"}:
            col_gap = int(self.width * cfg["col_gap_ratio"])
            grid_col_w = int(safe_w * cfg["grid_ratio"])
            text_col_w = safe_w - grid_col_w - col_gap

            split_left = layout_name == "split-left"
            if split_left:
                text_col_x = safe_x
                grid_col_x = safe_x + text_col_w + col_gap
            else:
                grid_col_x = safe_x
                text_col_x = safe_x + grid_col_w + col_gap

            grid_left = grid_col_x + (grid_col_w - grid_width) // 2
            grid_top = safe_y + (safe_h - grid_height) // 2

            year_date_gap = cfg["year_date_gap"] * s
            stack_gap = cfg["stack_gap"] * s
            meta_gap = cfg["meta_gap"] * s
            total_text_h = (
                year_h
                + year_date_gap
                + date_h
                + (meta_gap + metadata_h if show_metadata else 0)
                + stack_gap
                + bottom_h
            )
            text_start_y = safe_y + (safe_h - total_text_h) // 2

            year_x = text_col_x + (text_col_w - year_w) // 2
            year_y = text_start_y

            date_x = text_col_x + (text_col_w - date_w) // 2
            date_y = year_y + year_h + year_date_gap

            if show_metadata:
                metadata_x = text_col_x + (text_col_w - metadata_w) // 2
                metadata_y = date_y + date_h + meta_gap
                bottom_y = metadata_y + metadata_h + stack_gap
            else:
                bottom_y = date_y + date_h + stack_gap

            bottom_x = text_col_x + (text_col_w - bottom_w) // 2

        elif layout_name == "bottom-band":
            year_date_gap = cfg["year_date_gap"] * s
            meta_gap = cfg["meta_gap"] * s
            content_gap = cfg["content_gap"] * s
            header_offset = int(safe_h * cfg["header_offset_ratio"])
            footer_padding = int(safe_h * cfg["footer_padding_ratio"])

            year_x = (self.width - year_w) // 2
            year_y = safe_y + header_offset
            date_x = (self.width - date_w) // 2
            date_y = year_y + year_h + year_date_gap

            if show_metadata:
                metadata_x = (self.width - metadata_w) // 2
                metadata_y = date_y + date_h + meta_gap
                header_bottom = metadata_y + metadata_h
            else:
                header_bottom = date_y + date_h

            bottom_x = (self.width - bottom_w) // 2
            bottom_y = safe_bottom - bottom_h - footer_padding

            grid_left = safe_x + (safe_w - grid_width) // 2
            grid_top = int(self.height * cfg["grid_center_y_ratio"] - grid_height / 2)

            min_grid_top = header_bottom + content_gap
            max_grid_top = bottom_y - content_gap - grid_height
            if max_grid_top >= min_grid_top:
                grid_top = self._clamp(grid_top, min_grid_top, max_grid_top)
            else:
                grid_top = min_grid_top

        elif layout_name == "top-band":
            year_date_gap = cfg["year_date_gap"] * s
            meta_gap = cfg["meta_gap"] * s
            content_gap = cfg["content_gap"] * s
            below_grid_gap = cfg["below_grid_gap"] * s
            footer_padding = int(safe_h * cfg["footer_padding_ratio"])

            grid_left = safe_x + (safe_w - grid_width) // 2
            grid_top = int(self.height * cfg["grid_center_y_ratio"] - grid_height / 2)

            bottom_x = (self.width - bottom_w) // 2
            bottom_y = safe_bottom - bottom_h - footer_padding

            block_h = year_h + year_date_gap + date_h + (
                meta_gap + metadata_h if show_metadata else 0
            )
            min_year_y = grid_top + grid_height + below_grid_gap
            max_year_y = bottom_y - content_gap - block_h
            if max_year_y >= min_year_y:
                year_y = min_year_y + (max_year_y - min_year_y) // 3
            else:
                year_y = min_year_y

            year_x = (self.width - year_w) // 2
            date_x = (self.width - date_w) // 2
            date_y = year_y + year_h + year_date_gap

            if show_metadata:
                metadata_x = (self.width - metadata_w) // 2
                metadata_y = date_y + date_h + meta_gap

        else:
            raise ValueError(f"Invalid layout: {layout_name}")

        # Keep the grid inside safe frame when there is enough space.
        if safe_w > grid_width:
            grid_left = self._clamp(grid_left, safe_x, safe_right - grid_width)
        if safe_h > grid_height:
            grid_top = self._clamp(grid_top, safe_y, safe_bottom - grid_height)

        grid_start_x = grid_left + self.dot_size
        grid_start_y = grid_top + self.dot_size

        return {
            "year_x": year_x,
            "year_y": year_y,
            "date_x": date_x,
            "date_y": date_y,
            "metadata_x": metadata_x,
            "metadata_y": metadata_y,
            "bottom_x": bottom_x,
            "bottom_y": bottom_y,
            "grid_left": grid_left,
            "grid_top": grid_top,
            "grid_start_x": grid_start_x,
            "grid_start_y": grid_start_y,
            "grid_right": grid_left + grid_width,
            "grid_bottom": grid_top + grid_height,
            "safe_x": safe_x,
            "safe_y": safe_y,
            "safe_right": safe_right,
            "safe_bottom": safe_bottom,
        }

    def generate(self, output_path: str = "progress_wallpaper.png") -> str:
        img = Image.new("RGB", (self.width, self.height), self.bg_color)
        self._draw_vignette(img)
        draw = ImageDraw.Draw(img, "RGBA")

        title_font = self._get_font("hero", 260)
        date_font = self._get_font("data", 90)
        info_font = self._get_font("data", 45)
        metadata_font = self._get_font("data", 32)

        year_text = str(self.year)
        date_text = self.today.strftime("%B %d").upper()
        progress_pct = (self.current / self.total) * 100
        bottom_text = f"{self.label.upper()} {self.current} / {self.total}   //   {progress_pct:.1f}%"
        metadata_text = self._build_metadata_text()

        text_metrics = self._measure_text_blocks(
            draw,
            year_text,
            date_text,
            bottom_text,
            metadata_text,
            title_font,
            date_font,
            info_font,
            metadata_font,
        )
        grid_metrics = self._compute_grid_metrics()
        layout_metrics = {**text_metrics, **grid_metrics}
        positions = self._compute_positions(
            self.layout, layout_metrics, self.show_metadata
        )

        # --- DRAW TEXT ---
        draw.text(
            (positions["year_x"], positions["year_y"]),
            year_text,
            fill=self.text_primary,
            font=title_font,
        )
        draw.text(
            (positions["date_x"], positions["date_y"]),
            date_text,
            fill=self.text_accent,
            font=date_font,
        )
        if (
            self.show_metadata
            and positions["metadata_x"] is not None
            and positions["metadata_y"] is not None
        ):
            metadata_color = self._as_rgba(self.text_secondary, fallback_alpha=180)
            draw.text(
                (positions["metadata_x"], positions["metadata_y"]),
                metadata_text,
                fill=metadata_color,
                font=metadata_font,
            )

        # --- DRAW DOTS ---
        bloom_layer = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))

        # Loop through the FULL GRID to ensure a perfect rectangle.
        for i in range(1, grid_metrics["total_slots_in_grid"] + 1):
            row = (i - 1) // self.dots_per_row
            col = (i - 1) % self.dots_per_row

            cx = positions["grid_start_x"] + col * self.gap
            cy = positions["grid_start_y"] + row * self.gap
            bbox = (
                cx - self.dot_size,
                cy - self.dot_size,
                cx + self.dot_size,
                cy + self.dot_size,
            )

            if i <= self.total:
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
                draw.ellipse(bbox, fill=self.void_color)

        img = Image.alpha_composite(img.convert("RGBA"), bloom_layer)

        draw = ImageDraw.Draw(img, "RGBA")
        draw.text(
            (positions["bottom_x"], positions["bottom_y"]),
            bottom_text,
            fill=self.text_secondary,
            font=info_font,
        )

        img = self._add_noise(img)
        final_img = img.resize(
            (self.target_width, self.target_height), resample=Image.Resampling.LANCZOS
        )

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        final_img.save(output_path, quality=100, optimize=True)

        return output_path
