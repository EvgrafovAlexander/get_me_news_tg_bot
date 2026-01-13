FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем timezone
ENV TZ=Europe/Moscow
ENV DEBIAN_FRONTEND=noninteractive

# Установка минимальных зависимостей для сборки пакетов Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        make \
        libc6-dev \
        libffi-dev \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Переменные окружения подтянутся из docker-compose
CMD ["python", "main.py"]
