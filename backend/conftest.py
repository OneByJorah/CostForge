"""Pytest configuration for the CostForge backend.

Isolates the SQLite database per test session before `main` is imported, so the
real `backend/costforge.db` is never touched by a test run.
"""
import os
import sys
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

BACKEND_DIR = Path(__file__).resolve().parent


def pytest_configure():
    """Runs before collection: make `import main` work and redirect the DB."""
    if str(BACKEND_DIR) not in sys.path:
        sys.path.insert(0, str(BACKEND_DIR))
    # main.py resolves its database at import time, so the env var must be set
    # before the first `import main`. Use a temp directory pytest owns.
    db_dir = tempfile.mkdtemp(prefix="costforge-tests-")
    os.environ["COSTFORGE_DB"] = os.path.join(db_dir, "test_costforge.db")


@pytest.fixture()
def client():
    """A TestClient bound to the app, re-created per test."""
    from main import app

    with TestClient(app) as c:
        yield c
