FROM ubuntu:16.04

# Language configuration
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev

ENV CELERY_BROKER_URL redis://redis:6379/
ENV CELERY_RESULT_BACKEND redis://redis:6379/

# copy source code
COPY . /app
WORKDIR /app

# install requirements
RUN pip3 install -r requirements.txt

WORKDIR /app/src

# migrate db
RUN python3 main.py migrate

# expose the app port
EXPOSE 5000

# run the app server
CMD gunicorn --bind 0.0.0.0:5000 --workers=10 api:app
