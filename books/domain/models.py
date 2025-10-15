from datetime import datetime

from pydantic import BaseModel, Field


class Book(BaseModel):
    id: str | None = Field(default=None)
    title: str | None
    author: str | None
    published_date: datetime | None
    genre: str | None
    price: float | None

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d")}
