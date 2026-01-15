# Year Calendar Wallpaper for macOS

An automated macOS wallpaper system that displays a visual year calendar with dots representing weeks, automatically updating daily to show your progress through the year.

![Example](year_calendar_wallpaper.png)

## Features

- ✨ **Modern design** with gradient backgrounds and premium aesthetics
- 🎯 **Multiple display modes**: Day (365 dots), Week (52 dots), or Month (12 dots)
- 🎨 **Minimalist & clean** design that everyone will love
- 📊 **Visual progress tracking** with color-coded past/current/future periods
- 💫 **Glow effects** highlighting current period
- 🔄 **Automatic daily updates** at midnight
- 🖥️ **5K resolution** (5120×2880) optimized for macOS Retina displays
- 🎨 **Fully customizable** colors, modes, and update schedule

## Display Modes

### Week Mode (Default)
52 dots representing each week of the year in a single row.

### Day Mode  
365 dots representing every day of the year in 5 rows - perfect for daily tracking!

### Month Mode
12 large dots representing each month - for a cleaner, simpler view.

**Visual Design:**
- **Past periods**: Subtle gray dots
- **Current period**: Bright coral dot with glow effect
- **Future periods**: Semi-transparent white dots  
- **Display**: Year, current date, progress info, and completion percentage

## Installation

### 1. Install Dependencies

The script requires Pillow (PIL). If you have `uv` installed:

```bash
uv pip install Pillow
```

### 2. Test Manual Generation

Generate the wallpaper manually to verify it works:

```bash
uv run year_calendar.py
```

This creates `year_calendar_wallpaper.png` in the current directory.

### 3. Test Wallpaper Setting

Run the setter script to apply the wallpaper:

```bash
./set_wallpaper.sh
```

Your desktop wallpaper should update immediately!

### 4. Enable Automatic Daily Updates

Copy the LaunchAgent to your user's LaunchAgents directory:

```bash
cp com.yearcalendar.daily.plist ~/Library/LaunchAgents/
```

Load the LaunchAgent:

```bash
launchctl load ~/Library/LaunchAgents/com.yearcalendar.daily.plist
```

The wallpaper will now automatically update every day at 12:01 AM.

## Customization

### Display Modes

Change the `MODE` variable at the top of `year_calendar.py` to switch between visualizations:

```python
MODE = 'week'   # Options: 'day', 'week', or 'month'
```

- **`'day'`** - 365 dots showing every single day of the year (5 rows)
- **`'week'`** - 52 dots showing each week (1 row) - **Default**
- **`'month'`** - 12 dots showing each month (1 row)

### Color & Style Customization

Edit `year_calendar.py` configuration section to customize:

**Colors** (lines 13-20):
- `BG_START` / `BG_END` - Gradient background colors
- `PAST` - Color for completed periods
- `CURRENT` - Highlight color for current period (default: coral)
- `ACCENT` - Accent color for date text (default: purple)
- `TEXT_PRIMARY` / `TEXT_SECONDARY` - Text colors

**Appearance** (automatically adjusted per mode):
- `W, H` - Resolution (line 12)
- Mode-specific: `dot_size`, `gap`, `dots_per_row` (lines 30-57)

**Schedule** (change update time):
- Edit `com.yearcalendar.daily.plist` lines 18-22 to change the daily update time

## Uninstallation

To stop automatic updates:

```bash
launchctl unload ~/Library/LaunchAgents/com.yearcalendar.daily.plist
rm ~/Library/LaunchAgents/com.yearcalendar.daily.plist
```

## Troubleshooting

### Wallpaper not updating automatically

Check the logs:

```bash
cat wallpaper_update.log
cat launchd.log
cat launchd.error.log
```

### Manual trigger for testing

```bash
launchctl start com.yearcalendar.daily
```

### Verify LaunchAgent is loaded

```bash
launchctl list | grep yearcalendar
```

## Files

- `year_calendar.py` - Wallpaper generator script
- `set_wallpaper.sh` - Automation script that generates and sets wallpaper
- `com.yearcalendar.daily.plist` - LaunchAgent configuration for daily updates
- `year_calendar_wallpaper.png` - Generated wallpaper (created automatically)

## Requirements

- macOS
- Python 3.7+
- Pillow library
- `uv` (recommended) or `pip`

---

Made with ❤️ for tracking your year's progress
