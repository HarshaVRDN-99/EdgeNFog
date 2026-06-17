# ADR-002: Use FastAPI for Edge Node Services

## Status

Accepted

## Context

The Edge Node requires a backend service to receive detection data from the drone and provide analytics to downstream components.

## Decision

Use FastAPI as the backend framework for Edge Node services.

## Alternatives Considered

* Flask
* Django
* FastAPI

## Rationale

FastAPI provides high performance, automatic API documentation, built-in data validation, and native asynchronous support. It integrates well with Python-based analytics and machine learning workflows.

## Consequences

### Positive

* High performance
* Automatic API documentation
* Native async support
* Easy integration with Python ML tools

### Negative

* Smaller ecosystem compared to Django
