import pandas as pd
# データフレームの値検証とマージ処理を行うスクリプト
import sys
import numpy as np
from datetime import datetime as dt

    # df: 入力データフレーム
    # columns_types: (カラム名, 型)のリスト
def check_values(df, columns_types):
    warnings = []
    for col, col_type in columns_types:
        if col not in df.columns:
            continue
        if col_type == 'datetime':
            invalid_mask = pd.to_datetime(df[col], errors='coerce').isna() & df[col].notna()
            if invalid_mask.any():
                warnings.append(f"[ワーニング] {col}列に不正な日付値があります: {df.loc[invalid_mask, col].tolist()}")
                df.loc[invalid_mask, col] = ''
        elif col_type in ('float', 'int', 'numeric'):
            def is_number(x):
                if pd.isna(x):
                    return True
                if isinstance(x, (int, float, np.integer, np.floating)):
                    return True
                try:
                    float(x)
                    return True
                except Exception:
                    return False
            invalid = ~df[col].apply(is_number)
            if invalid.any():
                warnings.append(f"[ワーニング] {col}列に数値でない値があります: {df.loc[invalid, col].tolist()}")
                df.loc[invalid, col] = ''
        else:
            pass
    for w in warnings:
        print(w)
# コマンドライン引数からディレクトリやカラム情報を受け取り、CSVをマージ・検証・保存
    return warnings

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python check_process.py <input_dir> <columns_file> <output_dir>")
        sys.exit(1)
    input_dir = sys.argv[1]
    columns_file = sys.argv[2]
    output_dir = sys.argv[3]
    import glob, os
    with open(columns_file) as f:
        columns_types = [line.strip().split(":") for line in f if line.strip()]
        columns = [col for col, _type in columns_types]
    files = sorted(glob.glob(f"{input_dir}/*.csv"))
    if not files:
        print(f"No CSV files found in {input_dir}")
        sys.exit(0)
    dfs = [pd.read_csv(f) for f in files]
    merged = pd.concat(dfs)
    merged = merged.sort_values('datetime')
    merged = merged[columns]
    errors = check_values(merged, columns_types)
    if errors:
        print("値チェックエラー:")
        for err in errors:
            print(err)
        sys.exit(1)
    os.makedirs(output_dir, exist_ok=True)
    merged.to_csv(f"{output_dir}/checked.csv", index=False)
    print(f"Checked and saved to {output_dir}/checked.csv")
