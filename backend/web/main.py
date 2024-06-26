# web/main.py
from fastapi import FastAPI
from .api.v1.books import router as book_router
from .api.v1.reviews import router as review_router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:4000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(book_router, prefix='/api/v1/books')
app.include_router(review_router, prefix='/api/v1/books/{book_id}/reviews')
