FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /app/


ENV DJANGO_PORT=8000

EXPOSE ${DJANGO_PORT}

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:${DJANGO_PORT}"]
