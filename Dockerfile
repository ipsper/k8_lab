FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application
COPY app /app

# Set default environment variables for Uvicorn
ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8000

# Run FastAPI
CMD ["sh", "-c", "uvicorn main:app --host $UVICORN_HOST --port $UVICORN_PORT"]