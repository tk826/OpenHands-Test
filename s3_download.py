import boto3
# S3からCSVファイルをダウンロードするスクリプト
# 指定したバケット・プレフィックス・日付に該当するCSVファイルをS3から検索し、
# ローカルディレクトリにダウンロード保存します。
# ファイル名に日付が含まれるCSVのみを対象とします。
import pandas as pd
import io
import sys

# s3: boto3クライアント
# bucket: バケット名
# prefix: プレフィックス
# date: 対象日付（ファイル名に含まれる）
def list_csv_files(s3, bucket, prefix, date):
    paginator = s3.get_paginator('list_objects_v2')
    files = []
    # S3のオブジェクト一覧をページネーションで取得
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            # ファイル名にdateが含まれるCSVのみ抽出
            if key.endswith('.csv') and date in key:
                files.append(key)
    return files

# コマンドライン引数からS3情報・出力先を受け取り、CSVをダウンロード
#
# 引数:
#   src_bucket: ダウンロード元S3バケット名
#   src_prefix: プレフィックス
#   date: 対象日付（ファイル名に含まれる）
#   output_dir: ダウンロード先ディレクトリ
#
# 指定条件に合致するCSVファイルを全てoutput_dirに保存します。
def download_csv(s3, bucket, key):
    obj = s3.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(io.BytesIO(obj['Body'].read()))

def main(args):
    if len(args) < 4:
        print("Usage: python s3_download.py <src_bucket> <src_prefix> <date> <output_dir>")
        return 1
    src_bucket = args[0]
    src_prefix = args[1]
    date = args[2]
    output_dir = args[3]
    s3 = boto3.client('s3')
    files = list_csv_files(s3, src_bucket, src_prefix, date)
    if not files:
        print(f"No files found for date {date} in {src_bucket}/{src_prefix}")
        return 0
    os.makedirs(output_dir, exist_ok=True)
    for key in files:
        df = download_csv(s3, src_bucket, key)
        filename = key.split('/')[-1]
        df.to_csv(f"{output_dir}/{filename}", index=False)
        print(f"Downloaded {key} to {output_dir}/{filename}")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
