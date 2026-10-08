import json
import os



def test_healthz(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True


def test_api_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert "providers" in data
    assert isinstance(data["providers"], int)


def test_api_stats(client):
    resp = client.get("/api/stats")
    assert resp.status_code == 200
    data = resp.json()
    totals = data["totals"]
    assert "total_requests" in totals
    assert "total_tokens" in totals


def test_api_summary(client):
    resp = client.get("/api/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert "days" in data
    assert "total_requests" in data
    assert "items" in data
    assert "pricing_refs" in data


def test_ingest_and_stats_increment(client):
    payload = {
        "source": "test_source",
        "model": "gpt-4",
        "input_tokens": 100,
        "output_tokens": 50,
        "requests": 1,
        "meta": {"premium_model": "gpt-4", "premium_cost_usd": 0.01},
    }
    resp = client.post("/ingest", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True

    resp = client.get("/api/recent")
    assert resp.status_code == 200
    recent = resp.json()
    assert len(recent) >= 1
    last = recent[0]
    assert last["source"] == "test_source"
    assert last["input_tokens"] == 100
    assert last["output_tokens"] == 50

    resp = client.get("/api/stats")
    assert resp.status_code == 200
    data = resp.json()
    totals = data["totals"]
    assert totals["total_requests"] >= 1
    assert totals["total_tokens"] >= 150


def test__estimate_tokens():
    from main import _estimate_tokens

    assert _estimate_tokens(None) == 0
    assert _estimate_tokens("") == 0
    assert _estimate_tokens("hello") == 1
    assert _estimate_tokens("a" * 100) == 25


def test__parse_openai_usage():
    from main import _parse_openai_usage

    text = '{"usage": {"prompt_tokens": 50, "completion_tokens": 100}, "model": "gpt-4"}'
    body_text = '{"usage": {"prompt_tokens": 50, "completion_tokens": 100}, "model": "gpt-4"}'
    result = _parse_openai_usage(text, body_text)
    assert result == (50, 100, "gpt-4", False)


def test__parse_generic_usage():
    from main import _parse_generic_usage

    text = '{"usage": {"input_tokens": 50, "output_tokens": 100}, "model": "gpt-4"}'
    body_text = '{"usage": {"input_tokens": 50, "output_tokens": 100}, "model": "gpt-4"}'
    result = _parse_generic_usage(text, body_text)
    assert result == (50, 100, "gpt-4", False)