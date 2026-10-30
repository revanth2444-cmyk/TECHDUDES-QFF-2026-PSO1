import json
from itertools import product
from collections import Counter
from pathlib import Path

from qiskit import transpile
from qiskit.primitives import StatevectorSampler
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms.utils import algorithm_globals
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer

SEED = 42
N = 5
# Same original example graph, restricted to vertices 0..4.
edges = [
    (0, 1, 2), (0, 2, 4),
    (1, 2, 3), (1, 3, 5), (1, 4, 2),
    (2, 3, 1), (3, 4, 3),
]

best = max(
    sum(w for u, v, w in edges if bits[u] != bits[v])
    for bits in product([0, 1], repeat=N)
)

problem = QuadraticProgram("common_five_node_subproblem")
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
    optimizer=COBYLA(maxiter=40),
    reps=1,
)
result = MinimumEigenOptimizer(qaoa).solve(problem)
circuit = qaoa.ansatz.decompose(reps=2)

rows = []
for filename, label in [
    ("processors/processor_A.json", "Processor A"),
    ("processors/processor_B.json", "Processor B"),
]:
    cfg = json.loads(Path(filename).read_text(encoding="utf-8-sig"))
    compiled = transpile(
        circuit,
        basis_gates=cfg["basis_gates"],
        coupling_map=cfg["coupling_map"],
        optimization_level=cfg["optimization_level"],
        seed_transpiler=cfg["transpiler_seed"],
    )
    counts = Counter(
        item.operation.name for item in compiled.data
        if item.operation.num_qubits == 2
    )
    rows.append({
        "processor": label,
        "physical_qubits": cfg["num_qubits"],
        "configuration_status": cfg["configuration_status"],
        "compiled_depth": compiled.depth(),
        "two_qubit_gate_count": sum(counts.values()),
        "two_qubit_gate_breakdown": dict(counts),
        "explicit_swap_count": compiled.count_ops().get("swap", 0),
        "note": "SWAPs may be decomposed into basis gates; explicit swap count alone does not measure routing overhead."
    })

report = {
    "instance_name": "FIVE_NODE_SUBPROBLEM_NOT_OFFICIAL",
    "official_benchmark": False,
    "edges": [{"u": u, "v": v, "weight": w} for u, v, w in edges],
    "exact_max_cut_value": best,
    "qaoa_objective_value": float(result.fval),
    "qaoa_approximation_ratio": float(result.fval) / best if best else None,
    "logical_qubits": circuit.num_qubits,
    "logical_depth": circuit.depth(),
    "processors": rows,
    "noise_simulated": False,
}
Path("results/common_subproblem_comparison.json").write_text(
    json.dumps(report, indent=2), encoding="utf-8"
)

print("\n=== COMMON FIVE-NODE SUBPROBLEM ===")
print("Exact optimum:", best)
print("QAOA objective:", result.fval)
print("Approximation ratio:", report["qaoa_approximation_ratio"])
for row in rows:
    print(f"\n{row['processor']}:")
    print("Compiled depth:", row["compiled_depth"])
    print("Two-qubit gates:", row["two_qubit_gate_count"])
    print("Two-qubit gate breakdown:", row["two_qubit_gate_breakdown"])
    print("Explicit SWAP count:", row["explicit_swap_count"])

print("\nSaved: results/common_subproblem_comparison.json")
