"""Tests for greeting card PDF renderer."""

import os
import sys
from datetime import datetime

import pytest

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def fixture_path(name):
    return os.path.join(FIXTURE_DIR, name)


class TestGenerateHtml:
    def test_generates_valid_html(self):
        from render_card import generate_html
        html = generate_html(fixture_path("test-image.png"))
        assert "<!DOCTYPE html>" in html
        assert "</html>" in html

    def test_embeds_image_as_base64(self):
        from render_card import generate_html
        html = generate_html(fixture_path("test-image.png"))
        assert "data:image/png;base64," in html

    def test_includes_message_when_provided(self):
        from render_card import generate_html
        html = generate_html(fixture_path("test-image.png"), message="Happy Birthday!")
        assert "Happy Birthday!" in html

    def test_no_message_panel_empty_when_omitted(self):
        from render_card import generate_html
        html = generate_html(fixture_path("test-image.png"))
        assert 'class="message"' in html

    def test_default_back_text(self):
        from render_card import generate_html
        html = generate_html(fixture_path("test-image.png"))
        year = datetime.now().year
        assert f"\u00a9 {year}" in html or f"&copy; {year}" in html

    def test_custom_back_text(self):
        from render_card import generate_html
        html = generate_html(fixture_path("test-image.png"), back_text="Made with love")
        assert "Made with love" in html

    def test_invalid_image_raises(self):
        from render_card import generate_html
        with pytest.raises(FileNotFoundError):
            generate_html("/nonexistent/image.png")

    def test_html_message_overrides_plain(self):
        from render_card import generate_html
        html = generate_html(
            fixture_path("test-image.png"),
            message="plain text",
            html_message='<b>Bold HTML</b>',
        )
        assert "<b>Bold HTML</b>" in html
        assert "plain text" not in html

    def test_left_message(self):
        from render_card import generate_html
        html = generate_html(fixture_path("test-image.png"), left_message="Left side")
        assert "Left side" in html

    def test_html_left_message_overrides_plain(self):
        from render_card import generate_html
        html = generate_html(
            fixture_path("test-image.png"),
            left_message="plain left",
            html_left_message='<i>Styled left</i>',
        )
        assert "<i>Styled left</i>" in html
        assert "plain left" not in html

    def test_newlines_become_br(self):
        from render_card import generate_html
        html = generate_html(fixture_path("test-image.png"), message="Line 1\nLine 2")
        assert "Line 1<br>Line 2" in html

    def test_ampersand_escaped(self):
        from render_card import generate_html
        html = generate_html(fixture_path("test-image.png"), message="Jack & Jill")
        assert "Jack &amp; Jill" in html


class TestCollectImages:
    def test_finds_png_in_directory(self):
        from render_card import collect_images
        images = collect_images(FIXTURE_DIR)
        assert any(img.name == "test-image.png" for img in images)

    def test_returns_empty_for_empty_dir(self, tmp_path):
        from render_card import collect_images
        assert collect_images(str(tmp_path)) == []

    def test_invalid_dir_raises(self):
        from render_card import collect_images
        with pytest.raises(FileNotFoundError):
            collect_images("/nonexistent/dir")


class TestParseArgs:
    def test_single_image_mode(self):
        from render_card import parse_args
        args = parse_args(["--image", "test.png", "--output", "out.pdf"])
        assert args.image == "test.png"
        assert args.output == "out.pdf"

    def test_batch_mode(self):
        from render_card import parse_args
        args = parse_args(["--image-dir", "/some/dir", "--output-dir", "/out"])
        assert args.image_dir == "/some/dir"
        assert args.output_dir == "/out"

    def test_message_arg(self):
        from render_card import parse_args
        args = parse_args(["--image", "t.png", "--output", "o.pdf", "--message", "Hello!"])
        assert args.message == "Hello!"

    def test_back_text_arg(self):
        from render_card import parse_args
        args = parse_args(["--image", "t.png", "--output", "o.pdf", "--back-text", "Custom"])
        assert args.back_text == "Custom"

    def test_html_message_arg(self):
        from render_card import parse_args
        args = parse_args(["--image", "t.png", "--html-message", "<b>Hi</b>"])
        assert args.html_message == "<b>Hi</b>"

    def test_left_message_arg(self):
        from render_card import parse_args
        args = parse_args(["--image", "t.png", "--left-message", "Left"])
        assert args.left_message == "Left"


class TestRenderPdfIntegration:
    """Integration test — requires Playwright + Chromium."""

    @pytest.mark.integration
    def test_renders_pdf_from_fixture(self, tmp_path):
        import asyncio
        from render_card import generate_html, render_pdf

        html = generate_html(
            fixture_path("test-image.png"),
            message="Test message",
            back_text="Test back",
        )
        output = tmp_path / "test-card.pdf"
        asyncio.run(render_pdf(html, str(output)))
        assert output.exists()
        assert output.stat().st_size > 0
        # PDF files start with %PDF
        with open(output, "rb") as f:
            assert f.read(4) == b"%PDF"
