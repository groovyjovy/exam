from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.init import Base, Book, Review
from web.main import app
from db.database import DATABASE_URL, get_db

TEST_DATABASE_URL = DATABASE_URL + "_test"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

client = TestClient(app)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_create():
    db = TestingSessionLocal()
    test_book = Book(title="Test Book for Review", author="Author Review", price=250)
    db.add(test_book)
    db.commit()
    db.refresh(test_book)

    review_data = {
        "review": {
            "reviewer_name": "Reviewer",
            "content": "This is a review content",
            "rating": 5
        }
    }

    response = client.post(f"/api/v1/books/{test_book.id}/reviews", json=review_data)
    db.commit()
    assert response.status_code == 201
    data = response.json()
    assert data['reviewer_name'] == "Reviewer"
    assert data['content'] == "This is a review content"
    assert data['rating'] == 5
    assert data['book_id'] == test_book.id

    test_review = db.get(Review, data["id"])
    db.delete(test_review)
    db.delete(test_book)
    db.commit()
    db.close()

def test_index():
    db = TestingSessionLocal()
    test_book = Book(title="Test Book for Reviews", author="Author Reviews", price=250)
    db.add(test_book)
    db.commit()
    db.refresh(test_book)

    test_review1 = Review(reviewer_name="Reviewer1", content="Review content 1", rating=4, book_id=test_book.id)
    test_review2 = Review(reviewer_name="Reviewer2", content="Review content 2", rating=5, book_id=test_book.id)
    db.add(test_review1)
    db.add(test_review2)
    db.commit()
    db.refresh(test_review1)
    db.refresh(test_review2)

    response = client.get(f"/api/v1/books/{test_book.id}/reviews")
    assert response.status_code == 200
    reviews = response.json()
    assert len(reviews) == 2

    db.delete(test_review1)
    db.delete(test_review2)
    db.delete(test_book)
    db.commit()
    db.close()

def test_show():
    db = TestingSessionLocal()
    test_book = Book(title="Test Book for Single Review", author="Author Single Review", price=300)
    db.add(test_book)
    db.commit()
    db.refresh(test_book)

    test_review = Review(reviewer_name="Single Reviewer", content="Single review content", rating=3, book_id=test_book.id)
    db.add(test_review)
    db.commit()
    db.refresh(test_review)

    response = client.get(f"/api/v1/books/{test_book.id}/reviews/{test_review.id}")
    assert response.status_code == 200
    review_data = response.json()
    assert review_data['content'] == "Single review content"

    db.delete(test_review)
    db.delete(test_book)
    db.commit()
    db.close()

def test_update():
    db = TestingSessionLocal()
    test_book = Book(title="Test Book for Update Review", author="Author Update Review", price=350)
    db.add(test_book)
    db.commit()
    db.refresh(test_book)

    test_review = Review(reviewer_name="Update Reviewer", content="Update review content", rating=3, book_id=test_book.id)
    db.add(test_review)
    db.commit()
    db.refresh(test_review)

    updated_review_data = {
        "review": {
            "reviewer_name": "Updated Reviewer",
            "content": "Updated review content",
            "rating": 4
        }
    }

    response = client.put(f"/api/v1/books/{test_book.id}/reviews/{test_review.id}", json=updated_review_data)
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data['reviewer_name'] == "Updated Reviewer"
    assert updated_data['content'] == "Updated review content"
    assert updated_data['rating'] == 4

    db.delete(test_review)
    db.delete(test_book)
    db.commit()
    db.close()

def test_delete():
    db = TestingSessionLocal()
    test_book = Book(title="Test Book for Delete Review", author="Author Delete Review", price=400)
    db.add(test_book)
    db.commit()
    db.refresh(test_book)

    test_review = Review(reviewer_name="Delete Reviewer", content="Delete review content", rating=2, book_id=test_book.id)
    db.add(test_review)
    db.commit()
    db.refresh(test_review)

    response = client.delete(f"/api/v1/books/{test_book.id}/reviews/{test_review.id}")
    assert response.status_code == 204
