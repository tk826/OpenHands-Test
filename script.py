import subprocess
import sys
import os

def run(cmd):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(result.returncode)

def main():
    if len(sys.argv) != 9:
        print("Usage: python script.py <src_bucket> <src_prefix> <date> <download_dir> <columns_file> <checked_dir> <dst_bucket> <dst_key>")
        sys.exit(1)
    src_bucket, src_prefix, date, download_dir, columns_file, checked_dir, dst_bucket, dst_key = sys.argv[1:9]

    # 1. S3 Download
    run([sys.executable, "s3_download.py", src_bucket, src_prefix, date, download_dir])

    # 2. Check Process
    run([sys.executable, "check_process.py", download_dir, columns_file, checked_dir])

    # 3. S3 Upload
    checked_file = os.path.join(checked_dir, "checked.csv")
    run([sys.executable, "s3_upload.py", checked_file, dst_bucket, dst_key, date])

if __name__ == "__main__":
    main()
