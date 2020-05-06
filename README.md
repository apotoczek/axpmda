# Mood API

a Django REST API for tracking mood

**develop** branch for latest codebase and features

**master** branch for future production release

Use the **develop** branch to run locally: localhost:8000/mood/v1/

See additional README updates on **develop**


## Setup

Clone repo to local and checkout **develop** branch

Create Postgres DB

```
RDS_DB_NAME=axpmda
RDS_USERNAME=postgres
RDS_PASSWORD=
RDS_HOSTNAME=localhost
RDS_PORT=5432
```

Setup virtual environment

```
$ mkvirtualenv -p ~/.pyenv/versions/3.6.0/bin/python axpmda
```

... and env

```
export RDS_DB_NAME=axpmda
export RDS_USERNAME=postgres
export RDS_PASSWORD=
export RDS_HOSTNAME=localhost
export RDS_PORT=5432
export DJANGO_SETTINGS_MODULE=moodapi_project.settings
export DJANGO_SECRET_KEY="generate your own secret key here"

```

Clone repo into dir like ~/git/axpmda, checkout **develop** branch and activate virtual enviornment

`
adx5000@~/git/axpmda (develop)$ workon axpmda
`
`(axpmda) adx5000@~/git/axpmda (develop)$ pip install -r dev-requirements.txt`

Migrate

`(axpmda) adx5000@~/git/axpmda (develop)$ ./manage.py migrate`

Create superuser

`(axpmda) adx5000@~/git/axpmda (develop)$ ./manage.py createsuperuser`

Run server and verify superuser

`(axpmda) adx5000@~/git/axpmda (develop)$ ./manage.py runserver`

Go to http://127.0.0.1:8000/ to load default Django home page, then go to http://127.0.0.1:8000/admin/ and login as the superuser

## API Functionality

http://127.0.0.1:8000/mood/v1/

Setup new users via Django admin superuser

Users can login/logout via Login link on /mood/v1/