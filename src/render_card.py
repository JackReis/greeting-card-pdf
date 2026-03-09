"""Quarter-fold greeting card PDF renderer.

Generates print-ready PDFs from images using Playwright headless Chromium.
Layout: 8.5x11" letter, quarter-fold (4.25x5.5" panels).
"""

import argparse
import asyncio
import base64
import html as html_module
from datetime import datetime
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent / "card_template.html"
DEFAULT_BACK_TEXT = f"\u00a9 {datetime.now().year}"


def generate_html(
    image_path: str,
    message: str = "",
    back_text: str = DEFAULT_BACK_TEXT,
    html_message: str = "",
    left_message: str = "",
    html_left_message: str = "",
) -> str:
    """Generate HTML for a quarter-fold greeting card.

    Args:
        image_path: Path to the front panel image (PNG or JPG).
        message: Optional plain-text message for inside-right panel.
        back_text: Text for the back panel. Defaults to © {year}.
        html_message: Optional pre-styled HTML for inside-right panel.
            When provided, takes precedence over message (no escaping applied).
        left_message: Optional plain-text message for inside-left panel.
        html_left_message: Optional pre-styled HTML for inside-left panel.
            When provided, takes precedence over left_message (no escaping applied).

    Returns:
        Complete HTML string ready for Playwright rendering.

    Raises:
        FileNotFoundError: If image_path does not exist.
    """
    img_path = Path(image_path)
    if not img_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Determine MIME type
    suffix = img_path.suffix.lower()
    mime = "image/png" if suffix == ".png" else "image/jpeg"

    # Encode image as base64 data URI
    img_bytes = img_path.read_bytes()
    b64 = base64.b64encode(img_bytes).decode("ascii")
    data_uri = f"data:{mime};base64,{b64}"

    # Read template
    template = TEMPLATE_PATH.read_text()

    # Substitute placeholders (using replace to avoid CSS brace conflicts)
    result = template.replace("{image_data_uri}", data_uri)

    # Inside-right panel
    if html_message:
        result = result.replace("{message}", html_message)
    else:
        escaped_message = html_module.escape(message).replace("\n", "<br>")
        result = result.replace("{message}", escaped_message)

    # Inside-left panel
    if html_left_message:
        result = result.replace("{left_message}", html_left_message)
    else:
        escaped_left = html_module.escape(left_message).replace("\n", "<br>")
        result = result.replace("{left_message}", escaped_left)

    result = result.replace("{back_text}", html_module.escape(back_text))
    return result


def collect_images(directory: str) -> list[Path]:
    """Find all PNG/JPG images in a directory.

    Args:
        directory: Path to directory to scan.

    Returns:
        Sorted list of image Paths.

    Raises:
        FileNotFoundError: If directory does not exist.
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise FileNotFoundError(f"Directory not found: {directory}")
    extensions = {".png", ".jpg", ".jpeg"}
    return sorted(p for p in dir_path.iterdir() if p.suffix.lower() in extensions)


async def render_pdf(html_content: str, output_path: str) -> None:
    """Render HTML to PDF using Playwright headless Chromium.

    Args:
        html_content: Complete HTML string.
        output_path: Path for the output PDF file.
    """
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(html_content, wait_until="networkidle")
        await page.pdf(
            path=output_path,
            width="8.5in",
            height="11in",
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            print_background=True,
        )
        await browser.close()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate quarter-fold greeting card PDFs from images."
    )
    # Image source (mutually exclusive)
    img_group = parser.add_mutually_exclusive_group(required=True)
    img_group.add_argument("--image", help="Path to a single image file")
    img_group.add_argument("--image-dir", help="Directory of images (batch mode)")

    # Output (mutually exclusive)
    out_group = parser.add_mutually_exclusive_group()
    out_group.add_argument("--output", help="Output PDF path (single mode)")
    out_group.add_argument("--output-dir", help="Output directory (batch mode)")

    parser.add_argument("--message", default="", help="Plain-text message for inside-right panel")
    parser.add_argument(
        "--html-message", default="",
        help="Pre-styled HTML for inside-right panel (overrides --message, no escaping)",
    )
    parser.add_argument("--left-message", default="", help="Plain-text message for inside-left panel")
    parser.add_argument(
        "--html-left-message", default="",
        help="Pre-styled HTML for inside-left panel (overrides --left-message, no escaping)",
    )
    parser.add_argument(
        "--back-text",
        default=DEFAULT_BACK_TEXT,
        help=f"Text for back panel (default: {DEFAULT_BACK_TEXT})",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """CLI entry point."""
    args = parse_args(argv)

    if args.image:
        # Single mode
        html = generate_html(
            args.image, message=args.message, back_text=args.back_text,
            html_message=args.html_message, left_message=args.left_message,
            html_left_message=args.html_left_message,
        )
        output = args.output or Path(args.image).with_suffix(".pdf")
        asyncio.run(render_pdf(html, str(output)))
        print(f"Created: {output}")
    else:
        # Batch mode
        images = collect_images(args.image_dir)
        if not images:
            print(f"No images found in {args.image_dir}")
            return
        out_dir = Path(args.output_dir) if args.output_dir else Path(args.image_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        for img in images:
            html = generate_html(
                str(img), message=args.message, back_text=args.back_text,
                html_message=args.html_message, left_message=args.left_message,
                html_left_message=args.html_left_message,
            )
            output = out_dir / f"{img.stem}.pdf"
            asyncio.run(render_pdf(html, str(output)))
            print(f"Created: {output}")


if __name__ == "__main__":
    main()
