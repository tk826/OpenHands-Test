import os
import pandas as pd
import tempfile
import types
import pytest

import s3_download

def test_list_csv_files():
    class DummyS3:
        def get_paginator(self, _):
            class Page:
                def paginate(self, Bucket, Prefix):
                    return [
                        {'Contents': [
                            {'Key': f'{Prefix}2024-01-01_foo.csv'},
                            {'Key': f'{Prefix}2024-01-01_bar.csv'},
                            {'Key': f'{Prefix}2024-01-02_baz.csv'},
                        ]}
                    ]
            return Page()
    s3 = DummyS3()
    files = s3_download.list_csv_files(s3, 'bucket', 'prefix/', '2024-01-01')
    assert len(files) == 2
    assert all('2024-01-01' in f for f in files)

def test_download_csv(monkeypatch):
    class DummyS3:
        def get_object(self, Bucket, Key):
            import io
            df = pd.DataFrame({'a': [1,2], 'b': [3,4]})
            buf = io.BytesIO()
            df.to_csv(buf, index=False)
            buf.seek(0)
            return {'Body': buf}
    s3 = DummyS3()
    df = s3_download.download_csv(s3, 'bucket', 'key')
    assert list(df.columns) == ['a', 'b']
    assert df.shape == (2,2)
