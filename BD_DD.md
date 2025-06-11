# 機能全体設計書

## 1. システム概要
本システムは、AWS S3バケットからCSVファイルをダウンロードし、データの検証・加工を行い、再度S3へアップロードするバッチ処理を提供します。主な処理はPythonスクリプトで実装されています。

## 2. 処理フロー図

```mermaid
graph TD;
    A[開始] --> B[S3からCSV一覧取得]
    B --> C[CSVダウンロード]
    C --> D[データ検証]
    D --> E[データ加工]
    E --> F[S3へアップロード]
    F --> G[ZIP圧縮（必要時）]
    G --> H[終了]
```

## 3. 機能一覧
1. S3からのCSVファイル一覧取得
2. CSVファイルのダウンロード
3. データ検証（型チェック・日付チェック等）
4. データ加工
5. 加工済みCSVのS3アップロード
6. 複数CSVのZIP圧縮

## 4. 各機能の詳細
### 4.1 S3からのCSVファイル一覧取得
```mermaid
graph TD;
    A[開始] --> B[S3からCSV一覧取得]
    B --> C[CSVファイルリスト取得完了]
    C --> D[終了]
```
- 指定バケット・プレフィックス・日付でCSVファイルをリストアップ
- `s3_download.py` の `list_csv_files` 関数で実装

### 4.2 CSVファイルのダウンロード
```mermaid
graph TD;
    A[開始] --> B[CSVダウンロード]
    B --> C[DataFrameへ読み込み]
    C --> D[終了]
```
- S3から対象CSVをダウンロードしPandas DataFrameとして読み込み
- `s3_download.py` の `download_csv` 関数で実装

### 4.3 データ検証
```mermaid
graph TD;
    A[開始] --> B[型チェック]
    B --> C[日付・数値チェック]
    C --> D[警告出力]
    D --> E[終了]
```
- columns.txtで定義された型情報に基づき、各カラムの型チェックを実施
- 日付型・数値型の不正値を検出し、警告を出力
- `check_process.py` の `check_values` 関数で実装

### 4.4 データ加工
```mermaid
graph TD;
    A[開始] --> B[DataFrame加工]
    B --> C[加工内容拡張]
    C --> D[終了]
```
- 必要に応じてDataFrameの加工処理を実施（例：欠損値補完、不要カラム削除等）
- 加工内容は要件に応じて拡張可能

### 4.5 加工済みCSVのS3アップロード
```mermaid
graph TD;
    A[開始] --> B[CSVをS3へアップロード]
    B --> C[アップロード完了]
    C --> D[終了]
```
- 加工後のDataFrameをCSVとしてS3へアップロード
- `s3_upload.py` の `upload_csv` 関数で実装


### 4.6 複数CSVのZIP圧縮
```mermaid
graph TD;
    A[開始] --> B[CSVファイルをZIP圧縮]
    B --> C[ZIPファイル作成完了]
    C --> D[終了]
```
- 複数CSVファイルをZIP形式でまとめる
- `s3_upload.py` の `zip_csv_files` 関数で実装

## 5. ディレクトリ構成
- script.py: メインバッチスクリプト
- s3_download.py: S3からのダウンロード関連
- s3_upload.py: S3へのアップロード・ZIP圧縮関連
- check_process.py: データ検証処理
- columns.txt: カラム名と型定義
- test_*.py: 各種ユニットテスト

## 6. 環境変数
- .envファイルでS3バケット名、プレフィックス、日付、ダウンロードディレクトリ等を指定

---
2025年6月11日 作成
