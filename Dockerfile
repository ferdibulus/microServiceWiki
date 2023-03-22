FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
RUN pip install Flask \
    && pip install APScheduler \
    && pip install -U flask-cors \
    && pip install wikipedia
