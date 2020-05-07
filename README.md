# Mood API

a Django REST API for tracking mood

**develop** branch for latest codebase and features

**master** branch for future production release

Use the **develop** branch to run locally: localhost:8000/mood/v1/

See additional README updates on **develop**

## Contents

- [Setup](https://github.com/apotoczek/axpmda#setup)
- [API Functionality](https://github.com/apotoczek/axpmda#api-functionality)
- [Production](https://github.com/apotoczek/axpmda#production)


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