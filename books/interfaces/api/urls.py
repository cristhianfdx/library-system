from django.urls import path

from books.interfaces.api.views import BookDetailAPIView, BookListCreateAPIView

urlpatterns = [
    path("", BookListCreateAPIView.as_view(), name="book_list_create"),
    path("<str:book_id>/", BookDetailAPIView.as_view(), name="book-detail"),
]
