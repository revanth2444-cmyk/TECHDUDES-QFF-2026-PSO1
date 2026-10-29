# TECHDUDES — QFF 2026 PS-O1

## Project overview

This project investigates weighted Max-Cut using the Quantum Approximate Optimization Algorithm (QAOA) at depth p = 1.

The problem contains six vertices and nine weighted edges. The total edge weight is 27, and exhaustive enumeration gives an exact maximum-cut value of 22.

## Processor D

Processor D has nine qubits and twelve couplings. Its topology is connected and has maximum degree three. It supports the six logical qubits required by PS-O1.

Basis gates: rz, sx, x, cx.

Noise parameters:
- One-qubit error probability: 0.001
- Two-qubit error probability: 0.005
- Readout error probability: 0.01

The final configuration is processors/processor_D.json.

## Main results

| Processor | Condition | Mean cut | Approximation ratio | Optimal-cut probability |
|---|---|---:|---:|---:|
| B | Ideal | 15.6606 | 0.7118 | 0.0730 |
| B | Noisy | 15.4326 | 0.7015 | 0.0698 |
| D | Ideal | 15.5720 | 0.7078 | 0.0679 |
| D | Noisy | 15.3633 | 0.6983 | 0.0671 |

Processor A is not executable for this problem because it has five physical qubits but the circuit requires six logical qubits.

These are simulation results, not measurements from physical quantum hardware.

## Repository contents

- qff_phase2.py — challenge helper and validation functions
- data/instance.json — problem instance
- processors/ — processor configurations
- qaoa_p1.py — QAOA optimization and Processor B evaluation
- evaluate_processor_d.py — Processor D evaluation
- run_bell_experiments.py — Bell experiments
- baseline_comparison.py — random baseline and exact enumeration
- results/tables/results.csv — combined processor results
- results/tables/bell.csv — Bell-test results
- results/tables/initialization_summary.csv — initialization summary
- report.md — technical report

## Environment setup

Create and activate the virtual environment, then install dependencies:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

## Team

TECHDUDES

## AI-use disclosure

AI assistance was used for development guidance, debugging support, experimental workflow organization, and preparation and editing of project documentation. The team reviewed the implementation, configuration files, and reported results against the project execution outputs. The team remains responsible for the submitted code, experiments, interpretation, and final report.
