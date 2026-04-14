## 單一命令统治一切，

```bash
docker run -d --name embedchain -p 8080:8080 embedchain/rest-api:latest
```

### 在本機執行應用程式，

```bash
# 會在變更時幫助重新載入
DEVELOPMENT=True && python -m main
```

使用 docker（在本地端），

```bash
docker build -t embedchain/rest-api:latest .
docker run -d --name embedchain -p 8080:8080 embedchain/rest-api:latest
docker image push embedchain/rest-api:latest
```