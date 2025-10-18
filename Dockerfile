# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY weather.py .

# Set environment variable (can be overridden at runtime)
ENV APPID=""

# Run the application
CMD ["python", "weather.py"]