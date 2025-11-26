.PHONY: help install-ocb build run test clean

# Detect OS
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
	OS := darwin
	ARCH := arm64
else ifeq ($(UNAME_S),Linux)
	OS := linux
	ARCH := amd64
endif

OCB_VERSION := 0.114.0
OCB_URL := https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/cmd%2Fbuilder%2Fv$(OCB_VERSION)/ocb_$(OCB_VERSION)_$(OS)_$(ARCH)
COLLECTOR_BINARY := ./dist/otelcol-custom

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

install-ocb: ## Install OpenTelemetry Collector Builder
	@if [ ! -f ./ocb ]; then \
		echo "Downloading ocb $(OCB_VERSION) for $(OS)/$(ARCH)..."; \
		curl -L -o ocb $(OCB_URL); \
		chmod +x ocb; \
		echo "ocb installed successfully"; \
	else \
		echo "ocb already installed"; \
	fi

build: install-ocb ## Build the custom collector
	@echo "Building custom collector..."
	./ocb --config builder-config.yaml
	@echo "Build complete: $(COLLECTOR_BINARY)"

run: build ## Run the collector
	@echo "Starting collector..."
	$(COLLECTOR_BINARY) --config config.yaml

test: build ## Run tests
	@echo "Running Phase 1 tests..."
	@if [ ! -d venv ]; then \
		python3 -m venv venv; \
		. venv/bin/activate && pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http; \
	fi
	@. venv/bin/activate && python3 test_phase1.py

clean: ## Clean build artifacts
	@echo "Cleaning..."
	rm -rf dist
	rm -f ocb
	rm -rf venv
	@echo "Clean complete"
