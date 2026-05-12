"""
PDF report generator — WeasyPrint renders a Jinja2 HTML template to PDF bytes.
"""
from __future__ import annotations
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = Path(__file__).parent / "templates"


def _build_html(result: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=True,
    )
    template = env.get_template("report.html")
    return template.render(r=result)


def generate_pdf(result: dict) -> bytes:
    """
    Render the AwraResult dict to a PDF and return raw bytes.
    Raises ImportError if WeasyPrint is not installed.
    """
    try:
        from weasyprint import HTML, CSS
    except ImportError as exc:
        raise ImportError(
            "WeasyPrint is required for PDF generation. "
            "Install it with: pip install weasyprint"
        ) from exc

    html_string = _build_html(result)
    css_path = str(TEMPLATE_DIR / "report_styles.css")

    html_obj = HTML(string=html_string, base_url=str(TEMPLATE_DIR))
    css_obj   = CSS(filename=css_path)
    pdf_bytes = html_obj.write_pdf(stylesheets=[css_obj])
    return pdf_bytes
