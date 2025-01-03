FROM python:3.11-slim

# Install dependencies
WORKDIR /app
COPY app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application
COPY app /app

# Run FastAPI
CMD ["python", "main.py"]
