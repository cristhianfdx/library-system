from datetime import date

from pydantic import BaseModel


class BookOutputDTO(BaseModel):
    id: str
    title: str
    author: str
    published_date: date
    genre: str
    price: float

    class Config:
        from_attributes = True


class CreateBookOutputDTO(BookOutputDTO): ...


class UpdateBookOutputDTO(BookOutputDTO): ...
