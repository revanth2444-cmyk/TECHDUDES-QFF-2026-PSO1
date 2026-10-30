
import json
import platform
from collections import Counter
from itertools import product
from pathlib import Path

import qiskit
import scipy
from qiskit import transpile
from qiskit.primitives import StatevectorSampler
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms.utils import algorithm_globals
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer


# --------------------------------------------------
# 1. Three-node weighted toy Max-Cut graph
# This is NOT an official QFF benchmark instance.
# --------------------------------------------------

edges = [
    (0, 1, 2),
    (1, 2, 3),
    (0, 2, 1),
]

num_nodes = 3

problem = QuadraticProgram("toy_max_cut")

for node in range(num_nodes):
    problem.binary_var(name=f"x{node}")

linear = {f"x{i}": 0 for i in range(num_nodes)}
quadratic = {}

for a, b, weight in edges:
    linear[f"x{a}"] += weight
    linear[f"x{b}"] += weight
    quadratic[(f"x{a}", f"x{b}")] = -2 * weight

problem.maximize(
    linear=linear,
    quadratic=quadratic,
)

print(
    "Objective at all-zero assignment:",
    problem.objective.evaluate([0, 0, 0]),
)
print(
    "Objective at a good cut:",
    problem.objective.evaluate([0, 1, 0]),
)


# --------------------------------------------------
# 2. Configure and run QAOA
# --------------------------------------------------

SEED = 42

algorithm_globals.random_seed = SEED
sampler = StatevectorSampler(seed=SEED)

qaoa = QAOA(
    sampler=sampler,
    optimizer=COBYLA(maxiter=50),
    reps=1,
)

solver = MinimumEigenOptimizer(qaoa)
result = solver.solve(problem)

# Inspect the logical QAOA circuit before compilation.
circuit = qaoa.ansatz.decompose(reps=2)


# --------------------------------------------------
# 3. Load the illustrative toy processor configuration
# --------------------------------------------------

config_path = Path("processors/toy_line.json")
results_dir = Path("results")
results_dir.mkdir(parents=True, exist_ok=True)

with config_path.open("r", encoding="utf-8-sig") as f:
    processor_config = json.load(f)

# Prevent the development configuration from being
# accidentally treated as an official processor.
if processor_config.get("official") is not False:
    raise ValueError(
        "This demo requires toy_line.json to have official=false."
    )

if circuit.num_qubits > processor_config["num_qubits"]:
    raise ValueError(
        "The circuit requires more qubits than the toy processor provides."
    )

line_coupling = processor_config["coupling_map"]
basis_gates = processor_config["basis_gates"]
optimization_level = processor_config["optimization_level"]
transpiler_seed = processor_config["transpiler_seed"]


# --------------------------------------------------
# 4. Transpile the circuit for the toy topology
# --------------------------------------------------

compiled = transpile(
    circuit,
    basis_gates=basis_gates,
    coupling_map=line_coupling,
    optimization_level=optimization_level,
    seed_transpiler=transpiler_seed,
)

print("\nCompiled circuit for illustrative toy hardware:")
print(compiled.draw(output="text"))

print("\nCompiled depth:", compiled.depth())
print("Explicit SWAP count:", compiled.count_ops().get("swap", 0))
print("CX count:", compiled.count_ops().get("cx", 0))
print("Compiled operation counts:", compiled.count_ops())

two_qubit_ops = Counter(
    instruction.operation.name
    for instruction in compiled.data
    if instruction.operation.num_qubits == 2
)

two_qubit_gate_count = sum(two_qubit_ops.values())

print("Two-qubit gate breakdown:", dict(two_qubit_ops))
print("Compiled two-qubit gate count:", two_qubit_gate_count)


# --------------------------------------------------
# 5. Display the logical circuit and QAOA result
# --------------------------------------------------

print("\nGate counts before transpilation:")
print(circuit.count_ops())

print("\nLogical QAOA circuit:")
print(circuit.draw(output="text"))

print("\nLogical qubit count:", circuit.num_qubits)
print("Logical circuit depth:", circuit.depth())
print("Total logical circuit operations:", circuit.size())

print("\nQAOA run completed!")
print("Best bitstring:", result.x)
print("Objective value:", result.fval)
print("Variables:", result.variables_dict)


# --------------------------------------------------
# 6. Independently calculate the exact Max-Cut optimum
# --------------------------------------------------

best_value = float("-inf")
best_partition = None

for bits in product([0, 1], repeat=num_nodes):
    cut = sum(
        weight
        for a, b, weight in edges
        if bits[a] != bits[b]
    )

    if cut > best_value:
        best_value = cut
        best_partition = bits

matches_optimum = abs(float(result.fval) - best_value) < 1e-9

print("\nClassical verification:")
print("Exact maximum cut value:", best_value)
print("One optimal partition:", best_partition)
print("QAOA result matches optimum:", matches_optimum)


# --------------------------------------------------
# 7. Save reproducibility metadata
# --------------------------------------------------

metadata = {
    "instance_name": "TOY_TRIANGLE_NOT_OFFICIAL",
    "official_benchmark": False,
    "seed": SEED,
    "qaoa_reps": 1,
    "optimizer": "COBYLA",
    "optimizer_maxiter": 50,
    "sampler": "StatevectorSampler",
    "logical_qubits": circuit.num_qubits,
    "logical_depth": circuit.depth(),
    "compiled_depth": compiled.depth(),
    "compiled_two_qubit_gate_count": two_qubit_gate_count,
    "compiled_two_qubit_gate_breakdown": dict(two_qubit_ops),
    "explicit_swap_count": compiled.count_ops().get("swap", 0),
    "qaoa_objective_value": float(result.fval),
    "exact_max_cut_value": float(best_value),
    "qaoa_matches_optimum": bool(matches_optimum),
    "python_version": platform.python_version(),
    "qiskit_version": qiskit.__version__,
    "scipy_version": scipy.__version__,
    "transpiler_seed": transpiler_seed,
    "optimization_level": optimization_level,
    "hardware_topology": processor_config["processor_name"],
    "processor_official": processor_config["official"],
    "processor_num_qubits": processor_config["num_qubits"],
    "basis_gates": basis_gates,
    "coupling_map": line_coupling,
}

metadata = {
    key: (value.item() if hasattr(value, "item") else value)
    for key, value in metadata.items()
}

output_path = results_dir / "qaoa_toy_result.json"

with output_path.open("w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print("\nSaved reproducibility metadata:")
print(output_path)