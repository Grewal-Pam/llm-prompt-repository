from typing import List, Optional
from datetime import datetime
import sqlite3

from .db import get_connection
from .models import PromptCreate, PromptRead


def create_prompt(prompt: PromptCreate) -> PromptRead:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO prompts (title, prompt_text, purpose, tags, source)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            prompt.title,
            prompt.prompt_text,
            prompt.purpose,
            ",".join(prompt.tags) if prompt.tags else None,
            prompt.source,
        ),
    )

    conn.commit()
    prompt_id = cursor.lastrowid

    row = cursor.execute(
        "SELECT * FROM prompts WHERE id = ?", (prompt_id,)
    ).fetchone()

    conn.close()

    return PromptRead(
        id=row["id"],
        title=row["title"],
        prompt_text=row["prompt_text"],
        purpose=row["purpose"],
        tags=row["tags"].split(",") if row["tags"] else None,
        source=row["source"],
        created_at=row["created_at"],
    )


def get_prompts(q: Optional[str] = None, purpose: Optional[str] = None) -> List[PromptRead]:
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM prompts WHERE 1=1"
    params = []

    if q:
        query += " AND title LIKE ?"
        params.append(f"%{q}%")

    if purpose:
        query += " AND purpose = ?"
        params.append(purpose)

    rows = cursor.execute(query, params).fetchall()
    conn.close()

    return [
        PromptRead(
            id=row["id"],
            title=row["title"],
            prompt_text=row["prompt_text"],
            purpose=row["purpose"],
            tags=row["tags"].split(",") if row["tags"] else None,
            source=row["source"],
            created_at=row["created_at"],
        )
        for row in rows
    ]


def get_prompt_by_id(prompt_id: int) -> Optional[PromptRead]:
    conn = get_connection()
    cursor = conn.cursor()

    row = cursor.execute(
        "SELECT * FROM prompts WHERE id = ?", (prompt_id,)
    ).fetchone()

    conn.close()

    if not row:
        return None

    return PromptRead(
        id=row["id"],
        title=row["title"],
        prompt_text=row["prompt_text"],
        purpose=row["purpose"],
        tags=row["tags"].split(",") if row["tags"] else None,
        source=row["source"],
        created_at=row["created_at"],
    )
