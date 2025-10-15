class BookException(Exception):
    def __init__(self, message: str = "Error en el dominio de libros", *args, **kwargs):
        super().__init__(message, *args)
        self.message = message

    def __str__(self) -> str:
        return self.message


class BookNotFoundError(BookException):
    def __init__(self, book_id: str):
        super().__init__(f"El libro con id '{book_id}' no existe.")


class BookAlreadyExistsError(BookException):
    def __init__(self, title: str):
        super().__init__(f"Ya existe un libro con el título '{title}'.")


class BooksArentNotFound(BookException):
    def __init__(self, details: str = "No hay libros creados."):
        super().__init__(details)
