from pydantic import BaseModel, Field, HttpUrl


class JobCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    company: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=20_000)
    url: HttpUrl | None = None


class JobOut(BaseModel):
    id: int
    title: str
    company: str
    description: str
    url: HttpUrl | None = None

