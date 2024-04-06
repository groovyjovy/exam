from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.init import Base, Book
from web.main import app, get_db
from db.database import DATABASE_URL

TEST_DATABASE_URL = DATABASE_URL + "_test"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

client = TestClient(app)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# テスト関数
def test_create_book():
    response = client.post(
        "/books",
        json={
            "book": {
                "title": "Test Book",
                "author": "Test Author",
                "price": 100
            }
        }
    )
    assert response.status_code == 201
    assert response.headers["Location"].startswith("/books/")

def test_index():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_show():
    # 事前にテスト用のデータを挿入
    db = TestingSessionLocal()
    test_book = Book(title="Test Show", author="Author Show", price=200)
    db.add(test_book)
    db.commit()
    db.refresh(test_book)

    response = client.get(f"/books/{test_book.id}")
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "Test Show"
    assert data['author'] == "Author Show"
    assert data['price'] == 200

    # テスト後にクリーンアップ
    db.delete(test_book)
    db.commit()
    db.close()

def test_update():
    # 事前にテスト用のデータを挿入
    db = TestingSessionLocal()
    test_book = Book(title="Test Update", author="Author Update", price=300)
    db.add(test_book)
    db.commit()
    db.refresh(test_book)

    response = client.put(f"/books/{test_book.id}", json={"book": {"title": "Updated Title", "author": "Updated Author", "price": 400}})
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "Updated Title"
    assert data['author'] == "Updated Author"
    assert data['price'] == 400

    # テスト後にクリーンアップ
    db.delete(test_book)
    db.commit()
    db.close()

def test_delete():
    # 事前にテスト用のデータを挿入
    db = TestingSessionLocal()
    test_book = Book(title="Test Delete", author="Author Delete", price=500)
    db.add(test_book)
    db.commit()
    db.refresh(test_book)

    book_id = test_book.id

    db.close()  # このセッションを閉じて、独立したセッションでテストを行う

    # データ削除を実行
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 204

    # 新しいセッションで削除されたかどうかを確認
    new_db = TestingSessionLocal()
    deleted_book = new_db.get(Book, book_id)
    assert deleted_book is None
    new_db.close()
