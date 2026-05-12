FROM python:3.11-slim-bullseye

# ── System deps: Chromium for headless PDF generation ─────────────────────────
# Let apt resolve Chromium's own dependencies — avoids brittle manual dep lists
RUN apt-get update && apt-get install -y \
    chromium \
    fonts-liberation \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ── Python deps ───────────────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── App source ────────────────────────────────────────────────────────────────
COPY . .

# Render injects $PORT at runtime; default to 8001 for local docker run
ENV PORT=8001

CMD uvicorn main:app --host 0.0.0.0 --port $PORT
