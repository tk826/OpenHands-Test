import os
import subprocess
import shutil
import pandas as pd

def setup_module(module):
    os.makedirs('input/group1', exist_ok=True)
    with open('columns.txt', 'w') as f:
        f.write('datetime\nvalue1\n')
    with open('input/group1/2025-06-10_1.csv', 'w') as f:
        f.write('datetime,value1\n2025-06-10 12:00:00,123\n2025-06-10 13:00:00,456\n')
    with open('input/group1/2025-06-10_2.csv', 'w') as f:
        f.write('datetime,value1\n2025-06-10 14:00:00,789\n2025-06-10 15:00:00,abc\n')

def teardown_module(module):
    shutil.rmtree('input', ignore_errors=True)
    shutil.rmtree('output', ignore_errors=True)
    if os.path.exists('columns.txt'):
        os.remove('columns.txt')

def test_value_check(capsys):
    result = subprocess.run(['python3', 'script.py', '2025-06-10'], capture_output=True, text=True)
    assert 'Invalid numeric in column' in result.stdout
    assert 'abc' in result.stdout
    assert os.path.exists('output/group1/2025-06-10.csv')
    df = pd.read_csv('output/group1/2025-06-10.csv')
    assert df.shape[0] == 4
    assert 'abc' in df['value1'].values
