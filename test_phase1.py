#!/usr/bin/env python3
"""
Phase 1 Test: Send a trace, log, and metric to the collector endpoint.
"""

import time
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
import logging

# Configure resource
resource = Resource.create({"service.name": "phase1-test"})

# Setup Tracing
trace_provider = TracerProvider(resource=resource)
otlp_trace_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4318/v1/traces",
)
trace_provider.add_span_processor(BatchSpanProcessor(otlp_trace_exporter))
trace.set_tracer_provider(trace_provider)

# Setup Metrics
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://localhost:4318/v1/metrics"),
    export_interval_millis=1000,
)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

# Setup Logging
logger_provider = LoggerProvider(resource=resource)
otlp_log_exporter = OTLPLogExporter(endpoint="http://localhost:4318/v1/logs")
logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_log_exporter))

# Attach OTLP handler to root logger
handler = LoggingHandler(logger_provider=logger_provider)
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)


def main():
    print("Phase 1 Test: Sending trace, log, and metric to collector...")

    # Send a trace
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("test-span") as span:
        span.set_attribute("test.phase", "1")
        span.set_attribute("test.type", "basic")
        print("✓ Trace sent")

    # Send a log
    logger = logging.getLogger(__name__)
    logger.info("This is a test log message from Phase 1", extra={"test.phase": "1"})
    print("✓ Log sent")

    # Send a metric
    meter = metrics.get_meter(__name__)
    counter = meter.create_counter(
        "test.counter",
        description="A test counter for Phase 1"
    )
    counter.add(1, {"test.phase": "1"})
    print("✓ Metric sent")

    # Give time for data to be exported
    print("\nWaiting for data to be exported...")
    time.sleep(3)

    # Shutdown providers to flush remaining data
    trace_provider.shutdown()
    meter_provider.shutdown()
    logger_provider.shutdown()

    print("\n✅ Phase 1 test complete!")
    print("Check the collector output above to verify trace, log, and metric were received.")


if __name__ == "__main__":
    main()
