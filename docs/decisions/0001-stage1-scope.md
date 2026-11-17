# ADR 0001: Start with pulse-level compilation on a dummy Cluster

Date: 2026-11-17

Status: Accepted

## Context

The first exercise should expose the experiment-to-instrument compilation boundary without requiring a lab, qubit calibration, or a new control framework.

## Decision

Use the official Qblox scheduler and its dummy Cluster path with one QRM-RF module, one logical output, and two square pulses. Keep the experiment in a Python script and the wiring in JSON. Compile and inspect artifacts without starting sequencers or defining acquisitions. Use standard-library unittest for checks and pip/venv with exact dependency pins for Windows reproduction.

## Consequences

The learner can connect pulse timing, logical-to-physical mapping and generated Q1ASM. A pulse-level example does not require gate calibration or a transmon model. It also cannot establish qubit behavior, physical signal quality or real-time performance. The vendor stack has substantial transitive dependencies; this exercise adds no application framework. A custom scheduler, backend interface and fault model remain future exercises.
