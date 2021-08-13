# Mood API

a Django REST API for tracking mood

**develop** branch for latest codebase and features

**master** branch for future production release

Use the **develop** branch to run locally: localhost:8000/mood/v1/

See additional README updates on **develop**

## Contents

- [About](https://github.com/apotoczek/axpmda#about)
- [Setup](https://github.com/apotoczek/axpmda#setup)
- [API Functionality](https://github.com/apotoczek/axpmda#api-functionality)
- [Docker](https://github.com/apotoczek/axpmda#docker)
- [Production](https://github.com/apotoczek/axpmda#production)

## About

REST application with a '/mood' endpoint, which when POSTed to persists the submitted mood value.

Users login via Django's authentication UI.

The '/mood' endpoint allows logged-in users to GET values submitted by the logged-in user.

The ‘/mood’ endpoint returns, among other things, the length of their current "streak".  A user is on a “streak” if that user has submitted at least 1 mood rating for each consecutive day of that streak.  For example, if on March 1st, March 2nd, March 3rd, and March 5th the user entered mood ratings, a 3-day streak will apply to the March 3rd rating and the streak will reset to a 1-day streak for the March 5th rating.  The user's streak's percentile is a comparison to other users.

## Setup

Setup for virtualenvwrapper (see Docker section separately), uses axpmda_settings.py

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
export DJANGO_SETTINGS_MODULE=moodapi_project.axpmda_settings
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

Go to 127.0.0.1:8000/ to load default Django home page (before adding any urlpatterns, afterwards no home page exists, only API endpoints), then go to 127.0.0.1:8000/admin/ and login as the superuser

## API Functionality

Setup new users via Django admin superuser

Users can login/logout via Login link on /mood/v1/ or directly at /api-auth/login/?next=/mood/v1/

**Endpoints**

* GET Mood Report: 127.0.0.1:8000/mood/v1/
    * shows your user's info, streaks and list of moods

```
"user_id": your user's id
"username": your user's username
"moods_count": count of moods for your user
"newest_streak": newest streak of mood entries on consecutive days
"longest_streak": longest overall streak in your mood entries history
"streak_percentile": displayed in decimal representation...
    your longest streak = your_longest
    avg of longest streaks from all other users = avg_longest
	(your_longest - avg_longest) / avg_longest 
	e.g.: (7 - 3.8) / 3.8 = 0.84, which makes your percentile 84%
	negative decimal indicates below 0%
    return value can be easily changed to True/False for >=50%
        but the decimal representation may be more useful
```

* GET Mood List: 127.0.0.1:8000/mood/v1/moods/
    * shows your user's list of moods
  
* POST Mood: 127.0.0.1:8000/mood/v1/moods/
    * submit new mood for your user, e.g.:
 
```
Media type: application/json

Content:
{
    "mood": "<CharField max_length=50 required>",
    "details": "<TextField optional>"
}
```

* GET Mood Detail: 127.0.0.1:8000/mood/v1/moods/(mood id int:pk)/
    * shows single mood using mood id, if it exists for your user

Note: you must be logged-in and can only view, add or modify moods associated with your user

## Docker

Python 3.8, Django 2.2.12, psycopg2-binary 2.8.4, djangorestframework 3.11.0, postgres 10

Database for Docker in settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', 'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432
    }
}
```

```
adx5000@~/git/axpmda (develop)$ docker-compose up -d --build
adx5000@~/git/axpmda (develop)$ docker-compose exec web python manage.py migrate
adx5000@~/git/axpmda (develop)$ docker-compose exec web python manage.py createsuperuser
```

```
adx5000@~/git/axpmda (develop)$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
c9270a8d39b1        axpmda_web          "python /axpmda/mana…"   7 minutes ago       Up 7 minutes        0.0.0.0:8000->8000/tcp   axpmda_web_1
17c8a416abe5        postgres:10         "docker-entrypoint.s…"   7 minutes ago       Up 7 minutes        5432/tcp                 axpmda_db_1
```

Endpoints should be available from Docker at 127.0.0.1:8000/[endpoints]

Note: create a superuser, and additional users in /admin/, then add Moods via /admin/

## Production

Possible TODOs for production deployment:

- segregate django settings into enviornments; **base** settings for all envs, **local** settings, **prod** settings (and any other envs desired)
- add env-specific logging / debug settings
- include a credentials file pulled from something like a private S3 bucket with env vars/creds for each enviornment
- setup CI/CD like Jenkins to trigger based on changes to **master** branch
- add CORS and whitelist correct domains
- for AWS, setup EB deployment
- refactor streak calculations into models or DRYer solutions
- add API endpoints for user registration/auth etc. (currently a superuser can add users)