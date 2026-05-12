"""
AWRA Phase 1 — FastAPI scoring service.

POST /score   → AwraResult JSON
POST /report  → PDF bytes

Run locally:
  uvicorn main:app --reload --port 8001
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

from scoring.engine import calculate_awra_result
from scoring.config import SCORING_MODEL_VERSION

app = FastAPI(
    title="AWRA Scoring API",
    version=SCORING_MODEL_VERSION,
    description="AI Workflow Readiness Auditor — Phase 1 scoring and report generation.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tightened per deployment env
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)


# ── Pydantic models ───────────────────────────────────────────────────────────

class Answer(BaseModel):
    id: str
    answer_id: Optional[str] = None
    selected_option_ids: Optional[List[str]] = None
    score: Optional[float] = None
    is_not_sure: Optional[bool] = False
    is_not_yet_implemented: Optional[bool] = False

    class Config:
        extra = "allow"


class CalculatorInputs(BaseModel):
    people: Optional[float] = 0
    hours_per_week: Optional[float] = Field(default=0, alias="hoursPerWeek")
    automation_pct: Optional[float] = Field(default=0, alias="automationPct")
    hourly_cost: Optional[float] = Field(default=0, alias="hourlyCost")

    class Config:
        populate_by_name = True
        extra = "allow"


class DiagnosticSession(BaseModel):
    stage: str = "pilot"
    intake: Optional[Dict[str, Any]] = {}
    answers: List[Answer] = []
    calculator_inputs: Optional[CalculatorInputs] = Field(
        default=None, alias="calculatorInputs"
    )

    class Config:
        populate_by_name = True
        extra = "allow"


class AwraResult(BaseModel):
    """Loose model — scoring engine returns a plain dict; we pass it through."""
    class Config:
        extra = "allow"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _session_to_dict(session: DiagnosticSession) -> dict:
    """Convert Pydantic model to the plain dict the engine expects."""
    calc = {}
    if session.calculator_inputs:
        ci = session.calculator_inputs
        calc = {
            "people":         ci.people or 0,
            "hours_per_week": ci.hours_per_week or 0,
            "automation_pct": ci.automation_pct or 0,
            "hourly_cost":    ci.hourly_cost or 0,
        }

    answers_raw = []
    for a in session.answers:
        d = {"id": a.id}
        if a.answer_id is not None:
            d["answer_id"] = a.answer_id
        if a.selected_option_ids is not None:
            d["selected_option_ids"] = a.selected_option_ids
        if a.score is not None:
            d["score"] = a.score
        if a.is_not_sure:
            d["is_not_sure"] = True
        if a.is_not_yet_implemented:
            d["is_not_yet_implemented"] = True
        answers_raw.append(d)

    return {
        "stage":             session.stage,
        "intake":            session.intake or {},
        "answers":           answers_raw,
        "calculator_inputs": calc,
    }


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "scoring_model_version": SCORING_MODEL_VERSION}


@app.post("/score")
def score(session: DiagnosticSession):
    """
    Accept a full diagnostic session and return a scored AwraResult.
    """
    try:
        session_dict = _session_to_dict(session)
        result = calculate_awra_result(session_dict)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/report")
def report(result: Dict[str, Any]):
    """
    Accept an AwraResult JSON and return a PDF byte stream.
    Requires WeasyPrint to be installed.
    """
    try:
        from report.pdf_generator import generate_pdf
        pdf_bytes = generate_pdf(result)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": 'attachment; filename="awra-report.pdf"'
            },
        )
    except ImportError:
        raise HTTPException(
            status_code=503,
            detail="PDF generation not available — WeasyPrint not installed."
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
