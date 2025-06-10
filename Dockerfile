# ベースイメージ
FROM python:3.12-slim

# 必要なパッケージをインストール
RUN pip install boto3 pandas

# 作業ディレクトリを作成
WORKDIR /app

# スクリプトとカラム設定ファイルをコピー
COPY script.py columns.txt ./

# 入出力ディレクトリを作成
RUN mkdir -p input/group1 output/group1

# エントリポイント
CMD ["python", "script.py"]
