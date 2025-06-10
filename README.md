# OpenHands-Test
## Dockerによるビルドと実行

### ビルド
```sh
docker build -t myapp .
```
pip install -r requirements.txt


### 実行
```sh
docker run --rm -it -v $(pwd):/app myapp
```

## テストのビルドと実行

### テストのビルド
（テスト用Dockerfileがある場合はその説明を記載。なければ通常のDockerfileでテストを実行する方法を記載）

### テストの実行
```sh
docker run --rm -it -v $(pwd):/app myapp python -m unittest
```
docker run --rm -it -v $(pwd):/app myapp pytest


### test_check_values.py の実行方法
```sh
docker run --rm -it -v $(pwd):/app myapp python test_check_values.py
```

