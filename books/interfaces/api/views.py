from typing import Any

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from books.application.services import BookService
from books.infraestructure.repositories.book_repository_mongo import MongoBookRepository
from books.interfaces import mappers
from books.interfaces.api import serializers


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "page_size": self.get_page_size(self.request),
                "current_page": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )


class _BookAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = BookService(MongoBookRepository())


class BookListCreateAPIView(_BookAPIView):
    @extend_schema(
        operation_id="books_list",
        responses=serializers.PaginatedBookResponse,
        description="Listar todos los libros con paginación",
        parameters=[
            OpenApiParameter(
                name="page", description="Número de página", required=False, type=int
            ),
        ],
    )
    def get(self, request: Request) -> Response:
        paginator = self.pagination_class()
        books = self.service.list_books()
        results = paginator.paginate_queryset(books, request)
        serialized = [b.model_dump() for b in results]
        return paginator.get_paginated_response(serialized)

    @extend_schema(
        description="Crear un libro.",
        request=serializers.CreateBookRequest,
        responses={
            201: OpenApiResponse(
                response=serializers.CreateBookResponse,
                description="Libro creado exitosamente",
                examples=[
                    OpenApiExample(
                        "Respuesta exitosa",
                        value={
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "title": "Cien años de soledad",
                            "author": "Gabriel García Márquez",
                            "published_date": "1967-05-30",
                            "genre": "Realismo mágico",
                            "price": 19.99,
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                response=serializers.ErrorResponse,
                description="Error de validación",
                examples=[
                    OpenApiExample(
                        "Error de validación",
                        value={"detail": "El campo 'title' es obligatorio."},
                    )
                ],
            ),
            401: OpenApiResponse(
                response=serializers.ErrorResponse,
                description="No autorizado",
                examples=[
                    OpenApiExample(
                        "No autorizado",
                        value={"detail": "Token inválido o expirado."},
                    )
                ],
            ),
            409: OpenApiResponse(
                response=serializers.ErrorResponse,
                description="Conflicto: libro ya existe",
                examples=[
                    OpenApiExample(
                        "Conflicto",
                        value={"detail": "El libro con ese título ya existe."},
                    )
                ],
            ),
            500: OpenApiResponse(
                response=serializers.ErrorResponse,
                description="Internal server error",
                examples=[
                    OpenApiExample(
                        "Internal server error",
                        value={"detail": "Internal server error."},
                    )
                ],
            ),
        },
    )
    def post(self, request: Request) -> Response:
        serializer = serializers.CreateBookRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        book_dto = mappers.map_create_book_request_to_input_dto(
            request_data=serializer.validated_data
        )
        book = self.service.create_book(book_dto)
        response_serializer = serializers.CreateBookResponse(book.model_dump())
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class BookDetailAPIView(_BookAPIView):
    @extend_schema(
        operation_id="book_by_id",
        description="Obtener un libro por ID",
        responses={
            200: OpenApiResponse(
                response=serializers.BookResponse,
                description="Libro encontrado",
                examples=[
                    OpenApiExample(
                        "Ejemplo",
                        value={
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "title": "Cien años de soledad",
                            "author": "Gabriel García Márquez",
                            "published_date": "1967-05-30",
                            "genre": "Realismo mágico",
                            "price": 19.99,
                        },
                    )
                ],
            ),
            404: OpenApiResponse(
                response=serializers.ErrorResponse,
                description="Libro no encontrado",
                examples=[
                    OpenApiExample(
                        "No encontrado", value={"detail": "Libro no encontrado"}
                    )
                ],
            ),
            401: OpenApiResponse(
                response=serializers.ErrorResponse,
                description="No autorizado",
                examples=[
                    OpenApiExample(
                        "No autorizado", value={"detail": "Token inválido o expirado"}
                    )
                ],
            ),
        },
    )
    def get(self, _: Request, book_id: str) -> Response:
        book = self.service.get_book(book_id=book_id)
        response_serializer = serializers.BookResponse(book.model_dump())
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Actualizar un libro por ID",
        request=serializers.UpdateBookRequest,
        responses={
            200: serializers.UpdateBookResponse,
            400: OpenApiResponse(
                response=serializers.ErrorResponse, description="Error de validación"
            ),
            401: OpenApiResponse(
                response=serializers.ErrorResponse, description="No autorizado"
            ),
            404: OpenApiResponse(
                response=serializers.ErrorResponse, description="Libro no encontrado"
            ),
            409: OpenApiResponse(
                response=serializers.ErrorResponse,
                description="Conflicto: libro ya existe",
            ),
        },
    )
    def patch(self, request: Request, book_id: str) -> Response:
        serializer = serializers.UpdateBookRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_dto = mappers.map_update_book_request_to_input_dto(
            request_data=serializer.validated_data, book_id=book_id
        )
        book = self.service.update_book(book_dto)
        response_serializer = serializers.UpdateBookResponse(book.model_dump())
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Eliminar un libro por ID",
        responses={
            204: OpenApiResponse(
                response=None, description="Libro eliminado exitosamente"
            ),
            404: OpenApiResponse(
                response=serializers.ErrorResponse,
                description="Libro no encontrado",
                examples=[
                    OpenApiExample(
                        "No encontrado", value={"detail": "Libro no encontrado"}
                    )
                ],
            ),
            401: OpenApiResponse(
                response=serializers.ErrorResponse,
                description="No autorizado",
                examples=[
                    OpenApiExample(
                        "No autorizado", value={"detail": "Token inválido o expirado"}
                    )
                ],
            ),
        },
    )
    def delete(self, _: Request, book_id: str) -> Response:
        self.service.delete_book(book_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
