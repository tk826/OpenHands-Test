import pandas as pd
import numpy as np
from check_process import check_values

def test_check_values_datetime(capfd):
    df = pd.DataFrame({
        'datetime': ['2024-01-01 12:00:00', '2024-01-02 13:00:00', 'invalid-date'],
        'value1': [1, 2, 3]
    })
    columns_types = [('datetime', 'datetime'), ('value1', 'float')]
    warnings = check_values(df, columns_types)
    out, _ = capfd.readouterr()
    assert '[ワーニング]' in out
    assert df.loc[2, 'datetime'] == ''

def test_check_values_numeric(capfd):
    df = pd.DataFrame({
        'datetime': ['2024-01-01 12:00:00', '2024-01-02 13:00:00', '2024-01-03 14:00:00'],
        'value1': [1, 'abc', 3]
    })
    columns_types = [('datetime', 'datetime'), ('value1', 'float')]
    warnings = check_values(df, columns_types)
    out, _ = capfd.readouterr()
    assert '[ワーニング]' in out
    assert df.loc[1, 'value1'] == ''

def test_check_values_ok(capfd):
    df = pd.DataFrame({
        'datetime': ['2024-01-01 12:00:00', '2024-01-02 13:00:00', '2024-01-03 14:00:00'],
        'value1': [1, 2.5, np.nan]
    })
    columns_types = [('datetime', 'datetime'), ('value1', 'float')]
    warnings = check_values(df, columns_types)
    out, _ = capfd.readouterr()
    assert not warnings
    assert out == ''
