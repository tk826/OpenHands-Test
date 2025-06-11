import boto3
import pandas as pd
import io
import sys

def list_csv_files(s3, bucket, prefix, date):
    paginator = s3.get_paginator('list_objects_v2')
    files = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if key.endswith('.csv') and date in key:
                files.append(key)
    return files

def download_csv(s3, bucket, key):
    obj = s3.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(io.BytesIO(obj['Body'].read()))

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python s3_download.py <src_bucket> <src_prefix> <date> <output_dir>")
        sys.exit(1)
    src_bucket = sys.argv[1]
    src_prefix = sys.argv[2]
    date = sys.argv[3]
    output_dir = sys.argv[4]
    s3 = boto3.client('s3')
    files = list_csv_files(s3, src_bucket, src_prefix, date)
    if not files:
        print(f"No files found for date {date} in {src_bucket}/{src_prefix}")
        sys.exit(0)
    os.makedirs(output_dir, exist_ok=True)
    for key in files:
        df = download_csv(s3, src_bucket, key)
        filename = key.split('/')[-1]
        df.to_csv(f"{output_dir}/{filename}", index=False)
        print(f"Downloaded {key} to {output_dir}/{filename}")
