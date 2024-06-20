
FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /app/agregator

COPY . /app/agregator
COPY ./requeriments.txt /app/agregator/requirements.txt

RUN pip install --no-cache-dir -r /app/agregator/requirements.txt

CMD ["python", "agregator.py"]