# ADR-004: Use REST APIs for Inter-Node Communication

## Status

Accepted

## Context

The drone and Edge Node require a reliable communication mechanism for transmitting detection results and metadata.

## Decision

Use HTTP REST APIs with JSON payloads for communication between nodes.

## Alternatives Considered

* MQTT
* WebSockets
* gRPC

## Consequences

### Positive

* Easy implementation
* Human-readable data format
* Broad ecosystem support
* Simplified debugging and testing

### Negative

* Slightly higher overhead than MQTT or gRPC

---