FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

RUN apk --update add bash nano git

ENV STATIC_URL /static

ENV STATIC_PATH /var/www/app/static


RUN pip install Flask \
    && pip install APScheduler \
    && pip install -U flask-cors \
    && pip install wikipedia
