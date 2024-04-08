from pydantic import BaseModel, constr, conint

class BookCreateData(BaseModel):
    title: constr(min_length=1)
    author: constr(min_length=1)
    price: conint(gt=0)

class BookCreate(BaseModel):
    book: BookCreateData

class BookUpdateData(BaseModel):
    id: int
    title: constr(min_length=1)
    author: constr(min_length=1)
    price: conint(gt=0)

class BookUpdate(BaseModel):
    book: BookUpdateData
