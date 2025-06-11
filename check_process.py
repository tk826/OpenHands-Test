import pandas as pd
# データフレームの値検証とマージ処理を行うスクリプト
# このスクリプトは、指定されたカラムの型に基づいてデータフレームの値を検証し、
# 不正な値があれば警告を出し、値を空文字に置き換えます。
# また、複数CSVファイルのマージやカラム選択、ソート、検証結果の保存も行います。
import sys
import numpy as np
from datetime import datetime as dt

    # df: 入力データフレーム
    # columns_types: (カラム名, 型)のリスト
    #
    # columns_typesの型は 'datetime', 'float', 'int', 'numeric' などを想定。
    # 各カラムの値が指定型に合致するかを検証し、不正な値があれば警告リストに追加し、
    # データフレーム上の該当値を空文字に置き換えます。
    #
    # 戻り値: 警告メッセージのリストdef check_values(df, columns_types):
    warnings = []
    for col, col_type in columns_types:
        # 各カラムごとに型チェックを実施
        if col not in df.columns:
            continue
        if col_type == 'datetime':
            # 日付型の場合、pandasで変換できない値を検出
            invalid_mask = pd.to_datetime(df[col], errors='coerce').isna() & df[col].notna()
            if invalid_mask.any():
                warnings.append(f"[ワーニング] {col}列に不正な日付値があります: {df.loc[invalid_mask, col].tolist()}")
                df.loc[invalid_mask, col] = ''
        elif col_type in ('float', 'int', 'numeric'):
            # 数値型の場合、float変換できない値を検出
            def is_number(x):
                # xが数値として扱えるか判定する補助関数
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
        # 検出した警告を出力
        print(w)
# コマンドライン引数からディレクトリやカラム情報を受け取り、CSVをマージ・検証・保存
#
# 引数:
#   input_dir: 入力CSVファイルが格納されたディレクトリ
#   columns_file: カラム名と型情報が記載されたテキストファイル
#   output_dir: 検証済みCSVの出力先ディレクトリ
#
# columns_fileは「カラム名:型」の形式で各行に記載
#
# 入力ディレクトリ内の全CSVをマージし、指定カラム順に並べ替え、型検証を行い、
# 問題なければoutput_dir/checked.csvに保存する。
    return warnings

if __name__ == "__main__":
    if len(sys.argv) < 4:
        # 引数不足時は使い方を表示して終了
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
    # 入力ディレクトリにCSVがなければ終了
    if not files:
        print(f"No CSV files found in {input_dir}")
        sys.exit(0)
    dfs = [pd.read_csv(f) for f in files]
    merged = pd.concat(dfs)
    # 日付順にソートし、指定カラム順に並べ替え
    merged = merged.sort_values('datetime')
    merged = merged[columns]
    errors = check_values(merged, columns_types)
    # 検証エラーがあれば内容を表示して終了
    if errors:
        print("値チェックエラー:")
        for err in errors:
            print(err)
        sys.exit(1)
    # 出力ディレクトリを作成し、検証済みCSVを保存
    os.makedirs(output_dir, exist_ok=True)
    merged.to_csv(f"{output_dir}/checked.csv", index=False)
    print(f"Checked and saved to {output_dir}/checked.csv")
