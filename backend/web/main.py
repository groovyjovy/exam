from fastapi import FastAPI, Depends, status, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.init import Book

app = FastAPI()

class BookData(BaseModel):
    title: str
    author: str
    price: int

class BookCreate(BaseModel):
    book: BookData

# データベースセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/health-check")
def health_check():
    return {"message": "ok"}

@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book_create: BookCreate, response: Response, db: Session = Depends(get_db)):
    book_data = book_create.book
    db_book = Book(title=book_data.title, author=book_data.author, price=book_data.price)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    response.headers["Location"] = f"/books/{db_book.id}"
    return db_book
