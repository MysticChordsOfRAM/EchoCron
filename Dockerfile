FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y \
    r-base \
    rsync \
    cron \
    libpq-dev \
    gcc \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY crontab /etc/cron.d/echocron

COPY . .

RUN chmod 0644 /etc/cron.d/echocron

RUN crontab /etc/cron.d/echocron

CMD ["cron", "-f"]
