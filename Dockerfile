FROM python:3.9-alpine
WORKDIR /code
COPY . .
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install Flask \
    && pip install APScheduler \
    && pip install -U flask-cors \
    && apk del .build-deps
EXPOSE 5000
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]
