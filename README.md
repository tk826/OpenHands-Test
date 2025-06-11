# OpenHands-Test
## Dockerによるビルドと実行

### ビルド
```sh
docker build -t myapp .
```


### 実行
```sh
docker run --rm -it -v $(pwd):/app myapp
```
```cmd
docker run --rm -it -v "%cd%":/app myapp
```

## テストのビルドと実行

### テストのビルド
（テスト用Dockerfileがある場合はその説明を記載。なければ通常のDockerfileでテストを実行する方法を記載）

### テストの実行
```sh
docker run --rm -it -v $(pwd):/app myapp python
```
```cmd
docker run --rm -it -v "%cd%":/app myapp pytest
```

### test_check_values.py の実行方法
```sh
docker run --rm -it -v $(pwd):/app myapp python test_check_values.py
```
```cmd
docker run --rm -it -v "%cd%":/app myapp python test_check_values.py
```

## 機能全体の設計書

本システムは、AWS S3上のCSVファイルをダウンロードし、データの検証・加工処理を行い、再度S3へアップロードする一連のバッチ処理を自動化するPythonアプリケーションです。

### 機能一覧
1. S3からのCSVファイルダウンロード（`s3_download.py`）
2. データ検証・加工処理（`check_process.py`）
3. S3へのCSVファイルアップロード（`s3_upload.py`）
4. 一連処理の統括実行（`script.py`）

---

### 1. S3からのCSVファイルダウンロード（`s3_download.py`）
- 指定したS3バケット・プレフィックス・日付に一致するCSVファイルをリストアップし、ローカルディレクトリにダウンロードします。
- boto3を利用し、ファイル一覧取得・ダウンロードを実施。
- ダウンロードしたCSVはPandasで読み込み、指定ディレクトリに保存。

#### 入力
- S3バケット名
- プレフィックス
- 日付（ファイル名に含まれる）
- 出力ディレクトリ

#### 出力
- ローカルディレクトリにCSVファイル群

---

### 2. データ検証・加工処理（`check_process.py`）
- 指定ディレクトリ内のCSVファイルを読み込み、カラム定義（`columns.txt`）に従いデータ型チェック・不正値の検出・修正を行います。
- 日付型・数値型の検証、不正値の警告出力。
- 加工後のデータを新たなCSVとして保存。

#### 入力
- 入力ディレクトリ（ダウンロード済みCSV）
- カラム定義ファイル（`columns.txt`）
- 出力ディレクトリ

#### 出力
- 検証・加工済みCSVファイル
- 警告メッセージ（標準出力）

---

### 3. S3へのCSVファイルアップロード（`s3_upload.py`）
- 加工済みCSVファイルまたはディレクトリをS3へアップロードします。
- ファイルが多い場合は10件ごとにZIP圧縮し、バッチでアップロード。
- boto3を利用し、S3へput_object。

#### 入力
- アップロード対象ファイルまたはディレクトリ
- S3バケット名
- アップロード先キー
- 日付

#### 出力
- S3上にアップロードされたCSVまたはZIPファイル

---

### 4. 一連処理の統括実行（`script.py`）
- .envファイル等で指定された環境変数をもとに、1→2→3の処理を自動実行。
- 各ステップでエラー発生時は即時終了。

#### 入力
- 環境変数（S3バケット名、プレフィックス、日付、各種ディレクトリパス等）

#### 出力
- 各ステップの標準出力
- S3上のアップロード結果

---

### カラム定義ファイル（`columns.txt`）
- データ検証時に参照されるカラム名と型の定義ファイル。
- 例：
  - datetime:datetime
  - value1:float

---

## 各機能の詳細設計

### S3ダウンロード（`s3_download.py`）
- boto3のlist_objects_v2でファイル一覧取得
- 指定日付を含むCSVファイルのみ抽出
- get_objectでファイル取得し、Pandasで読み込み
- ローカルに保存

### データ検証・加工（`check_process.py`）
- columns.txtを読み込み、カラム名・型を取得
- 各CSVファイルをPandasで読み込み
- カラムごとに型チェック
  - datetime型: pd.to_datetimeで変換、失敗時は空文字に
  - float/int型: float変換できない値は空文字に
- 不正値は警告として標準出力
- 検証・加工済みCSVを出力ディレクトリに保存

### S3アップロード（`s3_upload.py`）
- ファイル数が多い場合は10件ごとにZIP圧縮
- boto3のput_objectでS3へアップロード
- アップロード後、ファイル名・パスを標準出力

### 統括スクリプト（`script.py`）
- .env等から各種パラメータを取得
- S3ダウンロード→データ検証→S3アップロードを順次実行
- 各ステップでエラー時は即時終了

---


