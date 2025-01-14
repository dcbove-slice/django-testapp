# Django Test App

For this sample project, I'm a bit like most everyone else and a newcomer to Django. I wrote this
project in attempt to get a bit of a feel for it. This isn't a production quality application, but
it does have a handful of things set up to hopefully get you "over the hump" and into exploring
what Django has to offer.

This app mostly just is:

* A RESTful interface that does some basic CRUD stuff for shapes.
* An extremely basic HTML page to show off the shapes.

And among the most obvious reasons this isn't production quality are:
* I've got Basic Auth for the REST endpoints and a default login for the admin console, but I need to look at this more.
* The database and redis are exposing their ports (via the docker-compose file) in a manner that doesn't suit production.
* I've got the DEBUG flags on.

## Project Creation

You don't need to perform these steps if you fetch the project from GitHub.  But, for a new project,
you could just run these commands to make a new project (that's the overarching bit) and one or more
applications.

```
django-admin startproject widget_project .
python manage.py startapp user_app
```

## Initial Setup

If you've fetched the app from source control, here's some steps to follow.  I've assumed that you've got
a bunch of stuff already installed like: python 3.10+, poetry, docker, make and a few other standard things.
Nothing crazy.

### Build the Docker Compose Environment

You need to follow the code below to perform these steps:
* set up the poetry virtual environment with all of the dependencies
* to satisfy the requirements of the `Dockerfile`, generate a `requirements.txt` file from the poetry
  config files.
* run docker compose.

This should set up the shell of a Django application that is available at 8009 and postgres available at 5432.

```
poetry install
poetry export --without-hashes --format=requirements.txt > requirements.txt
python manage.py collectstatic
docker-compose up --build -d
```

### Build a Superuser

Django provides as admin console through which you can view and execute and otherwise perform a bunch of
administrative functions. I've defined a custom user (that is exactly the same as the default user) and you
can configure it here as below.

For the purposes of this, the code below does the following:
* it figures out what all the database migrations should be (at the very least, it has to create the
  schema to support my custom user). In this case though, it should create migrations for at least
  two applications: `user_app` (which contains the custom user) and `shapes` (the rest demo).
* it applies the changes to the datbase.
* it creates a superuser for admin access. choose the username and password you like, but for simplicity i'll
  use a name and password is `superuser`.

```
docker compose exec app python manage.py makemigrations
docker compose exec app python manage.py migrate
docker compose exec app python manage.py createsuperuser
```

### Use the Database

The Django app is currently configured to use the postgres instance running within
the docker compose environment.  You can connect to it and then run a few basic
commands in the `psql` command line environment like this:

```
docker compose exec db psql --username=testapp --dbname widget_dev

\l
\c widget_dev
\dt
\q
```

### Examine Sessions in Redis

In order to support multiple Django instances behind a load balancer without any
sticky session nonsense, session storage is in Redis.

```
docker compose exec redis redis-cli
select 1
keys "*"
```

#### Database Reset

If, amidst your exploration, you can delete all data from your database while leaving your schema
unchanged with: `docker compose exec app python manage.py flush --no-input`.

If there are other things you'd like to do, I provided a "custom command" that you can use as
a template to build other commands into the application:
`docker compose exec app python manage.py do_custom_command`.

## Setup the Shapes App

### App Setup

Django has multiple apps within the project. Here I'm creating a new app named "shapes".
Then i write the code (in the case, the most important thing would be the model object)
and then I run the migration that will build (or update) the schema within the database.

```
python manage.py startapp shapes
<... write code...>
docker compose exec app python manage.py makemigrations
docker compose exec app python manage.py migrate
```

My "shapes" app basically is a RESTful interface to CRUD shapes. The following "Testing" section
demonstrates a bunch of ways to exercise that interface and the underlying code.

## Testing

### Unit (and Functional) Tests

It's always important to have and run tests. In this project, I've divided the tests into two
groups: unit and functional. Unit tests can be run at any time. Functional tests require the
docker compose environment to be running as they run against the database.

Also note that through the use of the `@pytest.mark.django_db` annotation, the data associated
with the running tests is not committed to the database.

#### pytest in VSCode

During development, it's nice to be able to run and debug your unit tests. For this project, you can
debug the tests within VSCode by using these rather standard test settings. I pulled these from
`.vscode/settings.json`.

Again, note, all of this setup specifically regarding the execution of tests within the
IDE is VSCode specific.

```
{
    "python.testing.pytestArgs": [
        "shapes"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
}
```

You'll also need the environment variables set somewhere.  Below you'll see different examples for
where the environment variables come from.  For this scenario, you'll need them exported within the terminal
window where the tests. I put the values in an `.env` file at the base of the project.

```
PYTHONPATH=.:$PYTHONPATH
DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=widget_dev
SQL_USER=testapp
SQL_PASSWORD=testapp
SQL_HOST=localhost
SQL_PORT=5432
DATABASE=postgres
DJANGO_SETTINGS_MODULE=widget_project.settings
```

#### pytest in Docker

Always, and especially during automated processes, it's nice to be able to run all your tests with a simple
command line. Remember, the environmental variables that this relies upon are configured in `.env.dev` and set
within the docker-compose.yml file.

Try these commands to run tests (with and without coverage stats):

```
docker compose exec app python -m pytest
docker compose exec app python -m pytest --cov="shapes"
```

If the docker compose environment isn't up and you just want to run the unit tests, here's a way to do it:

```
python -m pytest "shapes/tests/unit"
```

### Browser Testing in the Admin Console

Everyone likes some visual confirmation that things are working as expected. Here's multiple ways to
connect to the application and try things out. In all cases we are connecting to the postgres instance
running in the docker container. The various options allow us to debug as needed.

#### Browser Testing while Running Django in VSCode

This is an important scenario when attempting to debug. The goal is to start to docker compose
environment as normal in order to take advantage of the database instance running there (and exposed)
on port 5432. But we're going to start to app through a launch configuration, bind it to port 8000
and then try it out.

The valuable thing about this setup is that you can debug the running Django app inside of VSCode.

So:
* Start the docker compose environment: `docker compose up --build -d`.
* Use this launch configuration in VSCode (you can see that the environment variables are set here):
  ```
  {
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Django",
            "type": "debugpy",
            "request": "launch",
            "args": [
                "runserver",
                "0.0.0.0:8000"
            ],
            "env": {
                "DEBUG": "1",
                "SECRET_KEY": "foo",
                "DJANGO_ALLOWED_HOSTS": "localhost 127.0.0.1 [::1]",
                "SQL_ENGINE": "django.db.backends.postgresql",
                "SQL_DATABASE": "widget_dev",
                "SQL_USER": "testapp",
                "SQL_PASSWORD": "testapp",
                "SQL_HOST": "localhost",
                "SQL_PORT": "5432",
                "DATABASE": "postgres",
            },
            "django": true,
            "autoStartBrowser": false,
            "program": "${workspaceFolder}/manage.py"
        }
    ]
  }
  ```
* Test by navigating in your browser to:
  * [http://localhost:8000/admin/] (log in as superuser:superuser if that's how you configured it above)
  * [http://localhost:8000/api/shape/]

#### Browser Testing while Running Django in Docker

This is more straight forward. In this case we are going to try to connect to the Django app via port
8009 as defined within the `docker-compose.yml`:

* Start the docker compose environment: `docker compose up --build -d`.
* Test by navigating in your browser to:
  * [http://localhost:8009/admin/] (log in as superuser:superuser if that's how you configured it above)
  * [http://localhost:8009/api/shape/]

If you want to see the application logs as currently setup, just use: `docker compose logs app`.

### Browser Testing with the Regular App

I suggest creating some Shape objects in the database first.  Use the Admin console as described above
or use cURL as described below.

Then navigate to: `http://localhost:8009/shapes/`.


#### API Testing with cURL

Nothing prevents us from calling the application directly with cURL, Postman, or any other client. Here's
an example:

* First, find the available paths with: `docker compose exec app python manage.py show_urls`

* Then make and view your shape with these commands. These are saved in the database:
  ```
  curl --location 'http://localhost:8009/api/shape/' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Basic c3VwZXJ1c2VyOnN1cGVydXNlcg==' \
    --data '{"name": "pyramid", "face_count": 5, "is_sharp": true}'
  ```
* Then see it with: `curl --location 'http://localhost:8009/api/shape/'`
* And delete it with: `curl --location --request DELETE 'http://localhost:8009/api/shape/{shape-id}/'`

### Miscellaneous

#### Code Quality

Here's a few nice code quality things to run:
```
black .
pylint shapes user_app widget_project
isort .
```

or just: `pre-commit run --all-files`

#### Commit Hooks

Turn on commit hooks with: `make precommit`.  Then all the code quality stuff should run on every commit.

Only the __unit tests__ (i.e., not the functional tests) currently run with make precommit because there is
currently no expectation that the docker compose environment is running.
