from typing import Any

from books.application.dto import input_dto, output_dto
from books.domain.models import Book


def map_books_to_output_dto(*, books: list[Book]) -> list[output_dto.BookOutputDTO]:
    return [output_dto.BookOutputDTO.model_validate(b.model_dump()) for b in books]


def map_book_to_output_dto(*, book: Book) -> output_dto.BookOutputDTO:
    return output_dto.BookOutputDTO(**book.model_dump())


def map_create_book_input_dto_to_book(
    *, create_book_input_dto: input_dto.CreateBookInputDTO
) -> Book:
    return Book(**create_book_input_dto.model_dump())


def map_create_book_to_output_dto(*, book: Book) -> output_dto.CreateBookOutputDTO:
    return output_dto.CreateBookOutputDTO.model_validate(book.model_dump())


def map_update_book_input_dto_to_data_book(
    *, update_book_input_dto: input_dto.UpdateBookInputDTO
) -> dict[str, Any]:
    return update_book_input_dto.model_dump()


def map_update_book_to_output_dto(*, book: Book) -> output_dto.UpdateBookOutputDTO:
    return output_dto.UpdateBookOutputDTO.model_validate(book.model_dump())
