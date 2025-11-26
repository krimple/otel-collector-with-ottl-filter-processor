# OpenTelemetry Collector with Filtering

A custom OpenTelemetry Collector implementation with filtering capabilities, built using the OpenTelemetry Collector Builder (ocb).

## Prerequisites

- **Go**: Version 1.21 or later (required for building the collector)
- **Python**: Version 3.9 or later (required for running tests)
- **Make**: Standard make utility
- **curl**: For downloading ocb

### Installing Go

**macOS:**
```bash
brew install go
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install golang-go
```

Verify installation:
```bash
go version
```

## Project Structure

```
.
├── builder-config.yaml      # OCB configuration (defines collector components)
├── config.yaml              # Collector runtime configuration
├── Makefile                 # Build automation
├── test_phase1.py           # Phase 1 test script
├── REQUIREMENTS.md          # Implementation phases and requirements
└── dist/                    # Build output (created after build)
    └── otelcol-custom       # Custom collector binary
```

## Building from Scratch

### Step 1: Install Dependencies

Make sure Go is installed and accessible:
```bash
go version
```

### Step 2: Build the Collector

The Makefile handles everything automatically:
```bash
make build
```

This command will:
1. Download the OpenTelemetry Collector Builder (ocb) for your platform
2. Use ocb to generate a custom collector with the components defined in `builder-config.yaml`
3. Compile the collector binary to `./dist/otelcol-custom`

**First build takes 30-60 seconds** as it downloads dependencies and compiles the collector.

### Step 3: Verify the Build

Check that the binary was created:
```bash
ls -lh ./dist/otelcol-custom
```

## Running the Collector

### Option 1: Using Make (Recommended)
```bash
make run
```

### Option 2: Direct Execution
```bash
./dist/otelcol-custom --config config.yaml
```

The collector will start and listen for OTLP/HTTP traffic on `localhost:4318`.

### What the Collector Does

Current configuration (Phase 1):
- **Receives**: OTLP/HTTP on port 4318 (standard port)
- **Processes**: Batches telemetry data
- **Exports**: Outputs to console (stdout) using debug exporter

## Testing

### Automated Test

Run the full test suite:
```bash
make test
```

This will:
1. Build the collector (if not already built)
2. Create a Python virtual environment
3. Install OpenTelemetry Python SDK
4. Run test script that sends trace, log, and metric data
5. Verify data is received and displayed

### Manual Testing

For debugging or development, run collector and test separately:

**Terminal 1 - Start the collector:**
```bash
./dist/otelcol-custom --config config.yaml
```

**Terminal 2 - Set up Python environment (first time only):**
```bash
python3 -m venv venv
source venv/bin/activate
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
```

**Terminal 2 - Run test:**
```bash
source venv/bin/activate
python3 test_phase1.py
```

You should see telemetry data output in Terminal 1.

## Cleanup

Remove all build artifacts:
```bash
make clean
```

This removes:
- `./dist/` directory (compiled collector)
- `./ocb` binary
- `./venv/` Python virtual environment

## Makefile Targets

- `make help` - Show available commands
- `make install-ocb` - Download and install ocb only
- `make build` - Build the custom collector
- `make run` - Build and run the collector
- `make test` - Run automated tests
- `make clean` - Remove all build artifacts

## Configuration Files

### builder-config.yaml

Defines which components to include in the custom collector:
- **Receivers**: otlpreceiver (OTLP protocol)
- **Processors**: batchprocessor, filterprocessor
- **Exporters**: debugexporter (console), otlphttpexporter

### config.yaml

Runtime configuration for the collector:
- Receiver endpoints and protocols
- Processor settings
- Exporter configurations
- Pipeline definitions (traces, metrics, logs)

## Troubleshooting

### Build Fails - Go Not Found

**Error:** `go: command not found` or similar

**Solution:** Install Go using the instructions in Prerequisites section.

### Build Fails - Permission Denied

**Error:** Permission denied when downloading or executing ocb

**Solution:**
```bash
chmod +x ocb
```

### Port Already in Use

**Error:** `bind: address already in use` on port 4318

**Solution:** Stop any other collector instances or change the port in `config.yaml`:
```yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: 0.0.0.0:4319  # Use different port
```

### Python Module Not Found

**Error:** `ModuleNotFoundError: No module named 'opentelemetry'`

**Solution:** Activate the virtual environment and install dependencies:
```bash
source venv/bin/activate
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
```

## Platform Support

This project is designed to work on:
- **macOS** (darwin/arm64 and darwin/amd64)
- **Linux** (linux/amd64)

The Makefile automatically detects your platform and downloads the appropriate ocb binary.

## Next Steps

See `REQUIREMENTS.md` for the phased implementation plan:
- **Phase 1** ✅ - Basic collector with OTLP receiver and console output
- **Phase 2** ✅ - Add filtering by span name and duration
- **Phase 3** - Export to Honeycomb
