FROM python:3.11-slim
FROM python:3.11-slim AS app

# Set working directory
WORKDIR /app

# Kopiera applikationsfiler
COPY . /app

# Copy requirements file and install dependencies
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt


# Lägg till OpenTelemetry Collector
FROM otel/opentelemetry-collector:latest AS otel
COPY otel-collector-config.yml /etc/otel-collector-config.yml

# Kombinera applikationen och OpenTelemetry Collector
FROM python:3.11-slim
WORKDIR /app

# Kopiera applikationsfiler
COPY --from=app /app /app

# Kopiera OpenTelemetry Collector-konfigurationen
COPY --from=otel /etc/otel-collector-config.yml /etc/otel-collector-config.yml

# Set default environment variables for Uvicorn
ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8000

# Exponera nödvändiga portar för OpenTelemetry
EXPOSE 4318 4317


# Run FastAPI
CMD ["sh", "-c", "otel-collector --config /etc/otel-collector-config.yml" & "sh", "-c", "uvicorn main:app --host $UVICORN_HOST --port $UVICORN_PORT"]