import sys
from pprint import pprint
from fastapi.testclient import TestClient
from web.main import app, get_db  # get_db をインポート
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.init import Base
from db.database import DATABASE_URL

# sys.pathを表示
pprint(sys.path)

# テスト用データベースの設定
TEST_DATABASE_URL = DATABASE_URL + "_test"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# テスト用データベースのセットアップ
Base.metadata.create_all(bind=engine)

# テストクライアントの作成
client = TestClient(app)

# データベースセッションをオーバーライド
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
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Test Author"
    assert data["price"] == 100
