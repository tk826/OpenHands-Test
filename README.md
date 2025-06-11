# OpenHands-Test（運用ガイド）

## Dockerによるビルドと実行

### ビルド
```sh
docker build -t myapp .
```

### 実行
```sh
docker run --rm -it -v $(pwd):/app myapp
```
```cmd
docker run --rm -it -v "%cd%":/app myapp
```

## テストの実行
```sh
docker run --rm -it -v $(pwd):/app myapp pytest
```
```cmd
docker run --rm -it -v "%cd%":/app myapp pytest
```

---

## 詳細な設計・機能仕様については「b/設計書.md（ファイル名はb/\350\250\255\350\250\210\346\233\270.md）」を参照してください。
