- You are an expert in the OpenTelemetry Collector, in configuring it for linux and building a contrib instance
- You understand OpenTelemetry configuration and OTLP/HTTP protocols, and the how to use the filter processor to filter out spans we don't want.
- You use Makefiles to configure opentelemetry as well as the ocb tool and you prefer a native binary instance over running in docker

## How to Run the Collector

### Building
```bash
make build
```
This will:
- Download and install the OpenTelemetry Collector Builder (ocb) if not already present
- Build a custom collector binary at `./dist/otelcol-custom`

### Running
```bash
make run
```
This will build (if needed) and start the collector with the configuration in `config.yaml`.

The collector will:
- Listen for OTLP/HTTP traffic on `localhost:4318`
- Accept traces, metrics, and logs
- Output received telemetry to stdout using the debug exporter

### Testing
```bash
make test
```
This will:
- Build the collector
- Set up a Python virtual environment with OpenTelemetry SDK
- Run the test script to send sample trace, log, and metric data
- Verify the collector receives and outputs the data

### Manual Testing
To run the collector and test manually in separate terminals:

Terminal 1:
```bash
./dist/otelcol-custom --config config.yaml
```

Terminal 2:
```bash
source venv/bin/activate
python3 test_phase1.py
```

### Cleanup
```bash
make clean
```
Removes build artifacts, ocb binary, and Python virtual environment.
- the REQUIREMENTS.md file contains my current working requirements. We have completed phases 1 and 2