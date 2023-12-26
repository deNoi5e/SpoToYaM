FROM python:3

# Создаем рабочую директорию в контейнере
WORKDIR /app

# Копируем все файлы программы в контейнер
COPY . /app

# Копируем файл зависимостей (например, requirements.txt) в контейнер
COPY requirements.txt /app/requirements.txt

# Установим venv
RUN pip install virtualenv

RUN virtualenv venv

RUN source venv/bin/activate

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Устанавливаем cron
RUN apt-get update && apt-get -y install cron

# Добавляем cron-задачу в файл cron
RUN echo "0 0 * * * python /app/SpoToYam.py" >> /etc/crontab # Запуск каждую минуту

# Запускаем cron в фоновом режиме
CMD ["cron", "-f"]