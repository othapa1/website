"""
PDF report generator — WeasyPrint renders a Jinja2 HTML template to PDF bytes.

Strategy (in order):
  1. weasyprint Python library  — fastest, works on Linux (Railway/Render production)
  2. weasyprint CLI subprocess  — fallback for macOS where the pip library can't load
     native GLib/Pango; Homebrew installs its own isolated Python env that has the
     correct dylib paths pre-baked.
"""
from __future__ import annotations
import shutil
import subprocess
import tempfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = Path(__file__).parent / "templates"

# Homebrew (macOS Apple Silicon) weasyprint CLI path
_HOMEBREW_WP = "/opt/homebrew/bin/weasyprint"


def _build_html(result: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=True,
    )
    template = env.get_template("report.html")
    return template.render(r=result)


def _via_python_lib(html_string: str) -> bytes:
    """Use the weasyprint Python package (preferred; works on Linux)."""
    from weasyprint import HTML, CSS  # may raise OSError on macOS
    css_path = str(TEMPLATE_DIR / "report_styles.css")
    html_obj = HTML(string=html_string, base_url=str(TEMPLATE_DIR))
    css_obj  = CSS(filename=css_path)
    return html_obj.write_pdf(stylesheets=[css_obj])


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

        # Write HTML alongside a symlink to the template dir so relative
        # CSS / asset paths resolve correctly
        html_path.write_text(html_string, encoding="utf-8")

        # Copy CSS into the same temp dir so weasyprint CLI can find it
        css_src = TEMPLATE_DIR / "report_styles.css"
        css_dst = Path(tmp) / "report_styles.css"
        css_dst.write_bytes(css_src.read_bytes())

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


def generate_pdf(result: dict) -> bytes:
    """
    Render the AwraResult dict to a PDF and return raw bytes.

    Tries the Python library first; falls back to the CLI on macOS where the
    pip-installed library cannot load the native GLib/Pango dylibs.
    """
    html_string = _build_html(result)

    try:
        return _via_python_lib(html_string)
    except (ImportError, OSError):
        pass  # fall through to CLI

    return _via_cli(html_string)
