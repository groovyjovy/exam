from pydantic import BaseModel


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

