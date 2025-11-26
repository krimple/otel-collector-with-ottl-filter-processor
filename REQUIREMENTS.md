# Requirements to implement the collector

## Phase 1

Test: write a test that sends a trace, log and metric to a collector endpoint on localhost. Let it fail at first.

1. Create a collector native build using the ocb tool. Make sure the collector starts and reflects telemetry to stdout.
2. Add a reciever for otlp/http on the standard port
3. Create a simple pipeline for traces, logs and metrics via a batch processor to a console exporter

Success criteria: Run the test and make sure the collector outputs the data.

## Phase 2

Test: Write a test that sends several trace spans to the collector - one with the name 'filterme' that takes 3 seconds, and another named 'seeme' which takes 1 second, and one with the duration of 1.5 minutes named 'slowme'. The test should pass when only the seeme trace shows up.

1. Add a filter processor to the collector with a sample that filters out a span based on the name of the span
Run the tests and verify the filterme span is not present.
2. Add a filter processor to the collector that samples out any span with a duration longer than 1 minute. Run the tests and verify that the 'slowme' span is no longer present.

Success criteria: only the showme span surives.

## Phase 3

Add an export to Honeycomb using OTLP/HTTP that sends the Honeycomb API key as the value of the X-Honeycomb-Team header.

Test: make sure that the content shows up in Honeycomb. We'll connect the Honeycomb MCP before you run the test.
