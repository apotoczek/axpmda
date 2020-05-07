FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SECRET_KEY "aseifhowawhfqahwfoei2872528374alskjdfwalkhawlkhasa"

WORKDIR /axpmda

COPY Pipfile Pipfile.lock /axpmda/
RUN pip install pipenv && pipenv install --system

COPY . /axpmda/