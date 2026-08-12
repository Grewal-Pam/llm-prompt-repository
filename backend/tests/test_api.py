import os
import sys
import tempfile
import shutil

# Ensure repo root is on sys.path so `import backend` resolves
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

from fastapi.testclient import TestClient

import backend.db as db_module


def test_api_endpoints_seed_and_create():
    tmpdir = tempfile.mkdtemp()
    try:
        db_module.DATA_DIR = tmpdir
        db_module.DB_PATH = os.path.join(tmpdir, "prompts.db")

        # import app after setting DB path so startup uses temp DB
        from backend.main import app

        with TestClient(app) as client:
            r = client.get("/api/prompts")
            assert r.status_code == 200
            data = r.json()
            assert isinstance(data, list)

            # create a prompt
            payload = {
                "title": "API Test",
                "prompt_text": "text",
                "purpose": "testing",
                "tags": ["t"],
                "source": "unit",
            }
            cr = client.post("/api/prompts", json=payload)
            assert cr.status_code == 201

            m = client.get("/mcp/capabilities")
            assert m.status_code == 200
            mj = m.json()
            assert "protocol" in mj and "prompt_count" in mj
    finally:
        shutil.rmtree(tmpdir)
