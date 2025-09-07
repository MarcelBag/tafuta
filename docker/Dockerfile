# Use lightweight Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (SQLite, build tools)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Flask port
EXPOSE 5000

# Default command (using Gunicorn in prod)
CMD ["sh", "-c", "if [ \"$FLASK_ENV\" = 'production' ]; then gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app; else python backend/app.py; fi"]
