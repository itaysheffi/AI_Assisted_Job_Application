from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    # Keep as string to avoid extra runtime dependency (email-validator).
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=8, max_length=1024)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str = Field(min_length=3, max_length=254)
    created_at: datetime

