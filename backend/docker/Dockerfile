# backend/docker/Dockerfile
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy Python dependencies first (for caching)
COPY ../../requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend source code into container
COPY ../../backend ./backend

# Set PYTHONPATH so imports work
ENV PYTHONPATH=/app/backend

# Expose the port inside the container
EXPOSE 5000

# Run the Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
