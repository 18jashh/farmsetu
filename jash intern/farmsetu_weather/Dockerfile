# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (if needed for future expansion)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency manifest first for layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Expose port
EXPOSE 8000

# Collect static (no-op now, but good practice); run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
