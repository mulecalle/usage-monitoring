# Mock Services

This directory contains mock implementations of external services used by the application.

## Purpose

The mock services in this folder are intended for:
- Development and testing without external dependencies
- Providing a reference for the expected data structures
- Allowing local development without access to production services

## Important Note

⚠️ **These are mock implementations only!**

The production application should:
- NOT use these mock implementations
- Connect to the actual external services
- Handle proper authentication and error cases
- Implement proper retry and circuit breaker patterns

## Available Mocks

### Pool Service (`server.py`)
- Endpoint: `GET /pools`
- Port: 3000
- Simulates the external pools service
- Uses static data from `pools.json5`

## Usage

Run the make mock-server command to start the mock services.