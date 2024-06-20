# Используем базовый образ Python
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app/news

COPY . /app/news
COPY ./requirements.txt /app/news/requirements.txt

RUN pip install --no-cache-dir -r /app/news/requirements.txt
