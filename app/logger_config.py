import sys
print("Python version:", sys.version)

import logging
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Spårningskonfiguration
trace_provider = TracerProvider()
span_processor = BatchSpanProcessor(OTLPSpanExporter())
trace_provider.add_span_processor(span_processor)

# Loggkonfiguration
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)
