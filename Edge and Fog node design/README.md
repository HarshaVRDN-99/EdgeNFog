# Edge–Fog Computing Architecture for Drone Image Processing

## Overview

This project implements a distributed **Edge–Fog Computing Architecture** for real-time drone image acquisition, preprocessing, transmission, storage, and analytics.

The system is designed to reduce network load, improve processing latency, and demonstrate how computational tasks can be distributed across Edge and Fog layers in an IoT environment.

The project is organized into independent sprints. Since every sprint builds upon the previous sprint with a fully functional code base, a student can join at any point in the development track and begin implementation immediately without needing to complete all prior work from scratch.

---

## Objectives

* Capture images from a drone camera in real time.
* Perform preprocessing at the Far Edge layer.
* Transfer both raw and processed images to the Edge layer.
* Generate and store image metadata.
* Monitor image quality and transmission performance.
* Visualize system metrics through a dashboard.

---

# Sprint 1 — Edge Pipeline

## Goal

Build the complete data ingestion and preprocessing pipeline at the Edge node.

## Tasks

* Receive images from drone
* Validate incoming data
* Store temporary images
* Preprocess images

  * Grayscale conversion
  * Noise reduction
  * Edge detection
* Package raw image, processed image, and metadata
* Forward data to Fog node

## Deliverables

* Working image receiver
* Preprocessing module
* Edge-to-Fog communication

---

# Sprint 2 — Edge Analytics

## Goal

Generate operational insights directly at the Edge.

## Tasks

* Brightness analysis
* Blur detection
* Processing latency measurement
* Transmission latency measurement
* Data size analysis
* Metadata generation

## Deliverables

* Analytics engine
* Metadata JSON generator
* Edge performance reports

## Output Metrics

* Brightness
* Blur score
* Processing time
* Transmission time
* Raw image size
* Processed image size

---

# Sprint 3 — Fog Pipeline

## Goal

Build the Fog-side ingestion and storage infrastructure.

## Tasks

* Receive data from Edge
* Store raw images
* Store processed images
* Validate incoming metadata
* Database integration
* Data archival

## Deliverables

* Fog receiver service
* Image storage system
* SQLite database

---

# Sprint 4 — Fog Analytics

## Goal

Perform higher-level analytics using aggregated Edge data.

## Tasks

* Aggregate metadata
* Compute trends
* Generate system statistics
* Storage monitoring
* Throughput analysis
* Historical analysis

## Deliverables

* Analytics engine
* Trend reports
* Dashboard-ready data

## Output Metrics

* Images processed per hour
* Average blur score
* Average brightness
* Storage utilization
* Processing trends

---

# Sprint 5 — Fog ML Model

## Goal

Deploy machine learning inference at the Fog layer.

## Tasks

* Dataset preparation
* Feature engineering
* Model training
* Model evaluation
* Inference service deployment

## Possible Models

* Image quality classification
* Blur prediction
* Brightness anomaly detection
* Scene classification

## Deliverables

* Trained model
* Inference API
* Evaluation report

---

# Sprint 6 — Fog Dashboard & Visualization

## Goal

Create a centralized monitoring interface.

## Tasks

* Database connectivity
* KPI visualization
* Trend charts
* ML predictions display
* System health monitoring
* Storage monitoring

## Deliverables

* Streamlit dashboard
* Analytics visualizations
* ML monitoring panel

## Dashboard Sections

* Edge metrics
* Fog metrics
* Image analytics
* ML predictions
* Storage analytics
* System health
