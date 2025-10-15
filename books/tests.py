import unittest
from datetime import date
from unittest.mock import MagicMock, patch

from books.application.dto import input_dto
from books.application.services import BookService
from books.domain import exceptions


class TestBookService(unittest.TestCase):
    def setUp(self):
        self.repository = MagicMock()
        self.service = BookService(repository=self.repository)

    @patch("books.application.services.mappers.map_books_to_output_dto")
    def test_list_books(self, mock_mapper):
        books = ["book1", "book2"]
        self.repository.list_books.return_value = books
        mock_mapper.return_value = ["mapped1", "mapped2"]

        result = self.service.list_books()

        self.repository.list_books.assert_called_once()
        mock_mapper.assert_called_once_with(books=books)
        self.assertEqual(result, ["mapped1", "mapped2"])

    @patch("books.application.services.mappers.map_book_to_output_dto")
    def test_get_book_success(self, mock_mapper):
        book = MagicMock()
        self.repository.get_book.return_value = book
        mock_mapper.return_value = "book_dto"

        result = self.service.get_book("123")

        self.repository.get_book.assert_called_once_with(book_id="123")
        mock_mapper.assert_called_once_with(book=book)
        self.assertEqual(result, "book_dto")

    def test_get_book_not_found(self):
        self.repository.get_book.return_value = None

        with self.assertRaises(exceptions.BookNotFoundError):
            self.service.get_book("123")

    @patch("books.application.services.mappers.map_create_book_input_dto_to_book")
    @patch("books.application.services.mappers.map_create_book_to_output_dto")
    def test_create_book_success(self, mock_output_mapper, mock_input_mapper):
        dto = input_dto.CreateBookInputDTO(
            title="Book A",
            author="John",
            price=10,
            published_date=date(2024, 1, 1),
            genre="Fiction",
        )
        mapped_book = MagicMock()
        saved_book = MagicMock()
        self.repository.create_book.return_value = saved_book
        mock_input_mapper.return_value = mapped_book
        mock_output_mapper.return_value = "created_dto"

        result = self.service.create_book(dto)

        mock_input_mapper.assert_called_once_with(create_book_input_dto=dto)
        self.repository.create_book.assert_called_once_with(mapped_book)
        mock_output_mapper.assert_called_once_with(book=saved_book)
        self.assertEqual(result, "created_dto")

    @patch("books.application.services.mappers.map_create_book_input_dto_to_book")
    def test_create_book_already_exists(self, mock_input_mapper):
        dto = input_dto.CreateBookInputDTO(
            title="Book A",
            author="John",
            price=10,
            published_date=date(2024, 1, 1),
            genre="Fiction",
        )
        mapped_book = MagicMock()
        self.repository.create_book.side_effect = ValueError
        mock_input_mapper.return_value = mapped_book

        with self.assertRaises(exceptions.BookAlreadyExistsError):
            self.service.create_book(dto)

    @patch("books.application.services.mappers.map_update_book_input_dto_to_data_book")
    @patch("books.application.services.mappers.map_update_book_to_output_dto")
    def test_update_book_success(self, mock_output_mapper, mock_input_mapper):
        dto = input_dto.UpdateBookInputDTO(id="1", title="Book X")
        mapped_data = {"id": "1", "title": "Book X"}
        updated_book = MagicMock()
        self.repository.update_book.return_value = updated_book
        mock_input_mapper.return_value = mapped_data
        mock_output_mapper.return_value = "updated_dto"

        result = self.service.update_book(dto)

        mock_input_mapper.assert_called_once_with(update_book_input_dto=dto)
        self.repository.update_book.assert_called_once_with(data=mapped_data)
        mock_output_mapper.assert_called_once_with(book=updated_book)
        self.assertEqual(result, "updated_dto")

    @patch("books.application.services.mappers.map_update_book_input_dto_to_data_book")
    def test_update_book_not_found(self, mock_input_mapper):
        dto = input_dto.UpdateBookInputDTO(id="1", title="Book X")
        self.repository.update_book.return_value = None
        mock_input_mapper.return_value = {"id": "1", "title": "Book X"}

        with self.assertRaises(exceptions.BookNotFoundError):
            self.service.update_book(dto)

    @patch("books.application.services.mappers.map_update_book_input_dto_to_data_book")
    def test_update_book_already_exists(self, mock_input_mapper):
        dto = input_dto.UpdateBookInputDTO(id="1", title="Book X")
        self.repository.update_book.side_effect = ValueError
        mock_input_mapper.return_value = {"id": "1", "title": "Book X"}

        with self.assertRaises(exceptions.BookAlreadyExistsError):
            self.service.update_book(dto)

    def test_delete_book_success(self):
        self.repository.delete_book.return_value = True
        self.service.delete_book("1")
        self.repository.delete_book.assert_called_once_with("1")

    def test_delete_book_not_found(self):
        self.repository.delete_book.return_value = False

        with self.assertRaises(exceptions.BookNotFoundError):
            self.service.delete_book("1")

    def test_get_average_price_by_year_success(self):
        self.repository.get_average_price_by_year.return_value = 42.5
        result = self.service.get_average_price_by_year(2020)
        self.assertEqual(result, 42.5)
        self.repository.get_average_price_by_year.assert_called_once_with(2020)

    def test_get_average_price_by_year_not_found(self):
        self.repository.get_average_price_by_year.return_value = None

        with self.assertRaises(exceptions.BooksArentNotFound):
            self.service.get_average_price_by_year(2020)


if __name__ == "__main__":
    unittest.main()
