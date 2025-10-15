from abc import ABC, abstractmethod
from typing import Any

from books.domain.models import Book


class BookRepository(ABC):
    @abstractmethod
    def list_books(self) -> list[Book]:
        """List all books.

        Returns:
            list[Book]: List of books.
        """

    @abstractmethod
    def get_book(self, book_id: str) -> Book | None:
        """Gets a book by ID.

        Args:
            book_id (str): The book ID.

        Returns:
            Book | None: The book, or None if it does not exist.
        """

    @abstractmethod
    def create_book(self, book: Book) -> Book:
        """Creates a book.

        Args:
            book (Book): The Book info.

        Returns:
            Book: _description_
        """

    @abstractmethod
    def update_book(self, data: dict[str, Any]) -> Book | None:
        """Updates a book.

        Args:
            data (dict): The book data.

        Returns:
            Book | None: The book, or None if it does not exist.
        """

    @abstractmethod
    def delete_book(self, book_id: str) -> bool:
        """Deletes a book by ID.

        Args:
            book_id (str): The book ID.

        Returns:
            bool: True if the book was successfully deleted, False otherwise
        """

    @abstractmethod
    def get_average_price_by_year(self, year: int) -> float | None:
        """Calculates the average price of books published in a given year.

        Args:
            year (int): The publication year to filter books.

        Returns:
            float | None: The average price of books for the specified year,
                          or None if no books are found.
        """
