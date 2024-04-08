from pydantic import BaseModel

class ReviewCreateData(BaseModel):
    reviewer_name: str
    content: str
    rating: int

class ReviewCreate(BaseModel):
    review: ReviewCreateData

class ReviewUpdateData(BaseModel):
    id: int
    reviewer_name: str
    content: str
    rating: int

class ReviewUpdate(BaseModel):
    review: ReviewCreateData
