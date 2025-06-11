import boto3
import pandas as pd
import sys
import io
import os
import zipfile


def upload_csv(s3, df, bucket, key):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())


def zip_csv_files(file_list, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in file_list:
            zipf.write(file, arcname=os.path.basename(file))
    return zip_name

    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python s3_upload.py <input_file> <dst_bucket> <dst_key> <date>")
        sys.exit(1)
    input_file = sys.argv[1]
    dst_bucket = sys.argv[2]
    dst_key = sys.argv[3]
    date = sys.argv[4]
    s3 = boto3.client('s3')
    df = pd.read_csv(input_file)
    upload_csv(s3, df, dst_bucket, dst_key)
    print(f"Uploaded {input_file} to s3://{dst_bucket}/{dst_key}")
