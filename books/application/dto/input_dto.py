from datetime import datetime

from pydantic import BaseModel


class _BookInputDTO(BaseModel):
    title: str
    author: str
    published_date: datetime
    genre: str
    price: float


class CreateBookInputDTO(_BookInputDTO): ...


class UpdateBookInputDTO(BaseModel):
    id: str
    title: str | None = None
    author: str | None = None
    published_date: datetime | None = None
    genre: str | None = None
    price: float | None = None
