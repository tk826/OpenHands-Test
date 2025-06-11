import pandas as pd
import s3_upload

def test_upload_csv(monkeypatch):
    class DummyS3:
        def __init__(self):
            self.uploaded = {}
        def put_object(self, Bucket, Key, Body):
            self.uploaded[(Bucket, Key)] = Body
    s3 = DummyS3()
    df = pd.DataFrame({'a': [1,2], 'b': [3,4]})
    s3_upload.upload_csv(s3, df, 'bucket', 'key.csv')
    assert ('bucket', 'key.csv') in s3.uploaded
    body = s3.uploaded[('bucket', 'key.csv')]
    assert 'a,b' in body and '1,3' in body

def test_zip_csv_files(tmp_path):
    import os
    import zipfile
    # Create 11 dummy CSV files
    files = []
    for i in range(11):
        f = tmp_path / f"file_{i}.csv"
        f.write_text(f"col1,col2\n{i},val{i}")
        files.append(str(f))
    zip1 = tmp_path / "batch1.zip"
    zip2 = tmp_path / "batch2.zip"
    # First 10 files
    s3_upload.zip_csv_files(files[:10], str(zip1))
    # Last 1 file
    s3_upload.zip_csv_files(files[10:], str(zip2))
    # Check contents
    with zipfile.ZipFile(zip1) as z1:
        assert len(z1.namelist()) == 10
        for i in range(10):
            assert f"file_{i}.csv" in z1.namelist()
    with zipfile.ZipFile(zip2) as z2:
        assert z2.namelist() == ["file_10.csv"]


def test_zip_directory_and_upload(monkeypatch, tmp_path):
    import zipfile
    import types
    # Create dummy files in a directory
    d = tmp_path / "data"
    d.mkdir()
    (d / "a.csv").write_text("a,b\n1,2")
    (d / "b.txt").write_text("hello")
    (d / "subdir").mkdir()
    (d / "subdir" / "c.csv").write_text("x,y\n3,4")
    # Patch boto3.client to dummy
    uploaded = {}
    class DummyS3:
        def put_object(self, Bucket, Key, Body):
            uploaded[(Bucket, Key)] = Body
    monkeypatch.setattr("boto3.client", lambda *a, **kw: DummyS3())
    # Patch sys.argv
    import s3_upload
    s3_upload.main([str(d), "bucket", "key.csv", "20250101"])
    # Check upload
    assert ("bucket", "key.zip") in uploaded
    # Check zip content
    from io import BytesIO
    zf = zipfile.ZipFile(BytesIO(uploaded[("bucket", "key.zip")]))
    names = set(zf.namelist())
    assert names == {"a.csv", "b.txt", "subdir/c.csv"}

