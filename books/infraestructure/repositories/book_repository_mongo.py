from typing import Any

from bson import ObjectId
from pymongo.collection import Collection

from books.domain.models import Book
from books.domain.ports import BookRepository
from books.infraestructure import mongodb


class MongoBookRepository(BookRepository):
    def __init__(self):
        self.collection = mongodb.get_mongo_collection("books")
        self.collection.create_index("title", unique=True)

    def list_books(self) -> list[Book]:
        docs = self.collection.find()
        return [self._map_book(doc=doc) for doc in docs]

    def get_book(self, book_id: str) -> Book | None:
        doc = self.collection.find_one({"_id": ObjectId(book_id)})
        if not doc:
            return None
        return self._map_book(doc=doc)

    def create_book(self, book: Book) -> Book:
        self._validate_if_book_already_exists(book.title)

        result = self.collection.insert_one(book.model_dump(exclude={"id"}))
        book.id = str(result.inserted_id)
        return book

    def update_book(self, data: dict[str, Any]) -> Book | None:
        book_id = data["id"]
        update_data = {k: v for k, v in data.items() if v is not None and k != "id"}

        if "title" in update_data:
            self._validate_if_book_already_exists(update_data["title"])

        res = self.collection.update_one(
            {"_id": ObjectId(book_id)},
            {"$set": update_data},
        )

        if res.matched_count == 0:
            return None

        doc = self.collection.find_one({"_id": ObjectId(book_id)})
        return self._map_book(doc=doc)

    def delete_book(self, book_id: str) -> bool:
        res = self.collection.delete_one({"_id": ObjectId(book_id)})
        return res.deleted_count > 0

    def get_average_price_by_year(self, year: int) -> float | None:
        start = f"{year:04d}-01-01"
        end = f"{year + 1:04d}-01-01"

        pipeline = [
            {"$match": {"published_date": {"$gte": start, "$lt": end}}},
            {"$group": {"_id": None, "average_price": {"$avg": "$price"}}},
        ]

        result = list(self.collection.aggregate(pipeline))
        if result and "average_price" in result[0]:
            return result[0]["average_price"]
        return None

    def _map_book(self, doc: Collection) -> Book:
        return Book(id=str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"})

    def _validate_if_book_already_exists(self, title: str) -> None:
        if self.collection.find_one({"title": title}):
            raise ValueError(f"El libro con título '{title}' ya existe")
