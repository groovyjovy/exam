from models.init import Book, Review
from db.database import SessionLocal

def seed_data():
    db = SessionLocal()
    book1 = Book(title="Book 1", author="Author 1", price=100)
    book2 = Book(title="Book 2", author="Author 2", price=150)
    book3 = Book(title="Book 3", author="Author 3", price=200)
    db.add(book1)
    db.add(book2)
    db.add(book3)
    db.commit()

    review1 = Review(reviewer_name="Reviewer 1", content="Great book", rating=5, book_id=book1.id)
    review2 = Review(reviewer_name="Reviewer 2", content="Excellent read", rating=4, book_id=book1.id)
  
    db.add(review1)
    db.add(review2)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_data()
