# backend/docker/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY ../../requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ../../backend ./backend

ARG ENV=prod
ENV PYTHONPATH=/app/backend \
    FLASK_APP=backend/app.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000

# Install Flask dev dependencies if ENV=dev
RUN if [ "$ENV" = "dev" ]; then pip install flask[async]; fi

# Command will be overridden in docker-compose
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "backend.app:app"]
