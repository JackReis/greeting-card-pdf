---
name: greeting-card-pdf
description: >
  Use when the user asks to "make a greeting card", "generate a card PDF",
  "create a birthday card", "print card from image", "quarter-fold card",
  "card for printing", "thank you card", or needs to convert an image
  into a printable folded greeting card on letter paper.
---

# Greeting Card PDF Generator

Generate print-ready quarter-fold greeting card PDFs from images. The card
prints on a single 8.5x11" sheet, then folds twice into a 4.25x5.5" card
with front image, inside message, and back branding.

## Quarter-Fold Layout

```
+---------------+---------------+
| BACK          | FRONT         |   <- top half (both rotated 180°)
| (branding)    | (image,       |
|               |  fit-to-panel)|
+---------------+---------------+
| INSIDE-LEFT   | INSIDE-RIGHT  |   <- bottom half (right-side up)
| (message)     | (message)     |
+---------------+---------------+
```

Fold bottom edge up to top edge, then fold left edge to right edge.
The front panel faces outward; open the card to see inside-left and inside-right.

## First-Run Setup

If `skills/greeting-card-pdf/.local.md` does not exist, ask the user:

> "What name or brand should appear on the back of your cards?
> (e.g., 'Jane's Studio', 'The Smith Family')"

Then create `.local.md`:
```markdown
# Greeting Card PDF Settings
back_text: © 2026 Jane's Studio
```

Read `back_text` from `.local.md` on every invocation. If the user provides
`--back-text` on the command line, it overrides the setting for that run.

## Usage

Determine the plugin directory (where this SKILL.md lives, two levels up):

```
PLUGIN_DIR="<path to greeting-card-pdf plugin root>"
```

### Single Card

```bash
"$PLUGIN_DIR/.venv/bin/python3" "$PLUGIN_DIR/src/render_card.py" \
  --image /path/to/image.png \
  --message "Happy Birthday!" \
  --output /path/to/card.pdf
```

### Batch Mode

```bash
"$PLUGIN_DIR/.venv/bin/python3" "$PLUGIN_DIR/src/render_card.py" \
  --image-dir /path/to/images/ \
  --message "Same message for all" \
  --output-dir /path/to/pdfs/
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--image` | One of image/image-dir | Single image path |
| `--image-dir` | One of image/image-dir | Directory of images (batch) |
| `--output` | With --image | Output PDF path |
| `--output-dir` | With --image-dir | Output directory for PDFs |
| `--message` | No | Plain-text inside-right panel message |
| `--html-message` | No | Pre-styled HTML for inside-right (overrides --message) |
| `--left-message` | No | Plain-text inside-left panel message |
| `--html-left-message` | No | Pre-styled HTML for inside-left (overrides --left-message) |
| `--back-text` | No | Back panel text (default: from .local.md or © {year}) |

## Implementation Details

- **Runtime:** Plugin's own `.venv/bin/python3` (created by `setup.sh`)
- **No temp files:** HTML generated in memory via Python string substitution
- **Image embedding:** Base64 data URI avoids file path issues in headless Chrome
- **Fonts:** Georgia (messages), Courier New (back branding) — system fonts only
- **Image fitting:** `object-fit: contain` ensures full image visible without cropping

## Supported Image Formats

PNG, JPG, JPEG

## Files

- **`src/card_template.html`** — HTML/CSS template with placeholder tokens
- **`src/render_card.py`** — Python CLI script (stdlib + Playwright only)
- **`tests/test_render.py`** — Unit + integration tests
