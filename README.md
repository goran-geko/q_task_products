# Setup local env
Build all docker images:

`docker-compose build`

Start all containers:

`docker-compose up -d`

Run migrations to create DB schema:

`docker-compose exec web python manage.py migrate`

Run fixtures to insert dummy data:

`docker-compose exec web python manage.py loaddata products/fixtures.json`

Create `products` index:

`docker-compose exec web python manage.py search_index --create`

Populate `products` index:

`docker-compose exec web python manage.py search_index --populate`

Run all tests:

`docker-compose exec web python manage.py test products`

# Notes to myself
We can generate fixtures from DB by running this command:

`docker-compose exec web python manage.py dumpdata -o products/fixtures.json products auth.User authtoken.Token`

We can generate OpenAPI documentation by running this command:

`docker-compose exec web python manage.py generateschema --file docs/api-opanapi.yml`

# Future ideas

1. Using keycloak as user directory
2. Running average rating calculation as an async task on celery
3. Caching API views
4. ...
