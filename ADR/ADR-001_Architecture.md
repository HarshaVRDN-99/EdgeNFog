# ADR-001: Adopt a Multi-Layer Edge–Fog–Cloud Architecture

## Context

The asbestos sheet counting system requires distributed processing across multiple computational layers. The drone generates detections in real time, while additional analytics and aggregation are required at higher levels of the system.

## Implementation

* Far Edge (Drone)
* Edge Node (Local Processing Server)
* Fog Node (Regional Aggregation Server)
* Cloud Node (Centralized Storage and Analytics)

## Alternatives Considered

* Fully cloud-based architecture
* Drone-to-cloud communication
* Two-tier Edge–Cloud architecture

## Consequences

### Positive

* Reduced latency
* Lower bandwidth consumption
* Improved scalability
* Better fault tolerance

### Negative

* Increased system complexity
* More deployment and maintenance effort

---

