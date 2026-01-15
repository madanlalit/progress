"""Core wallpaper generation logic."""

from PIL import Image, ImageDraw, ImageFont
import datetime
from typing import Tuple, Optional
from .config import DEFAULT_CONFIG, MODE_CONFIG, DEFAULT_WIDTH, DEFAULT_HEIGHT


class WallpaperGenerator:
    """Generates year calendar wallpapers showing progress through the year."""

    def __init__(
        self,
        mode: str = "week",
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        bg_color: Optional[Tuple[int, int, int]] = None,
        past_color: Optional[Tuple[int, int, int]] = None,
        current_color: Optional[Tuple[int, int, int]] = None,
        future_color: Optional[Tuple[int, int, int, int]] = None,
        dot_size: Optional[int] = None,
    ):
        """
        Initialize the wallpaper generator.

        Args:
            mode: Display mode ('day', 'week', or 'month')
            width: Image width in pixels
            height: Image height in pixels
            bg_color: Background RGB color
            past_color: Past periods RGB color
            current_color: Current period RGB color
            future_color: Future periods RGBA color
            dot_size: Override dot size for the mode
        """
        self.mode = mode
        self.width = width
        self.height = height

        # Use custom colors or defaults
        self.bg_color = bg_color or DEFAULT_CONFIG["bg"]
        self.past_color = past_color or DEFAULT_CONFIG["past"]
        self.current_color = current_color or DEFAULT_CONFIG["current"]
        self.future_color = future_color or DEFAULT_CONFIG["future"]
        self.text_primary = DEFAULT_CONFIG["text_primary"]
        self.text_secondary = DEFAULT_CONFIG["text_secondary"]
        self.text_accent = DEFAULT_CONFIG["text_accent"]

        # Get mode configuration
        if mode not in MODE_CONFIG:
            raise ValueError(f"Invalid mode: {mode}. Must be 'day', 'week', or 'month'")

        mode_cfg = MODE_CONFIG[mode]
        self.dots_per_row = mode_cfg["dots_per_row"]
        self.dot_size = dot_size or mode_cfg["dot_size"]
        self.gap = mode_cfg["gap"]

        # Calculate date information
        self.today = datetime.date.today()
        self.year = self.today.year
        self.day_of_year = self.today.timetuple().tm_yday
        self.current_week = self.today.isocalendar().week
        self.current_month = self.today.month

        # Mode-specific totals and current position
        if mode == "day":
            self.total = 365
            self.current = self.day_of_year
            self.label = "Day"
        elif mode == "week":
            self.total = 52
            self.current = self.current_week
            self.label = "Week"
        else:  # month
            self.total = 12
            self.current = self.current_month
            self.label = "Month"

    def _load_fonts(self):
        """Load fonts with fallbacks."""
        try:
            title_font = ImageFont.truetype(
                "/System/Library/Fonts/Supplemental/Arial.ttf", 220
            )
            large_font = ImageFont.truetype(
                "/System/Library/Fonts/Supplemental/Arial.ttf", 90
            )
            medium_font = ImageFont.truetype(
                "/System/Library/Fonts/Supplemental/Arial.ttf", 52
            )
            small_font = ImageFont.truetype(
                "/System/Library/Fonts/Supplemental/Arial.ttf", 42
            )
        except OSError:
            try:
                title_font = ImageFont.truetype(
                    "/System/Library/Fonts/SFNSDisplay.ttf", 220
                )
                large_font = ImageFont.truetype(
                    "/System/Library/Fonts/SFNSDisplay.ttf", 90
                )
                medium_font = ImageFont.truetype(
                    "/System/Library/Fonts/SFNSDisplay.ttf", 52
                )
                small_font = ImageFont.truetype(
                    "/System/Library/Fonts/SFNSDisplay.ttf", 42
                )
            except OSError:
                try:
                    title_font = ImageFont.truetype(
                        "/System/Library/Fonts/Helvetica.ttc", 220
                    )
                    large_font = ImageFont.truetype(
                        "/System/Library/Fonts/Helvetica.ttc", 90
                    )
                    medium_font = ImageFont.truetype(
                        "/System/Library/Fonts/Helvetica.ttc", 52
                    )
                    small_font = ImageFont.truetype(
                        "/System/Library/Fonts/Helvetica.ttc", 42
                    )
                except OSError:
                    title_font = ImageFont.load_default()
                    large_font = ImageFont.load_default()
                    medium_font = ImageFont.load_default()
                    small_font = ImageFont.load_default()

        return title_font, large_font, medium_font, small_font

    def generate(self, output_path: str = "progress_wallpaper.png") -> str:
        """
        Generate the wallpaper and save to file.

        Args:
            output_path: Path where the wallpaper will be saved

        Returns:
            The output path
        """
        # Create image
        img = Image.new("RGB", (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(img, "RGBA")

        # Load fonts
        title_font, large_font, medium_font, small_font = self._load_fonts()

        # Calculate grid layout
        rows = (self.total + self.dots_per_row - 1) // self.dots_per_row
        grid_w = self.dots_per_row * self.gap
        grid_h = rows * self.gap

        start_x = (self.width - grid_w) // 2
        start_y = (self.height // 2) + 100

        # Draw text elements
        # Year
        year_text = str(self.year)
        year_bbox = draw.textbbox((0, 0), year_text, font=title_font)
        year_w = year_bbox[2] - year_bbox[0]
        year_x = (self.width - year_w) // 2
        year_y = 350
        draw.text((year_x, year_y), year_text, fill=self.text_primary, font=title_font)

        # Current date
        date_text = self.today.strftime("%B %d")
        date_bbox = draw.textbbox((0, 0), date_text, font=large_font)
        date_w = date_bbox[2] - date_bbox[0]
        date_x = (self.width - date_w) // 2
        date_y = year_y + 280
        draw.text((date_x, date_y), date_text, fill=self.text_accent, font=large_font)

        # Progress info
        progress_text = f"{self.label} {self.current} of {self.total}"
        progress_bbox = draw.textbbox((0, 0), progress_text, font=medium_font)
        progress_w = progress_bbox[2] - progress_bbox[0]
        progress_x = (self.width - progress_w) // 2
        progress_y = start_y - 150
        draw.text(
            (progress_x, progress_y),
            progress_text,
            fill=self.text_secondary,
            font=medium_font,
        )

        # Draw dots
        for i in range(1, self.total + 1):
            row = (i - 1) // self.dots_per_row
            col = (i - 1) % self.dots_per_row

            x = start_x + col * self.gap
            y = start_y + row * self.gap

            # Determine color
            if i < self.current:
                color = self.past_color
            elif i == self.current:
                color = self.current_color
            else:
                color = self.future_color

            draw.ellipse(
                (
                    x - self.dot_size,
                    y - self.dot_size,
                    x + self.dot_size,
                    y + self.dot_size,
                ),
                fill=color,
            )

        # Progress percentage at bottom
        progress_pct = (self.current / self.total) * 100
        percentage_text = f"{progress_pct:.1f}% complete"
        percentage_bbox = draw.textbbox((0, 0), percentage_text, font=small_font)
        percentage_w = percentage_bbox[2] - percentage_bbox[0]
        percentage_x = (self.width - percentage_w) // 2
        percentage_y = start_y + grid_h + 160
        draw.text(
            (percentage_x, percentage_y),
            percentage_text,
            fill=self.text_secondary,
            font=small_font,
        )

        # Save
        img.save(output_path, quality=95, optimize=True)

        return output_path
