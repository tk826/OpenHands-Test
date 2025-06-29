# ベースイメージ
FROM python:3.12-slim

# 必要なパッケージをインストール
RUN pip install boto3 pandas
COPY requirements.txt ./
RUN pip install -r requirements.txt


# 作業ディレクトリを作成
WORKDIR /app

# スクリプトとカラム設定ファイルをコピー
COPY script.py columns.txt test_check_values.py ./

# 入出力ディレクトリを作成
RUN mkdir -p input/group1 output/group1

# エントリポイント
CMD ["python", "script.py"]
