# Progress - Year Calendar Wallpaper Generator

Beautiful year calendar wallpapers for macOS showing your progress through the year.

## Features

- ✨ **Modern design** with clean aesthetics
- 🎯 **Multiple display modes**: Day (365 dots), Week (52 dots), or Month (12 dots)
- 🎨 **Fully customizable** colors and appearance
- 📊 **Visual progress tracking** with color-coded past/current/future periods
- 🔄 **Automatic daily updates** via LaunchAgent
- 🖥️ **5K resolution** (5120×2880) optimized for macOS Retina displays

## Installation

### From source

```bash
git clone https://github.com/madanlalit/progress.git
cd progress
pip install -e .
```

## Usage

### Generate Wallpaper

```bash
# Week mode (default)
progress generate

# Day mode with 365 dots
progress generate --mode day

# Month mode
progress generate --mode month

# Custom output location
progress generate --output ~/Desktop/calendar.png

# Custom colors
progress generate --bg-color "#1a1a1c" --current-color "#ff7350"
```

### Enable Daily Auto-Updates

```bash
# Install LaunchAgent for daily updates at midnight
progress install

# Uninstall
progress uninstall
```

### Command-Line Options

```
usage: progress [-h] [--version] {generate,install,uninstall} ...

Commands:
  generate    Generate wallpaper
  install     Install daily auto-update
  uninstall   Uninstall daily auto-update

Generate options:
  --mode {day,week,month}   Display mode (default: week)
  --output PATH             Output file path
  --bg-color HEX           Background color (e.g., "#1a1a1c")
  --past-color HEX         Past periods color
  --current-color HEX      Current period color
  --dot-size INT           Override dot size
  --no-set                 Generate only, don't set as wallpaper
```

## Display Modes

### Week Mode (Default)
52 dots representing each week of the year in a single row.

### Day Mode  
365 dots representing every day of the year in 5 rows - perfect for daily tracking!

### Month Mode
12 large dots representing each month - for a cleaner, simpler view.

## Customization

All display modes feature:
- **Past periods**: Subtle gray dots
- **Current period**: Bright coral dot
- **Future periods**: Semi-transparent white dots  
- **Display**: Year, current date, progress info, and completion percentage

## Requirements

- macOS
- Python >=3.8
- Pillow >=9.0.0

## Development

```bash
# Clone repository
git clone https://github.com/madanlalit/progress.git
cd progress

# Install in development mode
pip install -e .

# Run locally
python -m progress.cli generate
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Created by [Lalit Madan](https://github.com/madanlalit)

---

Made with ❤️ for tracking your year's progress
