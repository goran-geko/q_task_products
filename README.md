# Setup local env
Build all docker images:

`docker-compose build`

Start all containers:

`docker-compose up -d`

Run migrations to create DB schema:

`docker-compose exec web python manage.py migrate`

Run fixtures to insert dummy data:

`docker-compose exec web python manage.py loaddata products/fixtures.json`

# Notes to myself
We can generate fixtures from DB by running this command:

`dc exec web python manage.py dumpdata -o products/fixtures.json products auth.User authtoken.Token`

# Future ideas

1. Using keycloak as user directory
2. Running average rating calculation as an async task on celery
3. Caching API views
4. ...