import os
from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
from .seed_wolfram import seed_wolfram_prompts
from fastapi.middleware.cors import CORSMiddleware


from .db import init_db
from .models import PromptCreate, PromptRead
from .repository import (
    create_prompt,
    get_prompts,
    get_prompt_by_id,
)

app = FastAPI(
    title="LLM Prompt Repository",
    description="Anonymous repository for sharing and browsing LLM prompts for scientific use.",
    version="1.0.0",
)


@app.on_event("startup")
def startup_event():
    init_db()
    seed_wolfram_prompts()

ENV = os.getenv("ENV", "local")



if ENV == "production":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.post("/api/prompts", response_model=PromptRead, status_code=201)
def create_prompt_api(prompt: PromptCreate):
    return create_prompt(prompt)


@app.get("/api/prompts", response_model=List[PromptRead])
def list_prompts_api(
    q: Optional[str] = Query(default=None),
    purpose: Optional[str] = Query(default=None),
):
    return get_prompts(q=q, purpose=purpose)


@app.get("/api/prompts/{prompt_id}", response_model=PromptRead)
def get_prompt_api(prompt_id: int):
    prompt = get_prompt_by_id(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt
