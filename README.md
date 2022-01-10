<h1>Online Shop on DRF</h1>

<h4>Commands:</h4>
Build the project (docker-compose build):<br>

`make build`

Up the project (docker-compose up -d):<br>
`make up`

Run tests:<br>
`make test`

<h4>Envfile structure:</h4>

```
DJANGO_SETTINGS_MODULE=backend.settings.dev
POSTGRES_DB=backend
POSTGRES_USER=backend
POSTGRES_PASSWORD=backend
POSTGRES_HOST=pg_db
POSTGRES_PORT=5432
SECRET_KEY=123
REDIS_HOST=redis
REDIS_PORT=6379
```

<h4>User guide:</h4>
1. Launch the project via `make up` command.
2. Now you can go to the address `http://0.0.0.0:8000/` and use API.

<h4>Service urls:</h4>
1. `http://0.0.0.0:8000/` - Server url
2. `http://0.0.0.0:8000/admin/` - Django admin panel
3. `http://0.0.0.0:8000/schema/swagger-ui/` - Swagger documentation
