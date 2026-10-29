# TECHDUDES — QFF 2026 PS-O1

## Project Overview

This project investigates the weighted Max-Cut problem using the Quantum Approximate Optimization Algorithm (QAOA) at depth \(p=1\).

The problem contains six vertices and nine weighted edges. The total edge weight is 27, and exhaustive enumeration gives an exact maximum-cut value of 22.

## Processor D

Processor D has nine qubits and twelve couplings. Its topology is connected and has a maximum degree of four, satisfying the challenge's maximum-degree limit. It supports the six logical qubits required by PS-O1.

**Basis gates:** `rz`, `sx`, `x`, `cx`

**Noise parameters:**
- One-qubit error probability: 0.001
- Two-qubit error probability: 0.005
- Readout error probability: 0.01

The final configuration is `processors/processor_D.json`.

## Main Results

| Processor | Condition | Mean cut | Approximation ratio | Best cut | Best-cut ratio | Optimal-cut probability |
|---|---|---:|---:|---:|---:|---:|
| B | Ideal | 15.6606 | 0.7118 | 22 | 1.0000 | 0.0730 |
| B | Noisy | 15.4326 | 0.7015 | 22 | 1.0000 | 0.0698 |
| D | Ideal | 15.5720 | 0.7078 | 22 | 1.0000 | 0.0679 |
| D | Noisy | 15.3633 | 0.6983 | 22 | 1.0000 | 0.0671 |

Processor A is not executable for this problem because it has five physical qubits, while the circuit requires six logical qubits.

These results are from simulations, not measurements on physical quantum hardware.

## Repository Contents

- `qff_phase2.py` — Challenge helper and validation functions
- `data/instance.json` — Problem instance
- `processors/` — Processor configurations
- `qaoa_p1.py` — QAOA optimization and Processor B evaluation
- `evaluate_processor_d.py` — Processor D evaluation
- `run_bell_experiments.py` — Bell experiments
- `baseline_comparison.py` — Random baseline and exact enumeration
- `results/tables/results.csv` — Combined processor results
- `results/tables/bell.csv` — Bell-test results
- `results/tables/initialization_summary.csv` — Initialization summary
- `report.md` — Technical report
- `main.ipynb` — Notebook for processor validation and reviewing saved results

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/revanth2444-cmyk/TECHDUDES-QFF-2026-PSO1.git
cd TECHDUDES-QFF-2026-PSO1
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Open the notebook

Open `main.ipynb` in Jupyter Notebook or upload it to Google Colab. Run the cells from top to bottom.

The notebook validates the processor configuration and reviews saved experiment results. To reproduce the QAOA experiments, run the relevant experiment scripts separately.

## Team

**TECHDUDES**

## AI Use Disclosure

AI assistance was used for development guidance, debugging support, experimental workflow organization, and preparation and editing of project documentation. The team reviewed the implementation, configuration files, and reported results against the project execution outputs. The team remains responsible for the submitted code, experiments, interpretation, and final report.
