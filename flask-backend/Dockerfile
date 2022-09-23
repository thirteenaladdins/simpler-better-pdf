# syntax=docker/dockerfile:1
FROM python:3.9-alpine
WORKDIR /app /code
RUN apk update
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["gunicorn"  , "-b", "0.0.0.0:8080", "wsgi:app"]