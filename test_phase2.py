#!/usr/bin/env python3
"""
Phase 2 Test: Send multiple spans with different names and durations to test filtering.

Expected results:
- 'filterme' span (3s duration) should be filtered out by name
- 'slowme' span (1.5 min duration) should be filtered out by duration
- 'seeme' span (1s duration) should pass through and be visible
"""

import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Configure resource
resource = Resource.create({"service.name": "phase2-test"})

# Setup Tracing
trace_provider = TracerProvider(resource=resource)
otlp_trace_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4318/v1/traces",
)
trace_provider.add_span_processor(BatchSpanProcessor(otlp_trace_exporter))
trace.set_tracer_provider(trace_provider)


def main():
    print("Phase 2 Test: Sending spans with different names and durations...")
    print("\nExpected results after filtering:")
    print("  ✓ 'seeme' span (1s) - SHOULD BE VISIBLE")
    print("  ✗ 'filterme' span (3s) - SHOULD BE FILTERED OUT (by name)")
    print("  ✗ 'slowme' span (90s) - SHOULD BE FILTERED OUT (by duration > 1 min)")
    print()

    tracer = trace.get_tracer(__name__)

    # Send 'filterme' span - 3 seconds duration
    print("Sending 'filterme' span (3s duration)...")
    with tracer.start_as_current_span("filterme") as span:
        span.set_attribute("test.phase", "2")
        span.set_attribute("test.type", "name-filter")
        span.set_attribute("expected.filtered", "true")
        time.sleep(3)
    print("✓ 'filterme' span sent")

    # Send 'seeme' span - 1 second duration
    print("Sending 'seeme' span (1s duration)...")
    with tracer.start_as_current_span("seeme") as span:
        span.set_attribute("test.phase", "2")
        span.set_attribute("test.type", "pass-through")
        span.set_attribute("expected.filtered", "false")
        time.sleep(1)
    print("✓ 'seeme' span sent")

    # Send 'slowme' span - 90 seconds (1.5 minutes) duration
    print("Sending 'slowme' span (90s / 1.5 min duration)...")
    with tracer.start_as_current_span("slowme") as span:
        span.set_attribute("test.phase", "2")
        span.set_attribute("test.type", "duration-filter")
        span.set_attribute("expected.filtered", "true")
        time.sleep(90)
    print("✓ 'slowme' span sent")

    # Give time for data to be exported
    print("\nWaiting for data to be exported...")
    time.sleep(3)

    # Shutdown provider to flush remaining data
    trace_provider.shutdown()

    print("\n✅ Phase 2 test complete!")
    print("\nCheck the collector output above:")
    print("  - You should see ONLY the 'seeme' span")
    print("  - 'filterme' and 'slowme' spans should NOT appear")


if __name__ == "__main__":
    main()
