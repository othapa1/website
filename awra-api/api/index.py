"""
Vercel entry point — imports the FastAPI ASGI app from main.py.
Vercel's Python runtime detects the `app` export and runs it as ASGI.
All requests to this project are rewritten here via vercel.json.
"""
import sys
import os

# Add the awra-api root (one level up from api/) to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app  # noqa: F401  — Vercel looks for `app`
