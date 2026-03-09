# greeting-card-pdf

A Claude Code plugin that generates print-ready quarter-fold greeting card PDFs from images.

Print on a single 8.5x11" sheet of letter paper, fold twice, and you have a 4.25x5.5" greeting card with a full-image front, inside message panels, and back branding.

## Layout

```
+---------------+---------------+
| BACK          | FRONT         |   ← top half (printed upside-down)
| (branding)    | (your image)  |
+---------------+---------------+
| INSIDE-LEFT   | INSIDE-RIGHT  |   ← bottom half (right-side up)
| (message)     | (message)     |
+---------------+---------------+
```

**To fold:** Bottom edge up to top edge, then left edge to right edge.

## Install

```bash
claude plugins add greeting-card-pdf
```

On first use, the plugin runs `setup.sh` to create an isolated Python environment with Playwright and Chromium. No system Python changes.

## Usage

Just ask Claude:

> "Make a birthday card from this image"
> "Generate a thank you card with the photo at ~/Desktop/photo.png"
> "Create greeting cards from all images in ~/cards/"

On first run, Claude will ask what name or brand you'd like on the back of your cards. This is saved to `.local.md` and used for all future cards.

## Features

- **Single or batch mode** — one image or a whole directory
- **Inside-left and inside-right** message panels
- **Plain text or styled HTML** messages
- **Customizable back panel** branding (persisted in settings)
- **System fonts only** — Georgia for messages, Courier New for back text
- **No cropping** — images fit within the front panel without being cut off

## Supported Formats

PNG, JPG, JPEG

## Requirements

- Python 3.10+
- macOS or Linux (Playwright + Chromium, installed automatically)

## License

MIT
