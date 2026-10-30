import json
from pathlib import Path
from itertools import product

from qiskit.primitives import StatevectorSampler
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms.utils import algorithm_globals
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.quantum_info import Statevector

SEED = 42
N = 6
OUT = Path("results")

edges = [
    (0, 1, 2), (0, 2, 4), (0, 5, 1),
    (1, 2, 3), (1, 3, 5), (1, 4, 2),
    (2, 3, 1), (2, 5, 4), (3, 4, 3),
    (4, 5, 5),
]

# Find every optimal bitstring by exhaustive enumeration.
scores = {}
for bits in product([0, 1], repeat=N):
    scores["".join(map(str, bits))] = sum(
        w for u, v, w in edges if bits[u] != bits[v]
    )

best_value = max(scores.values())
optimal_strings = [bits for bits, value in scores.items() if value == best_value]

# Rebuild the same Max-Cut QUBO as benchmark_ab.py.
problem = QuadraticProgram("o1_reproducible_example_probability")
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
result = solver.solve(problem)

# Evaluate the optimized QAOA ansatz as an exact statevector.
optimal_point = result.min_eigen_solver_result.optimal_point
bound_circuit = qaoa.ansatz.assign_parameters(optimal_point)
bound_circuit = bound_circuit.remove_final_measurements(inplace=False)
state = Statevector.from_instruction(bound_circuit)
probabilities = state.probabilities()

# Qiskit statevector indices use little-endian qubit ordering:
# index bits are reversed relative to the x0, x1, ... variable string.
optimal_probability = 0.0
individual = {}
for bits in optimal_strings:
    index = int(bits[::-1], 2)
    p = float(probabilities[index])
    individual[bits] = p
    optimal_probability += p

report = {
    "instance_name": "O1_REPRODUCIBLE_EXAMPLE_NOT_OFFICIAL",
    "official_benchmark": False,
    "seed": SEED,
    "qaoa_reps": 1,
    "optimizer": "COBYLA",
    "optimizer_maxiter": 60,
    "exact_max_cut_value": best_value,
    "number_of_optimal_bitstrings": len(optimal_strings),
    "optimal_bitstrings_x0_to_x5": optimal_strings,
    "qaoa_objective_value": float(result.fval),
    "optimal_bitstring_probability": optimal_probability,
    "optimal_bitstring_probability_percent": 100.0 * optimal_probability,
    "individual_optimal_bitstring_probabilities": individual,
    "probability_method": "Exact optimized statevector; noiseless simulation",
    "limitations": [
        "Local example graph, not an official organizer-provided benchmark.",
        "No hardware noise or shot sampling included.",
        "This is ideal statevector probability, not hardware-measured success probability."
    ]
}

path = OUT / "o1_optimal_probability.json"
path.write_text(json.dumps(report, indent=2), encoding="utf-8")

print("Exact Max-Cut optimum:", best_value)
print("Number of optimal bitstrings:", len(optimal_strings))
print("QAOA objective:", result.fval)
print(f"Probability of any optimal bitstring: {optimal_probability:.8f} ({100*optimal_probability:.4f}%)")
print("Individual optimal probabilities:")
for bits, p in individual.items():
    print(f"  {bits}: {p:.8f}")
print("Saved:", path)
