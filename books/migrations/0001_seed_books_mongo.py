import os
import random
from datetime import datetime
from time import sleep

from django.db import migrations
from pymongo.errors import ServerSelectionTimeoutError
from pymongo import MongoClient


def seed_books_mongo(apps, schema_editor):
    """
    Seeds the MongoDB 'books' collection with 50 sample book documents.
    Uses environment variables for connection details.
    """

    print("seed_books_mongo...")
    mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017")
    mongo_db_name = os.getenv("MONGO_DB_NAME", "bookmanager")

    max_retries = 10
    for attempt in range(max_retries):
        try:
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            client.server_info()  # force connection
            break
        except ServerSelectionTimeoutError:
            print(
                f"MongoDB not available, attempt {attempt+1}/{max_retries}. Waiting 5s..."
            )
            sleep(5)
    else:
        raise Exception("Could not connect to MongoDB after several attempts")

    try:
        client = MongoClient(mongo_uri)
        db = client[mongo_db_name]
        books_collection = db["books"]

        # Skip seeding if collection already has data
        if books_collection.count_documents({}) > 0:
            print("Books already exist in MongoDB — skipping seed.")
            return

        titles = [
            "Clean Code",
            "The Pragmatic Programmer",
            "Design Patterns",
            "Refactoring",
            "Domain-Driven Design",
            "Code Complete",
            "Effective Java",
            "Python Crash Course",
            "Fluent Python",
            "Automate the Boring Stuff",
            "You Don't Know JS",
            "Eloquent JavaScript",
            "Java Concurrency in Practice",
            "Head First Design Patterns",
            "Introduction to Algorithms",
            "Structure and Interpretation of Computer Programs",
            "Cracking the Coding Interview",
            "Deep Learning with Python",
            "Hands-On Machine Learning",
            "Artificial Intelligence: A Modern Approach",
            "Learning SQL",
            "Pro Git",
            "Test-Driven Development by Example",
            "Continuous Delivery",
            "Clean Architecture",
            "Microservices Patterns",
            "Building Microservices",
            "The Mythical Man-Month",
            "Software Engineering at Google",
            "Working Effectively with Legacy Code",
            "Agile Estimating and Planning",
            "Extreme Programming Explained",
            "Peopleware",
            "Accelerate",
            "Site Reliability Engineering",
            "Release It!",
            "The Art of Computer Programming",
            "The Clean Coder",
            "Modern Operating Systems",
            "Computer Networks",
            "Programming Pearls",
            "Grokking Algorithms",
            "Think Python",
            "Effective Python",
            "Data Science for Business",
            "Machine Learning Yearning",
            "System Design Interview",
            "Linux Pocket Guide",
            "Python Tricks",
            "Learn Python the Hard Way",
        ]

        authors = [
            "Robert C. Martin",
            "Andrew Hunt",
            "Erich Gamma",
            "Martin Fowler",
            "Eric Evans",
            "Steve McConnell",
            "Joshua Bloch",
            "Al Sweigart",
            "Luciano Ramalho",
            "Kyle Simpson",
            "Marijn Haverbeke",
            "Brian Goetz",
            "Thomas Cormen",
            "Harold Abelson",
            "Gayle Laakmann",
            "François Chollet",
            "Aurélien Géron",
            "Stuart Russell",
            "Alan Beaulieu",
            "Scott Chacon",
            "Kent Beck",
            "Jez Humble",
            "Michael Feathers",
            "Tom DeMarco",
            "Donald Knuth",
            "Gene Kim",
            "Abhijit Khare",
            "Brett Slatkin",
        ]

        genres = [
            "Programming",
            "Software Engineering",
            "Computer Science",
            "AI",
            "Machine Learning",
            "Databases",
            "Web Development",
            "Cloud Computing",
            "Algorithms",
            "DevOps",
        ]

        # Create 50 random book documents
        books = []
        for i in range(50):
            title = titles[i % len(titles)]
            author = random.choice(authors)
            published_year = random.randint(1990, 2025)
            published_date = datetime(
                published_year, random.randint(1, 12), random.randint(1, 28)
            )

            books.append(
                {
                    "title": title,
                    "author": author,
                    "year": published_year,
                    "published_date": published_date.strftime("%Y-%m-%d"),
                    "genre": random.choice(genres),
                    "price": round(random.uniform(10, 150), 2),
                }
            )

        books_collection.insert_many(books)
        print(f"✅ Inserted {len(books)} books into MongoDB.")

    except Exception as e:
        print(f"Failed to seed MongoDB: {e}")


def remove_books_mongo(apps, schema_editor):
    """
    Removes all documents from the 'books' collection.
    Used for rollback.
    """
    mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017")
    mongo_db_name = os.getenv("MONGO_DB_NAME", "bookmanager")

    try:
        client = MongoClient(mongo_uri)
        db = client[mongo_db_name]
        db.books.delete_many({})
        print("Removed all books from MongoDB (rollback).")
    except Exception as e:
        print(f"Failed to clean up MongoDB: {e}")


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.RunPython(seed_books_mongo, remove_books_mongo),
    ]
