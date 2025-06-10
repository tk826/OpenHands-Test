import pandas as pd
import numpy as np
from script import check_values

def test_check_values_datetime():
    df = pd.DataFrame({
        'datetime': ['2024-01-01 12:00:00', '2024-01-02 13:00:00', 'invalid-date'],
        'value1': [1, 2, 3]
    })
    columns = ['datetime', 'value1']
    errors = check_values(df, columns)
    assert any('datetime' in e for e in errors)

def test_check_values_numeric():
    df = pd.DataFrame({
        'datetime': ['2024-01-01 12:00:00', '2024-01-02 13:00:00', '2024-01-03 14:00:00'],
        'value1': [1, 'abc', 3]
    })
    columns = ['datetime', 'value1']
    errors = check_values(df, columns)
    assert any('value1' in e for e in errors)

def test_check_values_ok():
    df = pd.DataFrame({
        'datetime': ['2024-01-01 12:00:00', '2024-01-02 13:00:00', '2024-01-03 14:00:00'],
        'value1': [1, 2.5, np.nan]
    })
    columns = ['datetime', 'value1']
    errors = check_values(df, columns)
    assert not errors
