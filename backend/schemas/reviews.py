from pydantic import BaseModel, constr, conint

class ReviewCreateData(BaseModel):
    reviewer_name: constr(min_length=1)
    content: constr(min_length=1)
    rating: conint(ge=1, le=5)

class ReviewCreate(BaseModel):
    review: ReviewCreateData

class ReviewUpdateData(BaseModel):
    id: int
    reviewer_name: constr(min_length=1)
    content: constr(min_length=1)
    rating: conint(ge=1, le=5)

class ReviewUpdate(BaseModel):
    review: ReviewUpdateData
