import os
import sys
import tempfile
import shutil

# Ensure repo root is on sys.path so `import backend` resolves
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

from backend import db
from backend import repository
from backend.models import PromptCreate


def setup_temp_db():
    tmpdir = tempfile.mkdtemp()
    db.DATA_DIR = tmpdir
    db.DB_PATH = os.path.join(tmpdir, "prompts.db")
    db.init_db()
    return tmpdir


def test_create_and_ordering():
    tmpdir = setup_temp_db()
    try:
        p1 = PromptCreate(
            title="First",
            prompt_text="first text",
            purpose="demo",
            tags=["a"],
            source="src1",
        )
        p2 = PromptCreate(
            title="Second",
            prompt_text="second text",
            purpose="demo",
            tags=None,
            source=None,
        )

        created1 = repository.create_prompt(p1)
        created2 = repository.create_prompt(p2)

        prompts = repository.get_prompts()
        assert len(prompts) == 2
        # newest first by created_at then id
        assert prompts[0].id == created2.id
        assert prompts[1].id == created1.id

        fetched = repository.get_prompt_by_id(created1.id)
        assert fetched is not None
        assert fetched.title == "First"
    finally:
        shutil.rmtree(tmpdir)
