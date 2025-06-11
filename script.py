import subprocess
import sys
import os
from dotenv import load_dotenv


def run(cmd):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(result.returncode)

def main():
    load_dotenv()
    src_bucket = os.getenv('SRC_BUCKET')
    src_prefix = os.getenv('SRC_PREFIX')
    date = os.getenv('DATE')
    download_dir = os.getenv('DOWNLOAD_DIR')
    columns_file = os.getenv('COLUMNS_FILE')
    checked_dir = os.getenv('CHECKED_DIR')
    dst_bucket = os.getenv('DST_BUCKET')
    dst_key = os.getenv('DST_KEY')

    required_vars = [src_bucket, src_prefix, date, download_dir, columns_file, checked_dir, dst_bucket, dst_key]
    if not all(required_vars):
        print("Error: One or more required environment variables are missing in .env file.")
        sys.exit(1)

    # 1. S3 Download
    run([sys.executable, "s3_download.py", src_bucket, src_prefix, date, download_dir])

    # 2. Check Process
    run([sys.executable, "check_process.py", download_dir, columns_file, checked_dir])

    # 3. S3 Upload
    checked_file = os.path.join(checked_dir, "checked.csv")
    run([sys.executable, "s3_upload.py", checked_file, dst_bucket, dst_key, date])

if __name__ == "__main__":
    main()
