# Встановлення базового образу
FROM python:3.9-slim

# Встановлення залежностей
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копіювання коду додатку
COPY . /app

# Встановлення робочого каталогу
WORKDIR /app

# Запуск додатку
CMD ["python", "flask_app.py"]
