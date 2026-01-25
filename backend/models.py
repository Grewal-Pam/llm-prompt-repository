# backend/models.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PromptBase(BaseModel):
    title: str = Field(..., example="ClickBaitTitle")
    prompt_text: str = Field(
        ...,
        example="Rewrite the given text as a clickbait-style headline."
    )
    purpose: str = Field(..., example="Text rewriting")
    tags: Optional[List[str]] = Field(
        default=None,
        example=["headline", "rewriting"]
    )
    source: Optional[str] = Field(
        default=None,
        example="https://resources.wolframcloud.com/PromptRepository/"
    )


class PromptCreate(PromptBase):
    """Schema used when creating a new prompt."""
    pass


class PromptRead(PromptBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
