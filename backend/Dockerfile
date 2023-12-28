# syntax=docker/dockerfile:1
FROM python:3.7.6-buster
WORKDIR /app /code
# RUN apt-get dist-upgrade -y
RUN apt-get update
# RUN apt-get install -y gcc musl-dev linux-headers-$(uname -r)
RUN apt-get install -y gcc musl-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["gunicorn"  , "-b", "0.0.0.0:8080", "wsgi:app"]