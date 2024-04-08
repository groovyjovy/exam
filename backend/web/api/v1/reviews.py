from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from models.init import Book, Review
from db.database import get_db
from schemas.reviews import ReviewCreate, ReviewCreateData, ReviewUpdateData

router = APIRouter()

@router.post("", status_code=status.HTTP_201_CREATED)
def create(book_id: int, review_create: ReviewCreate, response: Response, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404,  detail="Book not found")

    review_data = review_create.review
    review = Review(reviewer_name=review_data.reviewer_name, content=review_data.content, rating=review_data.rating, book_id=book_id)

    db.add(review)
    db.commit()
    db.refresh(review)

    response.headers["Location"] = f"/books/{book.id}/reviews/{review.id}"
    return review

@router.get("", response_model=list[ReviewUpdateData], status_code=status.HTTP_200_OK)
def index(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404,  detail="Book not found")

    reviews = book.reviews
    return reviews

@router.get("/{review_id}", response_model=ReviewUpdateData, status_code=status.HTTP_200_OK)
def show(book_id: int, review_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404,  detail="Book not found")

    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404,  detail="Review not found")
    return review

@router.put("/{review_id}", response_model=ReviewCreateData, status_code=status.HTTP_200_OK)
def update(book_id: int, review_id: int, review_update: ReviewCreate, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404,  detail="Book not found")

    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404,  detail="Review not found")
    
    req_review_data = review_update.review
    review.reviewer_name = req_review_data.reviewer_name
    review.content = req_review_data.content
    review.rating = req_review_data.rating
    db.commit()
    return review

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(book_id: int, review_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404,  detail="Book not found")

    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404,  detail="Review not found")
    
    db.delete(review)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
