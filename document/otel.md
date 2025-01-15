För att konfigurera OpenTelemetry (OTel) i en container att skicka data till OpenSearch med HTTPS, behöver du göra följande steg:

1. Skapa och konfigurera OpenSearch
   • Se till att OpenSearch är konfigurerad för att använda HTTPS. Detta innebär att du behöver:
   • Generera och installera TLS-certifikat för OpenSearch.
   • Aktivera HTTPS i OpenSearch-konfigurationen (opensearch.yml).
   • Öppna port 9200 (eller annan valfri port för HTTPS).

2. Installera och konfigurera OpenTelemetry Collector

OpenTelemetry Collector fungerar som en mellanhand för att samla in, bearbeta och skicka data.

a. Skapa en konfigurationsfil för OTel Collector

Exempel på en otel-collector-config.yml för att skicka data till OpenSearch via HTTPS:

receivers:
otlp:
protocols:
grpc:
http:

exporters:
otlphttp:
endpoint: "https://opensearch-host:9200"
headers:
Authorization: "Bearer YOUR_API_TOKEN" # Om autentisering behövs
tls:
insecure: false
ca_file: "/path/to/ca.crt" # Certifikat för att verifiera OpenSearch

service:
pipelines:
traces:
receivers: [otlp]
exporters: [otlphttp]
metrics:
receivers: [otlp]
exporters: [otlphttp]

b. Certifikat

Om OpenSearch använder ett självsignerat certifikat behöver du tillhandahålla dess CA-certifikat till OTel Collector.

3. Bygg eller använd en container för OTel Collector

Om du använder en egen container, skapa en Dockerfile:

FROM otel/opentelemetry-collector:latest
COPY otel-collector-config.yml /etc/otel-collector-config.yml
CMD ["--config", "/etc/otel-collector-config.yml"]

Bygg och kör containern:

docker build -t otel-collector .
docker run -d --name otel-collector otel-collector

4. Konfigurera din applikation att skicka data till OTel Collector
   • Lägg till OpenTelemetry SDK i din applikation.
   • Konfigurera exporter för att skicka data till OTel Collector (t.ex. via OTLP).

Exempel på inställning i Python:

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

trace.set_tracer_provider(TracerProvider())
span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4318"))
trace.get_tracer_provider().add_span_processor(span_processor)

5. Verifiera datainsamling och visualisering
   • Verifiera att data skickas korrekt till OpenSearch genom att:
   • Kontrollera OpenSearch-index med:

curl -k -u username:password "https://opensearch-host:9200/\_cat/indices?v"

    •	Inspektera loggarna i OTel Collector och din applikation.

    •	För visualisering kan du använda OpenSearch Dashboards (tidigare Kibana).

Behöver du hjälp med någon specifik del?
