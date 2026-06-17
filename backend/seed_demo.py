import json
import urllib.request
from datetime import datetime, timedelta

BASE = "http://127.0.0.1:17890/ingest"
HEADERS = {"Content-Type": "application/json"}

def post(data: dict):
    req = urllib.request.Request(BASE, data=json.dumps(data).encode(), headers=HEADERS, method="POST")
    urllib.request.urlopen(req, timeout=5)

now = datetime.utcnow()
events = [
    {"source": "openai/gpt-4.1-mini", "model": "openai/gpt-4.1-mini", "input_tokens": 54200, "output_tokens": 12800, "requests": 1, "ts": (now - timedelta(minutes=35)).isoformat()},
    {"source": "anthropic/claude-sonnet-4", "model": "anthropic/claude-sonnet-4", "input_tokens": 31200, "output_tokens": 9800, "requests": 1, "ts": (now - timedelta(minutes=18)).isoformat()},
    {"source": "telegram/bot_api", "model": "telegram/bot_api", "input_tokens": 1200, "output_tokens": 3400, "requests": 1, "ts": (now - timedelta(minutes=2)).isoformat()},
    {"source": "fal/flux", "model": "fal/flux", "input_tokens": 0, "output_tokens": 0, "requests": 1, "ts": (now - timedelta(minutes=22)).isoformat()},
    {"source": "llama_cpp/local", "model": "llama_cpp/local", "input_tokens": 67000, "output_tokens": 22100, "requests": 1, "ts": (now - timedelta(minutes=9)).isoformat()},
]

for ev in events:
    try:
        post(ev)
    except Exception as e:
        print("FAIL", ev["source"], e)
        raise SystemExit(1)

print("seeded", len(events))
