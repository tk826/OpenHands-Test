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
