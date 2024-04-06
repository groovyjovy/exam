from fastapi import FastAPI, Depends, status, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.init import Book

app = FastAPI()

class BookCreateData(BaseModel):
    title: str
    author: str
    price: int

class BookCreate(BaseModel):
    book: BookCreateData

class BookUpdateData(BaseModel):
    id: int
    title: str
    author: str
    price: int

class BookUpdate(BaseModel):
    book: BookUpdateData

# データベースセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health-check")
def health_check():
    return {"message": "ok"}

@app.post("/books", status_code=status.HTTP_201_CREATED)
def create(book_create: BookCreate, response: Response, db: Session = Depends(get_db)):
    book_data = book_create.book
    db_book = Book(title=book_data.title, author=book_data.author, price=book_data.price)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    response.headers["Location"] = f"/books/{db_book.id}"
    return db_book

@app.get("/books", response_model=list[BookUpdateData], status_code=status.HTTP_200_OK)
def index(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

@app.get("/books/{book_id}", response_model=BookUpdateData, status_code=status.HTTP_200_OK)
def show(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=BookUpdateData, status_code=status.HTTP_200_OK)
def update(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    book_data = book_update.book
    db_book.title = book_data.title
    db_book.author = book_data.author
    db_book.price = book_data.price

    db.commit()  # 変更をコミット
    db.refresh(db_book)  # 更新されたオブジェクトでセッションを更新

    return db_book

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(book_id: int, db: Session = Depends(get_db)):
    db_book = db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)  # オブジェクトを削除
    db.commit()  # 変更をコミット

    return Response(status_code=status.HTTP_204_NO_CONTENT)
