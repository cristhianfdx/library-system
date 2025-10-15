import logging

from pydantic import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from books.domain import exceptions
from books.interfaces.api import serializers

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        return response

    logger.error(str(exc))

    if isinstance(exc, ValidationError):
        serializer = serializers.ErrorResponse(data={"detail": str(exc)})
        serializer.is_valid(raise_exception=False)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, exceptions.BookNotFoundError | exceptions.BooksArentNotFound):
        serializer = serializers.ErrorResponse(data={"detail": str(exc)})
        serializer.is_valid(raise_exception=False)
        return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, exceptions.BookAlreadyExistsError):
        serializer = serializers.ErrorResponse(data={"detail": str(exc)})
        serializer.is_valid(raise_exception=False)
        return Response(serializer.data, status=status.HTTP_409_CONFLICT)

    serializer = serializers.ErrorResponse(data={"detail": "Internal server error"})
    serializer.is_valid(raise_exception=False)
    return Response(serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
