# examへようこそ

## リポジトリの概要
本リポジトリは課題として示された目標を達成するためのリポジトリです

## 環境構築
- 前提条件
    - `docker compose`コマンドを実行できる
1. コンテナをビルド、立ち上げ
    ```
    docker compose up -d
    ```
2. サンプルデータのセットアップ
    ```
     docker compose exec api sh -c 'alembic upgrade head && python seeds/seed.py'
    ```
3. [ページ](http://localhost:4000/books)にアクセス

### DBのmigration実行方法

- 最新バージョンへのmigarate。引数を変えればそのバージョンにmigrate可能
    ```
    alembic upgrade head
    ```
- migrationの初期化。引数を変えればそのバージョンにrollback可能
    ```
    alembic downgrade base
    ```
- 現在のバージョンの確認方法。DBを直接みても確認できる
    ```
    alembic history
    ```
    ```
    select * from  alembic_version;
    ```

### テストの実行方法
- DBの作成、設定
    ```
    docker compose exec db mysql -u root -psecret -e "CREATE DATABASE exam_test; GRANT ALL PRIVILEGES ON exam_test.* TO 'user'@'%'; FLUSPRIVILEGE"
    ```
- コマンドを実行
    ```
    docker compose exec api sh -c 'poetry run pytest'   
    ```

### lintの実行
- コマンドを実行
    ```
    docker compose exec api sh -c 'poetry run ruff check'
    ```
