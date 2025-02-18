# Usage Monitoring

A service that monitors pool usage and categorizes them based on their utilization levels.

## Features

- Monitors pools usage through external service
- Categorizes pools into:
  - Critical (≤ 10% usage)
  - Low (≤ 30% usage)
- Scheduled checks every 6 hours

## Configuration

- External service endpoint: `http://localhost:3000/pools`
- Main service port: `8000`
- Usage check interval: Every 6 hours
- Usage thresholds:
  - Critical: ≤ 10%
  - Low: ≤ 30%

## API Endpoints

### GET /pools
Get current pools usage data, optionally filtered by category.

Query Parameters:
- `categories`: Optional list of categories to filter by (critical, low)

Examples:
```bash
# Get all pools
curl http://localhost:8000/pools

# Get only critical pools
curl http://localhost:8000/pools?categories=critical

# Get only low usage pools
curl http://localhost:8000/pools?categories=low
```

### GET /last_execution
Get the last calculated usage data without triggering a new check.

Example:
```bash
curl http://localhost:8000/last_execution
```

## Development

### Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
make dependencies
```

### Running Services

1. Start the mock service:
```bash
make mock-server
```

2. Start the main service:
```bash
make run
```

### Testing

Run the test suite:
```bash
make test
```