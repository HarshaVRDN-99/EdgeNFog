# ADR-003: Use SQLite for Local Detection Storage

## Status

Accepted

## Context

The Edge Node requires persistent local storage for received detection records and generated analytics.

## Decision

Store detection data in a SQLite database.

## Alternatives Considered

* CSV files
* JSON files
* PostgreSQL
* SQLite

## Consequences

### Positive

* Lightweight deployment
* No external database server required
* Easy backup and portability
* Suitable for edge environments

### Negative

* Limited support for high-concurrency workloads

---
