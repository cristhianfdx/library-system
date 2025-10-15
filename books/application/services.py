from books.application.dto import input_dto, mappers, output_dto
from books.domain import exceptions
from books.domain.ports import BookRepository


class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def list_books(self) -> list[output_dto.BookOutputDTO]:
        return mappers.map_books_to_output_dto(books=self.repository.list_books())

    def get_book(self, book_id: str) -> output_dto.BookOutputDTO:
        book = self.repository.get_book(book_id=book_id)

        if book is None:
            raise exceptions.BookNotFoundError(book_id=book_id)
        return mappers.map_book_to_output_dto(book=book)

    def create_book(
        self, create_book_input_dto: input_dto.CreateBookInputDTO
    ) -> output_dto.CreateBookOutputDTO:
        book = mappers.map_create_book_input_dto_to_book(
            create_book_input_dto=create_book_input_dto
        )

        try:
            saved_book = self.repository.create_book(book)
            return mappers.map_create_book_to_output_dto(book=saved_book)
        except ValueError:
            raise exceptions.BookAlreadyExistsError(title=create_book_input_dto.title)

    def update_book(
        self, update_book_input_dto: input_dto.UpdateBookInputDTO
    ) -> output_dto.UpdateBookOutputDTO | None:
        data_book = mappers.map_update_book_input_dto_to_data_book(
            update_book_input_dto=update_book_input_dto
        )
        try:
            updated_book = self.repository.update_book(data=data_book)
        except ValueError:
            raise exceptions.BookAlreadyExistsError(title=update_book_input_dto.title)

        if updated_book is None:
            raise exceptions.BookNotFoundError(book_id=update_book_input_dto.id)
        return mappers.map_update_book_to_output_dto(book=updated_book)

    def delete_book(self, book_id: str) -> None:
        book_exists = self.repository.delete_book(book_id)
        if not book_exists:
            raise exceptions.BookNotFoundError(book_id=book_id)
