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


# ── Strategy 4: fpdf2 (pure Python — Vercel / any environment) ────────────────

def _via_fpdf2(result: dict) -> bytes:
    """
    Pure-Python PDF via fpdf2. No system dependencies — works on Vercel and
    any environment where Chrome and WeasyPrint are unavailable.
    Generates clickable link annotations natively.
    """
    from fpdf import FPDF  # may raise ImportError if fpdf2 not installed

    # ── Colour palette ────────────────────────────────────────────────────────
    PURPLE     = (108, 99, 255)
    DARK       = (26, 26, 46)
    MUTED      = (136, 136, 136)
    GREEN      = (46, 125, 50)
    DARK_GREEN = (27, 94, 32)
    RED        = (198, 40, 40)
    ORANGE     = (230, 81, 0)
    YELLOW_D   = (245, 127, 23)
    LIGHT_BG   = (250, 250, 254)
    BORDER     = (224, 224, 239)
    WHITE      = (255, 255, 255)

    SEV_COLORS = {
        "Critical": RED, "High": ORANGE, "Moderate": YELLOW_D,
        "Low": GREEN, "Note": MUTED,
    }

    # ── Unpack result ─────────────────────────────────────────────────────────
    intake   = result.get("intake", {})
    company  = intake.get("company", "Your Company")
    name     = intake.get("name", "Team")
    stage    = result.get("stage", "pilot")
    version  = result.get("scoring_model_version", "awra-1.0.0")
    cs       = result.get("construct_scores", {})
    ct       = result.get("construct_tiers", {})
    ps       = result.get("pillar_scores", {})
    baseline = result.get("lotusnex_baseline", {})
    div      = result.get("efficiency_dividend", {})
    q        = result.get("quadrant", {})
    findings = result.get("findings", [])
    strength = result.get("top_strength", {})
    contra   = result.get("contradictions", [])
    cta      = result.get("cta", {})
    roadmap  = result.get("roadmap", [])
    ev_chain = result.get("evidence_chain", [])
    ev_mat   = result.get("evidence_matrix", [])

    cta_url = cta.get("url", "https://lotusnex.com/contact.html")

    # ── FPDF subclass with header/footer and auto-sanitisation ────────────────
    class Report(FPDF):
        def normalize_text(self, text):
            """Auto-sanitise unicode to latin-1 so built-in fonts never error."""
            if not isinstance(text, str):
                text = str(text)
            for char, rep in _CHAR_MAP.items():
                text = text.replace(char, rep)
            return text.encode("latin-1", errors="replace").decode("latin-1")

        def header(self):
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*PURPLE)
            self.cell(0, 5, "LotusNex · AWRA", ln=False)
            self.set_font("Helvetica", "", 7)
            self.set_text_color(*MUTED)
            meta = f"{company}  |  {name}  |  Stage: {stage.replace('_', ' ')}  |  Model {version}"
            self.cell(0, 5, meta, ln=True, align="R")
            self.set_draw_color(*PURPLE)
            self.set_line_width(0.4)
            self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
            self.ln(3)
            self.set_text_color(*DARK)

        def footer(self):
            self.set_y(-12)
            self.set_font("Helvetica", "", 7)
            self.set_text_color(*MUTED)
            self.cell(0, 5, f"{self.page_no()} / {{nb}}", align="R")

    pdf = Report(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(18, 20, 18)

    W = 210 - 36  # usable width (A4 - margins)

    # ── Text sanitiser — fpdf2 built-in fonts are latin-1 only ───────────────
    _CHAR_MAP = {
        "—": "--",   # em dash
        "–": "-",    # en dash
        "‘": "'",    # left single quote
        "’": "'",    # right single quote
        "“": '"',    # left double quote
        "”": '"',    # right double quote
        "…": "...",  # ellipsis
        "→": "->",   # right arrow →
        "•": "*",    # bullet •
        "✓": "OK",   # checkmark ✓
        "·": ".",    # middle dot
    }

    def s(text) -> str:
        """Sanitise text to latin-1 safe characters for fpdf2 built-in fonts."""
        if not isinstance(text, str):
            text = str(text)
        for char, rep in _CHAR_MAP.items():
            text = text.replace(char, rep)
        return text.encode("latin-1", errors="replace").decode("latin-1")

    # ── Helpers ───────────────────────────────────────────────────────────────
    def tc(*rgb):
        pdf.set_text_color(*rgb)

    def fc(*rgb):
        pdf.set_fill_color(*rgb)

    def dc(*rgb):
        pdf.set_draw_color(*rgb)

    def page_label(txt):
        pdf.set_font("Helvetica", "B", 7)
        tc(*PURPLE)
        pdf.cell(0, 4, s(txt).upper(), ln=True)
        pdf.ln(1)

    def h1(txt):
        pdf.set_font("Helvetica", "B", 16)
        tc(*DARK)
        pdf.cell(0, 9, s(txt), ln=True)

    def h2(txt):
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 11)
        tc(*DARK)
        pdf.cell(0, 6, s(txt), ln=True)
        dc(*BORDER)
        pdf.set_line_width(0.3)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
        pdf.ln(3)

    def h3(txt):
        pdf.set_font("Helvetica", "B", 9)
        tc(*DARK)
        pdf.cell(0, 5, s(txt), ln=True)

    def body(txt, color=None):
        pdf.set_font("Helvetica", "", 8.5)
        tc(*(color or (85, 85, 85)))
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(W, 4.5, s(txt))

    def fmt_money(n):
        return f"${int(n):,}"

    # ── Reusable dividend columns ─────────────────────────────────────────────
    div_cols = [
        ("Conservative (50%)", fmt_money(div.get("conservative", 0)), "per year", False),
        ("Expected (70%)",     fmt_money(div.get("expected", 0)),
         f"{div.get('hours_per_week_recovered', 0)} hrs/wk recovered", True),
        ("Optimistic (85%)",   fmt_money(div.get("optimistic", 0)), "per year", False),
    ]

    def draw_dividend_cols(y_start):
        cw = W / 3
        for i, (lbl, val, sub, hi) in enumerate(div_cols):
            cx = pdf.l_margin + i * cw
            ch = 20
            fc(*(245, 243, 255) if hi else WHITE)
            dc(*(PURPLE if hi else BORDER))
            pdf.set_line_width(0.3)
            pdf.rect(cx, y_start, cw - 1, ch, style="FD")
            pdf.set_xy(cx + 2, y_start + 2)
            pdf.set_font("Helvetica", "", 7)
            tc(*MUTED)
            pdf.cell(cw - 4, 4, lbl, align="C")
            pdf.set_xy(cx + 2, y_start + 7)
            pdf.set_font("Helvetica", "B", 11)
            tc(*(PURPLE if hi else DARK))
            pdf.cell(cw - 4, 6, val, align="C")
            pdf.set_xy(cx + 2, y_start + 14)
            pdf.set_font("Helvetica", "", 7)
            tc(*MUTED)
            pdf.cell(cw - 4, 4, sub, align="C")
        pdf.set_y(y_start + 22)

    # ═════════════════════════════════════════════════════════════════════
    # PAGE 1 — EXECUTIVE SUMMARY
    # ═════════════════════════════════════════════════════════════════════
    pdf.add_page()
    page_label("AI Workflow Readiness Audit")
    h1("Executive Summary")
    pdf.set_font("Helvetica", "", 8)
    tc(*MUTED)
    pdf.cell(0, 5, company, ln=True)
    pdf.ln(4)

    # Composite score — centred
    pdf.set_font("Helvetica", "B", 38)
    tc(*PURPLE)
    pdf.cell(0, 14, str(result.get("composite_score", 0)), ln=True, align="C")
    pdf.set_font("Helvetica", "", 9)
    tc(85, 85, 85)
    pdf.cell(0, 5, "WORKFLOW READINESS SCORE", ln=True, align="C")
    pdf.set_font("Helvetica", "B", 9)
    tc(*PURPLE)
    pdf.cell(0, 5, result.get("composite_tier", ""), ln=True, align="C")
    pdf.set_font("Helvetica", "", 8)
    tc(*GREEN)
    pdf.cell(0, 5, f"Stage: {stage.replace('_', ' ')}  ·  Model {version}", ln=True, align="C")
    pdf.ln(5)

    # Four construct cards — 2×2
    card_w = (W - 4) / 2
    card_h = 24
    constructs = [
        ("AUTOMATION LEVERAGE",  cs.get("automation_leverage", 0),  ct.get("automation_leverage", "")),
        ("PRODUCTION RISK",      cs.get("production_risk", 0),      ct.get("production_risk", "")),
        ("ECONOMIC CONFIDENCE",  cs.get("economic_confidence", 0),  ct.get("economic_confidence", "")),
        ("EVIDENCE CONFIDENCE",  cs.get("evidence_confidence", 0),  ct.get("evidence_confidence", "")),
    ]
    row_top = pdf.get_y()
    for i, (lbl, score, tier) in enumerate(constructs):
        col, row = i % 2, i // 2
        cx = pdf.l_margin + col * (card_w + 4)
        cy = row_top + row * (card_h + 3)
        fc(*LIGHT_BG); dc(*BORDER); pdf.set_line_width(0.3)
        pdf.rect(cx, cy, card_w, card_h, style="FD")
        pdf.set_xy(cx + 3, cy + 3)
        pdf.set_font("Helvetica", "B", 6.5); tc(*PURPLE)
        pdf.cell(card_w - 6, 4, lbl)
        pdf.set_xy(cx + 3, cy + 7)
        pdf.set_font("Helvetica", "B", 18); tc(*DARK)
        pdf.cell(card_w - 6, 9, str(score))
        pdf.set_xy(cx + 3, cy + 17)
        pdf.set_font("Helvetica", "", 7.5); tc(*MUTED)
        pdf.cell(card_w - 6, 4, tier)
    pdf.set_y(row_top + 2 * (card_h + 3) + 3)

    # Quadrant card
    qy = pdf.get_y(); qh = 16
    fc(245, 243, 255); dc(*PURPLE); pdf.set_line_width(0.8)
    pdf.rect(pdf.l_margin, qy, 2, qh, style="F")
    pdf.set_line_width(0.3)
    pdf.rect(pdf.l_margin + 2, qy, W - 2, qh, style="FD")
    pdf.set_xy(pdf.l_margin + 5, qy + 2)
    pdf.set_font("Helvetica", "B", 9); tc(74, 67, 181)
    pdf.cell(W - 10, 5, q.get("label", ""), ln=True)
    pdf.set_xy(pdf.l_margin + 5, qy + 8)
    pdf.set_font("Helvetica", "", 8); tc(68, 68, 68)
    pdf.multi_cell(W - 10, 4, q.get("body", ""))
    pdf.set_y(qy + qh + 4)

    # Dividend range
    h3("Efficiency Dividend Estimate")
    pdf.ln(1)
    draw_dividend_cols(pdf.get_y())
    pdf.set_font("Helvetica", "I", 7); tc(*MUTED)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(W, 3.5, div.get("caveat", ""))

    # ═════════════════════════════════════════════════════════════════════
    # PAGE 2 — EVIDENCE MATRIX
    # ═════════════════════════════════════════════════════════════════════
    pdf.add_page()
    page_label("Page 2")
    h2("Evidence Matrix")
    body("What was reported, what it means, and what to verify.", color=MUTED)
    pdf.ln(2)

    col_widths = [32, 26, 38, 20, 46]
    headers    = ["Input Answers", "Derived Variable", "Consequence", "Severity", "Validation Step"]
    fc(240, 238, 255); dc(208, 200, 255); pdf.set_line_width(0.3)
    pdf.set_font("Helvetica", "B", 7); tc(74, 67, 181)
    for h, cw in zip(headers, col_widths):
        pdf.cell(cw, 6, h, border=1, fill=True)
    pdf.ln()

    fill = False
    for row in ev_mat:
        if pdf.get_y() > pdf.h - 28:
            pdf.add_page(); page_label("Evidence Matrix (cont.)")
        vals = [
            row.get("input_answers", ""),
            row.get("derived_variable", ""),
            row.get("consequence", ""),
            f"{row.get('severity_label', '')} {row.get('severity_score', '')}",
            row.get("validation_step", ""),
        ]
        row_h = max(5, max(len(v) // max(1, cw // 2) for v, cw in zip(vals, col_widths)) * 3.5)
        ry = pdf.get_y()
        rx = pdf.l_margin
        fc(*(LIGHT_BG if fill else WHITE)); pdf.set_font("Helvetica", "", 7); tc(68, 68, 68)
        for v, cw in zip(vals, col_widths):
            pdf.set_xy(rx, ry)
            pdf.multi_cell(cw, row_h, v, border=1, fill=fill)
            rx += cw
        pdf.set_y(ry + row_h)
        fill = not fill

    # ═════════════════════════════════════════════════════════════════════
    # PAGE 3 — PILLAR BREAKDOWN
    # ═════════════════════════════════════════════════════════════════════
    pdf.add_page()
    page_label("Page 3")
    h2("Pillar Breakdown vs LotusNex Production Baseline")

    pillar_labels = {
        "process": "Process Fit", "security": "Security",
        "tokenomics": "Tokenomics", "reliability": "Reliability",
    }
    bar_w, bar_h = 100, 5
    lbl_w = 35
    for pillar, label in pillar_labels.items():
        score = ps.get(pillar, 0)
        base  = baseline.get(pillar, 70)
        gap   = round(score - base, 1)
        y = pdf.get_y()
        pdf.set_font("Helvetica", "B", 8); tc(68, 68, 68)
        pdf.set_xy(pdf.l_margin, y + 1.5)
        pdf.cell(lbl_w, bar_h, label)
        bx = pdf.l_margin + lbl_w
        fc(238, 238, 238); pdf.rect(bx, y + 2, bar_w, bar_h, style="F")
        fc(*PURPLE); pdf.rect(bx, y + 2, bar_w * score / 100, bar_h, style="F")
        dc(255, 107, 107); pdf.set_line_width(0.8)
        bline = bx + bar_w * base / 100
        pdf.line(bline, y + 1, bline, y + 8)
        pdf.set_font("Helvetica", "B", 8); tc(*DARK)
        pdf.set_xy(bx + bar_w + 2, y + 1.5); pdf.cell(15, bar_h, str(score))
        tc(*(GREEN if gap >= 0 else RED))
        pdf.set_font("Helvetica", "", 7.5)
        pdf.cell(20, bar_h, ("+" if gap >= 0 else "") + str(gap), ln=True)
        pdf.ln(3)
    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 7); tc(*MUTED)
    pdf.cell(0, 4, "Red line = LotusNex Production Baseline. Gap shows your score vs baseline.", ln=True)

    # ═════════════════════════════════════════════════════════════════════
    # PAGE 4 — TOP FINDINGS
    # ═════════════════════════════════════════════════════════════════════
    pdf.add_page()
    page_label("Page 4")
    h2("Top Findings")
    body("Prioritised by severity score. All scores on a 0–100 scale.", color=MUTED)
    pdf.ln(2)

    for f in findings:
        if pdf.get_y() > pdf.h - 50:
            pdf.add_page(); page_label("Top Findings (cont.)")
        sev_col = SEV_COLORS.get(f.get("severity_label", "Note"), MUTED)
        pdf.set_font("Helvetica", "B", 7.5); tc(*sev_col)
        pdf.set_x(pdf.l_margin)
        pdf.cell(W, 5, f"{f.get('severity_label', '')} · {f.get('severity_score', '')}", ln=True)
        pdf.set_font("Helvetica", "B", 9.5); tc(*DARK)
        pdf.set_x(pdf.l_margin)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(W, 5, f.get("title", ""))
        pdf.set_font("Helvetica", "", 8); tc(85, 85, 85)
        pdf.set_x(pdf.l_margin)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(W, 4.5, f.get("evidence", ""))
        pdf.set_font("Helvetica", "B", 7.5); tc(68, 68, 68)
        pdf.set_x(pdf.l_margin)
        pdf.cell(W, 4, f"Impact: {f.get('consequence', '')}", ln=True)
        pdf.set_x(pdf.l_margin)
        pdf.cell(W, 4, "Validate:", ln=True)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.set_x(pdf.l_margin)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(W, 4, f.get("validation_step", ""))
        dc(*BORDER); pdf.set_line_width(0.2)
        pdf.line(pdf.l_margin, pdf.get_y() + 1, pdf.w - pdf.r_margin, pdf.get_y() + 1)
        pdf.ln(5)

    # ═════════════════════════════════════════════════════════════════════
    # PAGE 5 — TOP STRENGTH + REFLECTION PROMPTS
    # ═════════════════════════════════════════════════════════════════════
    pdf.add_page()
    page_label("Page 5")
    h2("Top Strength")

    sy = pdf.get_y()
    fc(232, 250, 240); dc(165, 214, 183); pdf.set_line_width(0.3)
    pdf.rect(pdf.l_margin, sy, W, 22, style="FD")
    pdf.set_xy(pdf.l_margin + 4, sy + 2)
    pdf.set_font("Helvetica", "B", 7); tc(*GREEN)
    pdf.cell(0, 4, "HIGHEST SCORING PILLAR", ln=True)
    pdf.set_xy(pdf.l_margin + 4, sy + 7)
    pdf.set_font("Helvetica", "B", 11); tc(*DARK_GREEN)
    pdf.cell(0, 6, f"{strength.get('label', '')} — {strength.get('score', '')}", ln=True)
    pdf.set_xy(pdf.l_margin + 4, sy + 14)
    pdf.set_font("Helvetica", "", 8); tc(68, 68, 68)
    pdf.multi_cell(W - 8, 4, strength.get("description", ""))
    pdf.set_y(sy + 24)

    h2("Reflection Prompts")
    if contra:
        body(f"{len(contra)} pattern(s) detected that warrant a second look.", color=MUTED)
    else:
        body("No contradictions detected. Your answers are internally consistent.", color=MUTED)
    pdf.ln(2)

    for c in contra:
        rpy = pdf.get_y()
        fc(255, 251, 234); dc(255, 179, 0); pdf.set_line_width(0.8)
        pdf.rect(pdf.l_margin, rpy, 2, 18, style="F")
        pdf.set_line_width(0.3)
        pdf.rect(pdf.l_margin + 2, rpy, W - 2, 18, style="FD")
        pdf.set_xy(pdf.l_margin + 5, rpy + 2)
        pdf.set_font("Helvetica", "B", 8.5); tc(93, 64, 55)
        pdf.cell(W - 10, 5, c.get("title", ""), ln=True)
        pdf.set_xy(pdf.l_margin + 5, rpy + 8)
        pdf.set_font("Helvetica", "", 8); tc(68, 68, 68)
        pdf.multi_cell(W - 10, 4, c.get("body", ""))
        pdf.set_y(rpy + 20); pdf.ln(2)

    if not contra:
        pdf.set_font("Helvetica", "", 8); tc(*MUTED)
        pdf.cell(0, 5, "No contradictions detected in this diagnostic session.", ln=True)

    # ═════════════════════════════════════════════════════════════════════
    # PAGE 6 — EFFICIENCY DIVIDEND DETAIL
    # ═════════════════════════════════════════════════════════════════════
    pdf.add_page()
    page_label("Page 6")
    h2("Efficiency Dividend — Detail")
    draw_dividend_cols(pdf.get_y())
    h3("Assumptions")
    pdf.set_font("Helvetica", "", 8); tc(85, 85, 85)
    for a in div.get("assumptions", []):
        pdf.set_x(pdf.l_margin)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(W, 5, "* " + a)
    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 7.5); tc(*MUTED)
    pdf.set_x(pdf.l_margin)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(W, 4, div.get("caveat", ""))

    # ═════════════════════════════════════════════════════════════════════
    # PAGE 7 — RECOMMENDED ROADMAP
    # ═════════════════════════════════════════════════════════════════════
    pdf.add_page()
    page_label("Page 7")
    h2("Recommended Roadmap")
    body("Stage-specific sequence for moving from current readiness to production confidence.", color=MUTED)
    pdf.ln(3)

    for i, phase in enumerate(roadmap):
        if pdf.get_y() > pdf.h - 40:
            pdf.add_page(); page_label("Roadmap (cont.)")
        py = pdf.get_y()
        fc(*PURPLE); dc(*PURPLE); pdf.set_line_width(0)
        pdf.rect(pdf.l_margin, py, 11, 8, style="F")
        pdf.set_xy(pdf.l_margin, py + 1)
        pdf.set_font("Helvetica", "B", 8); tc(*WHITE)
        pdf.cell(11, 6, str(i + 1), align="C")
        pdf.set_xy(pdf.l_margin + 14, py)
        pdf.set_font("Helvetica", "B", 9); tc(*DARK)
        pdf.cell(0, 5, phase.get("title", ""), ln=True)
        pdf.set_x(pdf.l_margin + 14)
        pdf.set_font("Helvetica", "", 8); tc(85, 85, 85)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(W, 4.5, phase.get("description", ""))
        for action in phase.get("actions", []):
            pdf.set_x(pdf.l_margin + 14)
            pdf.set_font("Helvetica", "", 7.5); tc(85, 85, 85)
            pdf.multi_cell(W - 14, 4.5, "-> " + action)
        pdf.ln(4)

    # ═════════════════════════════════════════════════════════════════════
    # PAGE 8 — DISCOVERY CALL CTA
    # ═════════════════════════════════════════════════════════════════════
    pdf.add_page()
    page_label("Page 8")

    cy = pdf.get_y(); cta_h = 62
    fc(*PURPLE); pdf.rect(pdf.l_margin, cy, W, cta_h, style="F")

    pdf.set_xy(pdf.l_margin + 8, cy + 8)
    pdf.set_font("Helvetica", "B", 13); tc(*WHITE)
    pdf.multi_cell(W - 16, 7, cta.get("heading", ""), align="C")

    pdf.set_x(pdf.l_margin + 8)
    pdf.set_font("Helvetica", "", 9); tc(210, 210, 255)
    pdf.multi_cell(W - 16, 5, cta.get("body", ""), align="C")

    btn_y = pdf.get_y() + 5
    btn_w = 90; btn_h = 11
    btn_x = pdf.l_margin + (W - btn_w) / 2
    fc(*WHITE); pdf.set_line_width(0)
    pdf.rect(btn_x, btn_y, btn_w, btn_h, style="F")
    pdf.set_xy(btn_x, btn_y + 2)
    pdf.set_font("Helvetica", "B", 9); tc(*PURPLE)
    pdf.cell(btn_w, btn_h - 4, cta.get("button_label", "Book the Review →"),
             align="C", link=cta_url)

    pdf.set_xy(pdf.l_margin, btn_y + btn_h + 4)
    pdf.set_font("Helvetica", "", 7); tc(190, 190, 240)
    pdf.cell(W, 5, cta_url, align="C", link=cta_url)

    pdf.set_y(cy + cta_h + 8)
    pdf.set_font("Helvetica", "", 7); tc(*MUTED)
    pdf.cell(0, 4, f"AWRA Scoring Model {version} · LotusNex · lotusnex.com", ln=True, align="C")
    pdf.cell(0, 4, "All scores are directional. No industry benchmarks or calibrated probabilities are implied.", ln=True, align="C")

    # ═════════════════════════════════════════════════════════════════════
    # APPENDIX — PER-QUESTION EVIDENCE CHAIN
    # ═════════════════════════════════════════════════════════════════════
    pdf.add_page()
    page_label("Appendix")
    h2("Per-Question Evidence Chain")
    body("Every question answered, what was selected, and how it is interpreted.", color=MUTED)
    pdf.ln(2)

    for item in ev_chain:
        if pdf.get_y() > pdf.h - 32:
            pdf.add_page(); page_label("Evidence Chain (cont.)")
        pdf.set_font("Helvetica", "B", 7); tc(*PURPLE)
        fc(240, 238, 255); pdf.set_line_width(0)
        pdf.cell(14, 5, item.get("question_id", "").upper(), fill=True)
        pdf.set_font("Helvetica", "I", 8); tc(68, 68, 68)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(W, 5, "  " + item.get("question_wording", ""))
        ans = f"→ {item.get('answer_label', '')}"
        if item.get("is_not_sure"): ans += " [Not Sure]"
        if item.get("is_not_yet_implemented"): ans += " [Not Yet Implemented]"
        pdf.set_font("Helvetica", "B", 8); tc(*DARK); pdf.set_x(pdf.l_margin)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(W, 4.5, ans)
        if item.get("evidence"):
            pdf.set_font("Helvetica", "", 7.5); tc(85, 85, 85); pdf.set_x(pdf.l_margin)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(W, 4, item.get("evidence", ""))
        pdf.ln(3)

    return bytes(pdf.output())


# ── Public entry point ─────────────────────────────────────────────────────────

def generate_pdf(result: dict) -> bytes:
    """
    Render the AwraResult dict to a PDF and return raw bytes.

    Strategy order:
      1. Chrome headless  — clickable links; local macOS dev
      2. WeasyPrint lib   — Linux production (Railway/Render)
      3. fpdf2            — pure Python; Vercel and any environment
      4. WeasyPrint CLI   — Homebrew macOS last resort
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

    # Strategy 3 — fpdf2 (pure Python — Vercel / no system deps)
    try:
        return _via_fpdf2(result)
    except ImportError:
        pass

    # Strategy 4 — WeasyPrint CLI (macOS last resort, no link annotations)
    return _via_cli(html_string)
