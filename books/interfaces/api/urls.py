from django.urls import path

from books.interfaces.api.views import (
    AveragePriceAPIView,
    BookDetailAPIView,
    BookListCreateAPIView,
)

urlpatterns = [
    path("", BookListCreateAPIView.as_view(), name="book_list_create"),
    path("average-price/", AveragePriceAPIView.as_view(), name="average-price"),
    path("<str:book_id>/", BookDetailAPIView.as_view(), name="book-detail"),
]
