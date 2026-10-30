# Experiment Notes

## Current status
- Classical exact Max-Cut baseline runs on a toy graph.
- QAOA simulation runs on a separate toy triangle graph.
- QAOA result matched the exact optimum in the recorded run.
- Current circuit compilation uses an illustrative three-qubit line.

## Limitations
- These are development tests, not official hackathon benchmark results.
- The illustrative line is not a verified Processor A or Processor B topology.
- No conclusion about which official processor performs better can be drawn yet.
- Replace toy inputs and configuration with organizer-provided definitions before reporting official comparisons.

## Reproducibility
- Python environment: project virtual environment (.venv).
- Qiskit and simulator package versions should be recorded from the active environment.
- Run `python main.py` for the classical toy baseline.
- Run `python qaoa_demo.py` for the QAOA toy demonstration.
