FROM python:3.9-alpine

WORKDIR /opt

RUN apk update && apk add \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    zlib-dev \
    jpeg-dev \
    tzdata \
    postgresql-dev \
    libpq

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh", "gunicorn", "Sibdev_test.wsgi:application", "--bind", "0.0.0.0:8000"]
