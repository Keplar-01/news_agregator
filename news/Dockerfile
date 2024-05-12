# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем переменную окружения PYTHONUNBUFFERED для предотвращения буферизации вывода
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию в /app
WORKDIR /app/news

# Копируем файлы проекта в контейнер
COPY . /app/news
COPY ./requirements.txt /app/news/requirements.txt

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r /app/news/requirements.txt

# Команда для запуска FastAPI приложения в контейнере
CMD ["uvicorn", "news:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]