#!/usr/bin/env python3
"""
Phase 3 Test: Send spans that pass through filters to Honeycomb.

Expected results:
- Spans should be sent to Honeycomb via OTLP/HTTP
- Data should be visible in Honeycomb UI
- Filtered spans should NOT appear in Honeycomb
"""

import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Configure resource
resource = Resource.create({
    "service.name": "phase3-honeycomb-test",
    "test.phase": "3"
})

# Setup Tracing
trace_provider = TracerProvider(resource=resource)
otlp_trace_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4318/v1/traces",
)
trace_provider.add_span_processor(BatchSpanProcessor(otlp_trace_exporter))
trace.set_tracer_provider(trace_provider)


def main():
    print("Phase 3 Test: Sending spans to Honeycomb...")
    print("\nThese spans should appear in Honeycomb:")
    print("  ✓ 'process-order' span (short duration)")
    print("  ✓ 'validate-payment' span (short duration)")
    print("\nThese spans should be filtered out:")
    print("  ✗ 'filterme' span (filtered by name)")
    print("  ✗ 'slowme' span (filtered by duration > 60s)")
    print()

    tracer = trace.get_tracer(__name__)

    # Send a span that should pass through - 'process-order'
    print("Sending 'process-order' span...")
    with tracer.start_as_current_span("process-order") as span:
        span.set_attribute("test.phase", "3")
        span.set_attribute("test.destination", "honeycomb")
        span.set_attribute("order.id", "12345")
        span.set_attribute("order.amount", 99.99)
        time.sleep(0.5)
    print("✓ 'process-order' span sent")

    # Send another span that should pass through - 'validate-payment'
    print("Sending 'validate-payment' span...")
    with tracer.start_as_current_span("validate-payment") as span:
        span.set_attribute("test.phase", "3")
        span.set_attribute("test.destination", "honeycomb")
        span.set_attribute("payment.method", "credit-card")
        span.set_attribute("payment.success", True)
        time.sleep(0.3)
    print("✓ 'validate-payment' span sent")

    # Send a span that should be filtered out by name
    print("Sending 'filterme' span (should be filtered by name)...")
    with tracer.start_as_current_span("filterme") as span:
        span.set_attribute("test.phase", "3")
        span.set_attribute("test.destination", "honeycomb")
        span.set_attribute("expected.filtered", "true")
        span.set_attribute("filter.reason", "name")
        time.sleep(0.2)
    print("✓ 'filterme' span sent (but should be filtered)")

    # Send a span that should be filtered out by duration (> 60 seconds)
    print("Sending 'slowme' span (90s duration - should be filtered by duration)...")
    with tracer.start_as_current_span("slowme") as span:
        span.set_attribute("test.phase", "3")
        span.set_attribute("test.destination", "honeycomb")
        span.set_attribute("expected.filtered", "true")
        span.set_attribute("filter.reason", "duration")
        time.sleep(90)
    print("✓ 'slowme' span sent (but should be filtered)")

    # Give time for data to be exported
    print("\nWaiting for data to be exported...")
    time.sleep(3)

    # Shutdown provider to flush remaining data
    trace_provider.shutdown()

    print("\n✅ Phase 3 test complete!")
    print("\nNext steps:")
    print("  1. Check Honeycomb UI for the traces")
    print("  2. You should see 'process-order' and 'validate-payment' spans")
    print("  3. The 'filterme' span should NOT appear (filtered by name)")
    print("  4. Service name should be 'phase3-honeycomb-test'")


if __name__ == "__main__":
    main()
