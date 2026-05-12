"""
PDF report generator — renders a Jinja2 HTML template to PDF bytes.

Strategy (tried in order):
  1. Chrome / Chromium headless  — generates proper clickable PDF link annotations;
     works on macOS dev and any environment with Chrome/Chromium installed.
  2. weasyprint Python library   — no link annotations in v68, but full CSS Paged
     Media support (page counters, margins); preferred for Linux production
     (Railway/Render) where Chrome is typically absent.
  3. weasyprint CLI subprocess   — Homebrew-installed CLI on macOS; same limitation
     as the library regarding link annotations; last resort.
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = Path(__file__).parent / "templates"

# Chrome / Chromium candidate paths (macOS first, then Linux)
_CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome-stable",
    "google-chrome",
    "chromium-browser",
    "chromium",
]

# Homebrew (macOS Apple Silicon) weasyprint CLI path
_HOMEBREW_WP = "/opt/homebrew/bin/weasyprint"


# ── HTML rendering ─────────────────────────────────────────────────────────────

def _build_html(result: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=True,
    )
    template = env.get_template("report.html")
    return template.render(r=result)


# ── Strategy 1: Chrome headless ────────────────────────────────────────────────

def _find_chrome():
    for candidate in _CHROME_CANDIDATES:
        p = Path(candidate)
        if p.exists():
            return str(p)
        found = shutil.which(candidate)
        if found:
            return found
    return None


def _via_chrome(html_string: str) -> bytes:
    """
    Use Chrome/Chromium headless to render HTML → PDF.
    Generates proper /URI link annotations — links are clickable in any PDF viewer.
    Requires Chrome or Chromium to be installed.
    """
    chrome = _find_chrome()
    if not chrome:
        raise FileNotFoundError("Chrome/Chromium not found on this system.")

    with tempfile.TemporaryDirectory() as tmp:
        html_path = Path(tmp) / "report.html"
        pdf_path  = Path(tmp) / "report.pdf"

        html_path.write_text(html_string, encoding="utf-8")

        # Copy CSS alongside the HTML so the file:// URL resolves it
        css_dst = Path(tmp) / "report_styles.css"
        css_dst.write_bytes((TEMPLATE_DIR / "report_styles.css").read_bytes())

        result = subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--run-all-compositor-stages-before-draw",
                "--print-to-pdf-no-header",       # suppress Chrome's URL/date header
                f"--print-to-pdf={pdf_path}",
                f"file://{html_path}",
            ],
            capture_output=True,
            timeout=60,
        )

        if not pdf_path.exists():
            raise RuntimeError(
                f"Chrome PDF generation failed (exit {result.returncode}):\n"
                + result.stderr.decode(errors="replace")
            )

        return pdf_path.read_bytes()


# ── Strategy 2: WeasyPrint Python library ──────────────────────────────────────

def _via_python_lib(html_string: str) -> bytes:
    """
    Use the weasyprint Python package.
    Full CSS Paged Media support (page counters, @page margins).
    Works on Linux; raises OSError on macOS (dylib naming mismatch under SIP).
    Note: WeasyPrint 68.x does not generate PDF link annotations.
    """
    from weasyprint import HTML, CSS  # may raise ImportError / OSError on macOS
    css_path = str(TEMPLATE_DIR / "report_styles.css")
    html_obj = HTML(string=html_string, base_url=str(TEMPLATE_DIR))
    css_obj  = CSS(filename=css_path)
    return html_obj.write_pdf(stylesheets=[css_obj])


# ── Strategy 3: WeasyPrint CLI subprocess ─────────────────────────────────────

def _via_cli(html_string: str) -> bytes:
    """
    Use the Homebrew weasyprint CLI as a subprocess.
    Writes HTML to a temp file, invokes the CLI, returns PDF bytes.
    """
    cli = shutil.which("weasyprint") or _HOMEBREW_WP
    if not Path(cli).exists():
        raise FileNotFoundError(
            "weasyprint CLI not found. Install with: brew install weasyprint"
        )

    with tempfile.TemporaryDirectory() as tmp:
        html_path = Path(tmp) / "report.html"
        pdf_path  = Path(tmp) / "report.pdf"

        html_path.write_text(html_string, encoding="utf-8")

        css_dst = Path(tmp) / "report_styles.css"
        css_dst.write_bytes((TEMPLATE_DIR / "report_styles.css").read_bytes())

        result = subprocess.run(
            [cli, str(html_path), str(pdf_path)],
            capture_output=True,
            timeout=60,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"weasyprint CLI failed (exit {result.returncode}):\n"
                + result.stderr.decode(errors="replace")
            )
        return pdf_path.read_bytes()


# ── Public entry point ─────────────────────────────────────────────────────────

def generate_pdf(result: dict) -> bytes:
    """
    Render the AwraResult dict to a PDF and return raw bytes.

    Tries Chrome first (clickable links), then WeasyPrint Python library
    (Linux production), then WeasyPrint CLI (macOS last resort).
    """
    html_string = _build_html(result)

    # Strategy 1 — Chrome headless (clickable links)
    try:
        return _via_chrome(html_string)
    except Exception:
        pass

    # Strategy 2 — WeasyPrint Python library (Linux production)
    try:
        return _via_python_lib(html_string)
    except (ImportError, OSError):
        pass

    # Strategy 3 — WeasyPrint CLI (macOS fallback, no link annotations)
    return _via_cli(html_string)
