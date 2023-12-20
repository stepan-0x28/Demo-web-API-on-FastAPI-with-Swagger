# Demo web API on FastAPI with Swagger

### My first demo project on FastAPI with Swagger

- asynchronous
- SQLAlchemy
- Pydantic
- other libraries

### Launch (Docker)

#### Creating a network:

```
docker network create demo-web-api-network
```

#### Launching the DBMS:

```
docker pull postgres
```

```
docker run -d \
-p 5432:5432 \
--name demo-web-api-dbms \
--network demo-web-api-network \
-e POSTGRES_PASSWORD=password \
-e POSTGRES_USER=user \
-e POSTGRES_DB=db \
-e PGDATA=/var/lib/postgresql/data/pgdata \
-v /var/lib/demowebapi/data:/var/lib/postgresql/data \
-v $(pwd)/initialization.sql:/docker-entrypoint-initdb.d/initialization.sql:ro \
postgres
```

#### Launching the web API:

```
docker build -t demowebapi .
```

```
docker run -d \
--name demo-web-api \
--network demo-web-api-network \
-e DATABASE_HOST=demo-web-api-dbms \
-e DATABASE_NAME=db \
-e DATABASE_PASSWORD=password \
-e DATABASE_USERNAME=user \
-e ENCRYPTION_KEY=116dbf4ce038d9e961cf1bfb03aa6f007389b4760fe2b1deb94a806af2b29ad0 \
-e UVICORN_ROOT_PATH=/Demo-web-API-on-FastAPI-with-Swagger \
demowebapi
```

#### Launching the web server:

```
docker pull nginx
```

```
docker run -d \
-p 443:443 \
--name demo-web-api-web-server \
--network demo-web-api-network \
-v $(pwd)/demowebapi.conf:/etc/nginx/conf.d/demowebapi.conf:ro \
-v /etc/letsencrypt/live/stepan-0x28.com/fullchain.pem:/etc/letsencrypt/live/stepan-0x28.com/fullchain.pem:ro \
-v /etc/letsencrypt/live/stepan-0x28.com/privkey.pem:/etc/letsencrypt/live/stepan-0x28.com/privkey.pem:ro \
nginx
```