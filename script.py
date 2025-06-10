import pandas as pd
import glob
import os
import sys

# コマンドライン引数で日付のみ受け取る
if len(sys.argv) < 2:
    print("Usage: python script.py YYYY-MM-DD")
    sys.exit(1)
date = sys.argv[1]

# columns.txtから出力カラムを取得
with open('columns.txt') as f:
    columns = [line.strip() for line in f if line.strip()]

# --- S3部分（ローカル実行時はコメントアウト） ---
# import boto3
# import io
# s3 = boto3.client('s3')
# src_bucket = 'your-source-bucket'
# dst_bucket = 'your-destination-bucket'
# src_prefix = f'input/{group}/'
# dst_prefix = f'output/{group}/'
# def list_csv_files(bucket, prefix, date):
#     paginator = s3.get_paginator('list_objects_v2')
#     files = []
#     for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
#         for obj in page.get('Contents', []):
#             key = obj['Key']
#             if key.endswith('.csv') and date in key:
#                 files.append(key)
#     return files
# def download_csv(bucket, key):
#     obj = s3.get_object(Bucket=bucket, Key=key)
#     return pd.read_csv(io.BytesIO(obj['Body'].read()))
# def upload_csv(df, bucket, key):
#     csv_buffer = io.StringIO()
#     df.to_csv(csv_buffer, index=False)
#     s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())
# --- S3実行部分 ---
# group_list_s3 = []
# response = s3.list_objects_v2(Bucket=src_bucket, Prefix='input/', Delimiter='/')
# for prefix in response.get('CommonPrefixes', []):
#     group = prefix['Prefix'].split('/')[1]
#     group_list_s3.append(group)
# for group in group_list_s3:
#     src_prefix = f'input/{group}/'
#     dst_prefix = f'output/{group}/'
#     files = list_csv_files(src_bucket, src_prefix, date)
#     if not files:
#         print(f"No files found for date {date} in group {group} (S3).")
#         continue
#     dfs = [download_csv(src_bucket, f) for f in files]
#     if not dfs:
#         continue
#     # 共通処理（S3/ローカルどちらでも使う）
#     merged = pd.concat(dfs)
#     merged = merged.sort_values('datetime')
#     merged = merged[columns]
#     output_key = f"{dst_prefix}{date}.csv"
#     upload_csv(merged, dst_bucket, output_key)
#     print(f"Uploaded merged file to s3://{dst_bucket}/{output_key}")

# --- ローカル実行部分 ---
input_root = "input"
group_list = [d for d in os.listdir(input_root) if os.path.isdir(os.path.join(input_root, d))]
if not group_list:
    print("No group directories found under input/.")
    sys.exit(0)

for group in group_list:
    input_dir = os.path.join(input_root, group)
    pattern = os.path.join(input_dir, f"{date}_*.csv")
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"No files found for date {date} in group {group}.")
        continue
    dfs = [pd.read_csv(f) for f in files]
    merged = pd.concat(dfs)
    merged = merged.sort_values('datetime')
    # --- 値チェック追加 ---
    for col in columns:
        if col not in merged.columns:
            print(f"Column {col} not found in merged data.")
            continue
        if col == 'datetime':
            # 日付時間チェック
            invalid = ~pd.to_datetime(merged[col], errors='coerce').notna()
            if invalid.any():
                print(f"Invalid datetime in column '{col}':\n{merged.loc[invalid, col]}")
        else:
            # 数値チェック
            invalid = ~pd.to_numeric(merged[col], errors='coerce').notna()
            if invalid.any():
                print(f"Invalid numeric in column '{col}':\n{merged.loc[invalid, col]}")

    merged = merged[columns]
    output_dir = f"output/{group}/"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{date}.csv")
    merged.to_csv(output_file, index=False)
    print(f"出力ファイル: {output_file}")
