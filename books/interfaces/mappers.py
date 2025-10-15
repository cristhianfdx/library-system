from typing import Any

from books.application.dto import input_dto


def map_create_book_request_to_input_dto(
    *,
    request_data: dict[str, Any],
) -> input_dto.CreateBookInputDTO:
    return input_dto.CreateBookInputDTO(**request_data)


def map_update_book_request_to_input_dto(
    *, request_data: dict[str, Any], book_id: str
) -> input_dto.UpdateBookInputDTO:
    return input_dto.UpdateBookInputDTO(id=book_id, **request_data)
