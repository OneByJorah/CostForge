from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
import json, sqlite3, os
from datetime import datetime, timedelta

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "costforge.db"
LOG_PATH = os.getenv("COSTFORGE_LOG", str(APP_DIR / "usage.jsonl"))

app = FastAPI(title="CostForge")

PRICE_MAP = {
  "anthropic/claude-sonnet-4": {"provider": "anthropic", "input": 3.0, "output": 15.0, "unit": "per 1M tokens"},
  "openai/gpt-4.1-mini": {"provider": "openai", "input": 0.40, "output": 1.60, "unit": "per 1M tokens"},
  "openrouter/pricing": {"provider": "openrouter", "input": 0.0, "output": 0.0, "unit": "varies"},
  "telegram/bot_api": {"provider": "telegram", "input": 0.0, "output": 0.0, "unit": "free up to threshold"},
  "fal/flux": {"provider": "fal", "input": 0.0, "output": 0.0, "unit": "free tier"},
  "edge/tts": {"provider": "microsoft", "input": 0.0, "output": 0.0, "unit": "free tier"},
  "whisper/stt": {"provider": "openai", "input": 0.0, "output": 0.0, "unit": "free tier / local"},
  "llama_cpp/local": {"provider": "local", "input": 0.0, "output": 0.0, "unit": "compute only"},
  "github/api": {"provider": "github", "input": 0.0, "output": 0.0, "unit": "free tier"},
  "searxng/search": {"provider": "selfhost", "input": 0.0, "output": 0.0, "unit": "compute only"},
  "browser/cdp": {"provider": "selfhost", "input": 0.0, "output": 0.0, "unit": "compute only"},
}

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""create table if not exists usage(
            id integer primary key autoincrement,
            ts text,
            source text,
            model text,
            input_tokens integer default 0,
            output_tokens integer default 0,
            requests integer default 1,
            meta text
        )""")
        c.execute("""create table if not exists events(
            id integer primary key autoincrement,
            ts text,
            kind text,
            detail text
        )""")

init_db()

@app.get("/healthz")
def healthz():
    return {"ok": True, "ts": datetime.utcnow().isoformat()}

@app.post("/ingest")
def ingest(payload: dict):
    source = payload.get("source", "unknown")
    model = payload.get("model", "")
    input_tokens = int(payload.get("input_tokens", 0))
    output_tokens = int(payload.get("output_tokens", 0))
    requests = int(payload.get("requests", 1))
    meta = json.dumps(payload.get("meta", {}))
    ts = payload.get("ts", datetime.utcnow().isoformat())
    with sqlite3.connect(DB_PATH) as c:
        c.execute("insert into usage(ts,source,model,input_tokens,output_tokens,requests,meta) values(?,?,?,?,?,?,?)",
                  (ts, source, model, input_tokens, output_tokens, requests, meta))
    return {"ok": True}

@app.get("/api/usage")
def usage(days: int = 30):
    since = datetime.utcnow() - timedelta(days=days)
    with sqlite3.connect(DB_PATH) as c:
        rows = c.execute("select ts,source,model,input_tokens,output_tokens,requests from usage where ts >= ? order by ts asc",
                         (since.isoformat(),)).fetchall()
    out = []
    for r in rows:
        out.append({"ts": r[0], "source": r[1], "model": r[2], "input_tokens": r[3], "output_tokens": r[4], "requests": r[5]})
    return JSONResponse(out)

@app.get("/api/summary")
def summary(days: int = 7):
    since = datetime.utcnow() - timedelta(days=days)
    with sqlite3.connect(DB_PATH) as c:
        rows = c.execute("""select source,model,
            sum(requests) as reqs,
            sum(input_tokens) as in_toks,
            sum(output_tokens) as out_toks
            from usage where ts >= ? group by source,model""", (since.isoformat(),)).fetchall()
    total_req = 0
    chart = []
    for r in rows:
        source, model, reqs, inp, outp = r
        total_req += reqs
        price = PRICE_MAP.get(model, PRICE_MAP.get(source, {"input": 0.0, "output": 0.0}))
        effective_cost = 0.0 if ("local" in source or "selfhost" in source or "free" in source) else (inp * price.get("input", 0) + outp * price.get("output", 0)) / 1_000_000.0
        premium = (inp * price.get("input", 0) + outp * price.get("output", 0)) / 1_000_000.0
        chart.append({"key": f"{source}::{model or 'free'}", "source": source, "model": model or "free", "requests": reqs,
                      "input_tokens": inp or 0, "output_tokens": outp or 0,
                      "effective_cost": effective_cost, "premium_equivalent": premium})
    return {"days": days, "total_requests": total_req, "items": chart, "pricing_refs": PRICE_MAP}

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return (APP_DIR.parent / "frontend" / "dist" / "index.html").read_text()
