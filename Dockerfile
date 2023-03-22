FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
WORKDIR /app
COPY . .
RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /app/static
RUN pip install Flask
RUN pip install -U flask-cors
RUN pip install wikipedia
