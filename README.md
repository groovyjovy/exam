# examへようこそ

## リポジトリの概要
本リポジトリは課題として示された目標を達成するためのリポジトリです

## 環境構築
- 前提条件
1. コンテナをビルド、立ち上げ
    ```
    docker compose up -d
    ```
2. コンテナに入る
    ```
    docker compose exec api bash
    ```
3. サーバーを起動
    ```
    poetry run uvicorn src.main:app --host 0.0.0.0 --reload
    ```

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

## なんとなくの構成、というか盛り込みたい要素
- logをs3に出す
- lamdaでfastapiを動作させる
- s3にvite + reactのspaアプリケーションをアップロードする
    - S3にアップロードしたアプリケーションからauthenticateヘッダーを利用して認証を行う。BASICで
- 型アノテーション
- MUIを利用して効率的にコンポーネントを開発する
- DB設計書を書く。クラス図は簡単なものなので特に書かなくていいかな...
- インフラ構成図を書く。サーバーレスで作成する場合、elbとかは特に書かなくていい？
- OpenAPIに則って書いた方が良い？
- linterを利用して書く
- pytestでテストを書く

## スケジュール
- 4/2(火)
    - 環境構築。ハロワまで行きたい
- 4/3(水)
    - ローカルのDBとの接続。DB設計
- 4/4(木)
    - CRUDAPIの作成
- 4/5(金)
    - CRUDAPIの作成
- 4/6(土)
    - フロントの作成
- 4/7(日)
    - 本番環境の作成
- 4/8(月)
    - 本番環境の作成
- 4/9(火)
    - ドキュメントの作成と提出
- 4/10(水)
    - 面談
