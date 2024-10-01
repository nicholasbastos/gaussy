# Gaussy URL Shortener Test

## Overview

This is a simple URL shortener service built with Flask and SQLite.

### Running the app (without docker)
1. Run `make install` to install the dependencies locally
2. Run `make dev` to run Flask server

### Running the app (Docker)

To build the Docker image and run the container, run the following command:

```bash
docker compose up
```

## Testing the Application

You can test the application using `curl`. Here are some examples:

1. **Shorten a URL**:

```bash
curl -X POST http://localhost:5000/shorten -H "Content-Type: application/json" -d '{"long_url": "https://https://www.gaussy.com/company"}'
```

2. **Access the shortened URL**:

```bash
http://localhost:5000/<short_url>
```


## Accessing the Database

To access and read the SQLite database, first start the container that will access the container.

1. start database access container:
```bash
docker-compose exec db bash
```

2. Open the gaussy database:
```bash
sqlite3 /app/instance/gaussy.db
```

3. List the tables:

```bash
.tables
```

4. Check content of urls information:
```bash
select * from urls;
```

5. Check analytics of urls accesses:
```bash
select * from url_analytics;
```
