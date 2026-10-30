import json
from pathlib import Path

def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))

six = read_json("results/o1_ab_benchmark.json")
five = read_json("results/common_subproblem_comparison.json")
graph = read_json("results/o1_reproducible_graph.json")

def markdown_cell(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(keepends=True)
    }

def code_cell(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(keepends=True)
    }

cells = [
    markdown_cell("""# QFF 2026 Phase 1 — PS-O1 Max-Cut

**Status:** Reproducible development benchmark; not an official benchmark result.

This notebook documents the existing QAOA runs and the topology compilation comparison. Processor configurations and basis gates are PDF-derived assumptions pending organizer approval. No hardware noise is simulated.
"""),
    markdown_cell("""## 1. Six-node weighted graph

The graph is a locally chosen example. It must not be represented as an organizer-provided official instance.
"""),
    code_cell("""import json
from pathlib import Path
from itertools import product
from collections import Counter

graph = json.loads(Path("results/o1_reproducible_graph.json").read_text(encoding="utf-8"))
edges = [(e["u"], e["v"], e["weight"]) for e in graph["edges"]]
n = len(graph["nodes"])

print("Instance:", graph["instance_name"])
print("Official benchmark:", graph["official_benchmark"])
print("Nodes:", n)
print("Edges:")
for edge in edges:
    print(edge)
"""),
    markdown_cell("""## 2. Exact classical reference

Exhaustive search checks every binary partition for this small graph.
"""),
    code_cell("""def cut_value(bits, edges):
    return sum(w for u, v, w in edges if bits[u] != bits[v])

all_cuts = [
    (cut_value(bits, edges), bits)
    for bits in product([0, 1], repeat=n)
]
best_value = max(value for value, _ in all_cuts)
best_partitions = [bits for value, bits in all_cuts if value == best_value]

print("Exact Max-Cut:", best_value)
print("Example optimal partition:", best_partitions[0])
"""),
    markdown_cell("""## 3. Existing six-node QAOA and Processor B compilation results

The following values are loaded from the saved benchmark output, rather than rerunning the optimizer in this cell.
"""),
    code_cell("""six = json.loads(Path("results/o1_ab_benchmark.json").read_text(encoding="utf-8"))
print("QAOA objective:", six["qaoa_objective_value"])
print("Approximation ratio:", six["qaoa_approximation_ratio"])
print("Logical depth:", six["logical_depth"])
print("Exact classical optimum:", six["exact_max_cut_value"])
for p in six["processors"]:
    print("\\\\n", p["processor"])
    print("Physical qubits:", p["physical_qubits"])
    print("Compiled depth:", p["compiled_depth"])
    print("Two-qubit gates:", p["two_qubit_gate_count"])
    print("Explicit SWAPs:", p["explicit_swap_count"])
    print("Note:", p["note"])
"""),
    markdown_cell("""## 4. Common five-node Processor A/B comparison

Both topologies compile the same five-qubit logical circuit for this subproblem.
"""),
    code_cell("""five = json.loads(Path("results/common_subproblem_comparison.json").read_text(encoding="utf-8"))
print("Exact subproblem optimum:", five["exact_max_cut_value"])
print("QAOA objective:", five["qaoa_objective_value"])
print("Approximation ratio:", five["qaoa_approximation_ratio"])
for p in five["processors"]:
    print("\\\\n", p["processor"])
    print("Compiled depth:", p["compiled_depth"])
    print("Two-qubit gates:", p["two_qubit_gate_count"])
    print("Gate breakdown:", p["two_qubit_gate_breakdown"])
    print("Explicit SWAPs:", p["explicit_swap_count"])
"""),
    markdown_cell("""## 5. Interpretation and limitations

- In the saved five-node compilation, Processor B has depth 30 versus 34 for Processor A, and 23 CX gates versus 26.
- These are compilation metrics under the current topology and basis-gate assumptions, not hardware performance measurements.
- A zero explicit SWAP count does not prove there was no routing overhead.
- Processor A has five physical qubits, so it cannot host the full six-qubit circuit.
- The example graphs are not official challenge instances.
- Processor configurations and basis gates require confirmation against the final organizer kit.
- Noise was not simulated.
- The saved objective ratio is not the probability of measuring an optimal bitstring.
""")
]

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.13"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

Path("main.ipynb").write_text(
    json.dumps(notebook, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

# Validate notebook JSON and basic notebook structure.
check = json.loads(Path("main.ipynb").read_text(encoding="utf-8"))
assert check["nbformat"] == 4
assert len(check["cells"]) == len(cells)
assert all(c["cell_type"] in ("markdown", "code") for c in check["cells"])
print("Created and validated main.ipynb")
print("Cells:", len(check["cells"]))
