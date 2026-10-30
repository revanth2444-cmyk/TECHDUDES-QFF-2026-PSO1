import json
import platform
from itertools import product
from pathlib import Path
from collections import Counter

import qiskit
from qiskit import transpile
from qiskit.primitives import StatevectorSampler
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms.utils import algorithm_globals
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer

SEED = 42
N = 6
OUT = Path("results")
OUT.mkdir(exist_ok=True)

# Reproducible example graph, not an organizer-specified official graph.
edges = [
    (0, 1, 2), (0, 2, 4), (0, 5, 1),
    (1, 2, 3), (1, 3, 5), (1, 4, 2),
    (2, 3, 1), (2, 5, 4), (3, 4, 3),
    (4, 5, 5),
]

graph = {
    "instance_name": "O1_REPRODUCIBLE_EXAMPLE_NOT_OFFICIAL",
    "official_benchmark": False,
    "seed": SEED,
    "nodes": list(range(N)),
    "edges": [{"u": u, "v": v, "weight": w} for u, v, w in edges],
    "note": "Locally chosen reproducible example; not an organizer-provided fixed graph."
}
(OUT / "o1_reproducible_graph.json").write_text(
    json.dumps(graph, indent=2), encoding="utf-8"
)

# Exact classical Max-Cut.
best_cut = -1
best_bits = None
for bits in product([0, 1], repeat=N):
    value = sum(w for u, v, w in edges if bits[u] != bits[v])
    if value > best_cut:
        best_cut, best_bits = value, bits

# Build the Max-Cut QUBO.
problem = QuadraticProgram("o1_reproducible_example")
for i in range(N):
    problem.binary_var(name=f"x{i}")

linear = {f"x{i}": 0 for i in range(N)}
quadratic = {}
for u, v, w in edges:
    linear[f"x{u}"] += w
    linear[f"x{v}"] += w
    quadratic[(f"x{u}", f"x{v}")] = -2 * w
problem.maximize(linear=linear, quadratic=quadratic)

algorithm_globals.random_seed = SEED
qaoa = QAOA(
    sampler=StatevectorSampler(seed=SEED),
    optimizer=COBYLA(maxiter=60),
    reps=1,
)
solver = MinimumEigenOptimizer(qaoa)
qaoa_result = solver.solve(problem)
circuit = qaoa.ansatz.decompose(reps=2)

rows = []
for filename, label in [
    ("processors/processor_A.json", "Processor A"),
    ("processors/processor_B.json", "Processor B"),
]:
    config = json.loads(Path(filename).read_text(encoding="utf-8-sig"))
    row = {
        "processor": label,
        "configuration_name": config["processor_name"],
        "configuration_status": config["configuration_status"],
        "official": config["official"],
        "physical_qubits": config["num_qubits"],
        "logical_qubits": circuit.num_qubits,
        "full_six_qubit_circuit_supported": config["num_qubits"] >= circuit.num_qubits,
        "compiled_depth": None,
        "two_qubit_gate_count": None,
        "two_qubit_gate_breakdown": None,
        "explicit_swap_count": None,
        "note": None,
    }

    if config["num_qubits"] < circuit.num_qubits:
        row["note"] = "Cannot map the full six-qubit circuit: processor has fewer than six qubits."
    else:
        compiled = transpile(
            circuit,
            basis_gates=config["basis_gates"],
            coupling_map=config["coupling_map"],
            optimization_level=config["optimization_level"],
            seed_transpiler=config["transpiler_seed"],
        )
        counts = Counter(
            item.operation.name for item in compiled.data
            if item.operation.num_qubits == 2
        )
        row.update({
            "compiled_depth": compiled.depth(),
            "two_qubit_gate_count": sum(counts.values()),
            "two_qubit_gate_breakdown": dict(counts),
            "explicit_swap_count": compiled.count_ops().get("swap", 0),
            "note": "Compiled with the documented topology and assumed basis gates; noise not simulated.",
        })
    rows.append(row)

report = {
    "instance_name": graph["instance_name"],
    "official_benchmark": False,
    "seed": SEED,
    "edges": graph["edges"],
    "exact_max_cut_value": best_cut,
    "one_exact_optimal_partition": list(best_bits),
    "qaoa_reps": 1,
    "optimizer": "COBYLA",
    "optimizer_maxiter": 60,
    "qaoa_objective_value": float(qaoa_result.fval),
    "qaoa_approximation_ratio": (
        float(qaoa_result.fval) / best_cut if best_cut else None
    ),
    "logical_qubits": circuit.num_qubits,
    "logical_depth": circuit.depth(),
    "processors": rows,
    "python_version": platform.python_version(),
    "qiskit_version": qiskit.__version__,
    "limitations": [
        "Graph is a reproducible local example, not an organizer-specified graph.",
        "Processor configurations are PDF-derived and pending approval.",
        "Basis gates are development assumptions; noise is not simulated.",
        "Processor A cannot run the full six-qubit circuit."
    ]
}
(OUT / "o1_ab_benchmark.json").write_text(
    json.dumps(report, indent=2), encoding="utf-8"
)

print("\n=== SIX-NODE MAX-CUT BENCHMARK ===")
print("Exact classical optimum:", best_cut)
print("One optimal partition:", best_bits)
print("QAOA objective:", qaoa_result.fval)
print("QAOA approximation ratio:", report["qaoa_approximation_ratio"])
print("\n=== PROCESSOR COMPARISON ===")
for row in rows:
    print(f"\n{row['processor']} ({row['physical_qubits']} qubits)")
    print("Full circuit supported:", row["full_six_qubit_circuit_supported"])
    print("Compiled depth:", row["compiled_depth"])
    print("Two-qubit gates:", row["two_qubit_gate_count"])
    print("Explicit SWAPs:", row["explicit_swap_count"])
    print("Note:", row["note"])

print("\nSaved:", OUT / "o1_reproducible_graph.json")
print("Saved:", OUT / "o1_ab_benchmark.json")
