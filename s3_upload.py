import boto3
import pandas as pd
import sys
import io
import os

def upload_csv(s3, df, bucket, key):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())

def zip_csv_files(file_list, zip_path):
    import zipfile
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in file_list:
            zipf.write(f, arcname=os.path.basename(f))


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python s3_upload.py <input_file> <dst_bucket> <dst_key> <date>")
        sys.exit(1)
    input_path = sys.argv[1]
    dst_bucket = sys.argv[2]
    dst_key = sys.argv[3]
    date = sys.argv[4]
    s3 = boto3.client('s3')

    # ZIP圧縮処理
    import glob, tempfile
    if os.path.isdir(input_path):
        csv_files = sorted(glob.glob(os.path.join(input_path, '*.csv')))
        if not csv_files:
            print(f"No CSV files found in {input_path}")
            sys.exit(1)
        zip_files = []
        for i in range(0, len(csv_files), 10):
            zip_path = os.path.join(tempfile.gettempdir(), f'batch_{i//10+1}.zip')
            zip_csv_files(csv_files[i:i+10], zip_path)
            zip_files.append(zip_path)
        for idx, zipf in enumerate(zip_files):
            key = dst_key.replace('.csv', f'_batch{idx+1}.zip') if dst_key.endswith('.csv') else f'{dst_key}_batch{idx+1}.zip'
            with open(zipf, 'rb') as f:
                s3.put_object(Bucket=dst_bucket, Key=key, Body=f.read())
            print(f"Uploaded {zipf} to s3://{dst_bucket}/{key}")
    else:
        # 単一CSVファイルの場合は従来通り
        df = pd.read_csv(input_path)
        upload_csv(s3, df, dst_bucket, dst_key)
        print(f"Uploaded {input_path} to s3://{dst_bucket}/{dst_key}")

