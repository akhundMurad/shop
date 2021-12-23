FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache jpeg-dev postgresql-libs && \
    apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    postgresql-dev \
    g++ \
    python3-dev \
    zlib-dev \
    libxml2-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    build-base

COPY src/ /app

WORKDIR /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt