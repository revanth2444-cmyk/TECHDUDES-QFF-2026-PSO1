# QFF 2026 Phase 1 — O1 Max-Cut starter

**Status:** beginner starter project. The included graph is a **TOY TEST INSTANCE**, not the official QFF benchmark.

## What this version does
- Loads a weighted graph from JSON.
- Computes the cut value of a partition.
- Finds the exact maximum cut by exhaustive search (suitable only for small graphs).
- Writes a result JSON to `results/toy_result.json`.

## Setup (VS Code terminal)
Create and activate a virtual environment:

Windows PowerShell:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```bash
python -m pip install -r requirements.txt
```

Run:
```bash
python main.py
```

This first version uses only the Python standard library, so no packages are required yet.

## Project layout
```text
data/
  toy_graph.json             # safe test data; not official
  official/README.md         # keep official files separate
src/
  problem.py                 # classical Max-Cut verification
results/                     # generated outputs
main.py
requirements.txt
```

## Important benchmark rules
- Do not replace the toy graph with guessed values and call them official.
- Put organizer-provided graph/weights in `data/official/` only after confirming they are official.
- Store official Processor A/B definitions in `processors/` when received.
- Use identical problem inputs and controlled settings for A/B comparisons.
- Report measured results, and clearly label simulations or toy runs.

## Next milestones
1. Confirm the official O1 weighted graph and scoring definition.
2. Obtain the official Processor A/B configuration files.
3. Implement the QAOA circuit and classical optimizer.
4. Transpile the same logical experiment against A and B; record cut quality, depth, two-qubit gates and SWAP overhead.
5. Add plots, a reproducible notebook, and evidence-based analysis.
