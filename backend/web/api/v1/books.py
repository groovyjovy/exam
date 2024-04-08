from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from db.database import get_db
from models.init import Book, Review
from schemas.books import BookCreate, BookCreateData, BookUpdateData

router = APIRouter()

@router.post("", status_code=status.HTTP_201_CREATED)
def create(book_create: BookCreate, response: Response, db: Session = Depends(get_db)):
    req_book_data = book_create.book
    book = Book(title=req_book_data.title, author=req_book_data.author, price=req_book_data.price)
    db.add(book)
    db.commit()
    db.refresh(book)

    response.headers["Location"] = f"/books/{book.id}"
    return book

@router.get("", response_model=list[BookUpdateData], status_code=status.HTTP_200_OK)
def index(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

@router.get("/{book_id}", response_model=BookUpdateData, status_code=status.HTTP_200_OK)
def show(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookCreateData, status_code=status.HTTP_200_OK)
def update(book_id: int, book_update: BookCreate, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    req_book_data = book_update.book
    book.title = req_book_data.title
    book.author = req_book_data.author
    book.price = req_book_data.price

    db.commit()

    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    reviews = db.query(Review).filter(Review.book_id == book_id).all()
    for review in reviews:
        db.delete(review)

    db.delete(book)
    db.commit()



    return Response(status_code=status.HTTP_204_NO_CONTENT)
