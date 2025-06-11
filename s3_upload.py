import boto3
# CSVファイルまたはZIPをS3へアップロードするスクリプト
# 指定したCSVファイルまたはディレクトリ内の複数CSVをZIP圧縮し、
# S3バケットへアップロードします。
# 10ファイルごとにZIP化し、バッチごとにS3へ保存します。
# 単一CSVの場合はそのままアップロードします。
import pandas as pd
import sys
import io
import os

# s3: boto3クライアント
# df: アップロードするデータフレーム
# bucket: バケット名
# key: アップロード先キー
def upload_csv(s3, df, bucket, key):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())

def zip_csv_files(file_list, zip_path):
    # file_list: 圧縮対象CSVファイルのリスト
    # zip_path: 出力ZIPファイルパス
    #
    # 指定したCSVファイル群を1つのZIPファイルにまとめます。
    import zipfile
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
# コマンドライン引数から入力ファイル/ディレクトリ・S3情報を受け取り、アップロード
#
# 引数:
#   input_file: アップロード元CSVファイルまたはディレクトリ
#   dst_bucket: アップロード先S3バケット名
#   dst_key: アップロード先キー
#   date: 日付（ファイル名やキーに利用）
#
# ディレクトリ指定時は10ファイルごとにZIP化し、バッチごとにS3へ保存します。
# 単一CSVの場合はそのままアップロードします。
        for f in file_list:
            zipf.write(f, arcname=os.path.basename(f))



def main(args):
    if len(args) < 4:
        print("Usage: python s3_upload.py <input_file> <dst_bucket> <dst_key> <date>")
        return 1
    input_path = args[0]
    dst_bucket = args[1]
    dst_key = args[2]
    date = args[3]
    s3 = boto3.client('s3')
    import tempfile
    if os.path.isdir(input_path):
        import zipfile
        zip_path = os.path.join(tempfile.gettempdir(), f'{os.path.basename(input_path)}.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(input_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, input_path)
                    zipf.write(file_path, arcname=arcname)
        key = dst_key.replace('.csv', '.zip') if dst_key.endswith('.csv') else dst_key + '.zip'
        with open(zip_path, 'rb') as f:
            s3.put_object(Bucket=dst_bucket, Key=key, Body=f.read())
        print(f"Uploaded {zip_path} to s3://{dst_bucket}/{key}")
        return 0
    else:
        # 単一CSVファイルの場合はそのままアップロード
        if input_path.endswith('.csv'):
            with open(input_path, 'rb') as f:
                s3.put_object(Bucket=dst_bucket, Key=dst_key, Body=f.read())
            print(f"Uploaded {input_path} to s3://{dst_bucket}/{dst_key}")
            return 0
        else:
            print("対応していないファイル形式です。")
            return 1

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))

