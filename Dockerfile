FROM python:3.12-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем timezone
ENV TZ=Europe/Moscow

# Устанавливаем зависимости для сборки некоторых Python-библиотек
# (Alpine использует musl, поэтому некоторым пакетам нужны dev-библиотеки)
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Переменные окружения подтянутся из docker-compose
CMD ["python", "main.py"]
