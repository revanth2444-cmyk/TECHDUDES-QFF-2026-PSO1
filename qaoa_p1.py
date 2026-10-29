from pathlib import Path
import csv
import json
import numpy as np

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.circuit import ParameterVector
from qiskit_algorithms.optimizers import COBYLA

import qff_phase2 as qff


# ------------------------------------------------------------
# Official PS-O1 instance and reproducibility settings
# ------------------------------------------------------------
with open("instances.json", encoding="utf-8") as f:
    instance = json.load(f)["PS-O1"]

N = instance["num_vertices"]
EDGES = [tuple(edge) for edge in instance["weighted_edges"]]
C_STAR = 22
SHOTS = 4096
SEEDS = [0, 1, 2, 3, 4]
MAXITER = 100

with open("instances.json", encoding="utf-8") as f:
    official_instances = json.load(f)

processor_b_data = official_instances["processors"]["B"]
processor_b = {
    "name": "Processor B",
    "num_qubits": processor_b_data["num_qubits"],
    "edges": [tuple(edge) for edge in processor_b_data["edges"]],
    "basis_gates": official_instances["processors"]["D_limits"]["basis_gates"],
}


# ------------------------------------------------------------
# Max-Cut objective: expected cut weight for a bitstring
# ------------------------------------------------------------
def cut_weight(bits):
    return sum(w for u, v, w in EDGES if bits[u] != bits[v])


def expected_cut_from_state(state):
    probabilities = np.abs(state.data) ** 2
    expected = 0.0
    for index, probability in enumerate(probabilities):
        bits = tuple((index >> i) & 1 for i in range(N))
        expected += probability * cut_weight(bits)
    return float(expected)


# ------------------------------------------------------------
# QAOA p=1 circuit
# Cost unitary: exp(-i gamma C), up to a global phase.
# Mixer unitary: exp(-i beta sum_i X_i).
# ------------------------------------------------------------
def make_qaoa(gamma_value, beta_value):
    qc = QuantumCircuit(N)
    qc.h(range(N))

    gamma = float(gamma_value)
    beta = float(beta_value)

    for u, v, w in EDGES:
        qc.rzz(-gamma * w, u, v)

    qc.rx(2.0 * beta, range(N))
    return qc


# ------------------------------------------------------------
# Exact classical cross-check: all 2^6 assignments
# ------------------------------------------------------------
all_cuts = []
for index in range(2**N):
    bits = tuple((index >> i) & 1 for i in range(N))
    all_cuts.append((cut_weight(bits), bits))

exact_best = max(value for value, _ in all_cuts)
optimal_bits = [bits for value, bits in all_cuts if value == exact_best]

assert exact_best == C_STAR, (
    f"Expected optimum {C_STAR}, got {exact_best}"
)

print(f"PS-O1 vertices={N}, edges={len(EDGES)}")
print(f"Exact optimum C*={exact_best}")
print("Optimal bitstrings (x0,...,x5):", optimal_bits)
print(f"Optimizer=COBYLA, maxiter={MAXITER}, shots={SHOTS}")


# ------------------------------------------------------------
# Five seeded optimizer starts, ideal statevector objective
# ------------------------------------------------------------
runs = []

for seed in SEEDS:
    rng = np.random.default_rng(seed)
    initial = rng.uniform(0.0, np.pi, size=2)
    evaluations = 0

    def objective(theta):
        nonlocal_placeholder = None
        gamma, beta = theta
        state = Statevector.from_instruction(make_qaoa(gamma, beta))
        return -expected_cut_from_state(state)

    optimizer = COBYLA(maxiter=MAXITER, tol=1e-5)
    result = optimizer.minimize(
        fun=objective,
        x0=initial,
    )

    gamma_best, beta_best = result.x
    state = Statevector.from_instruction(
        make_qaoa(gamma_best, beta_best)
    )
    ideal_expectation = expected_cut_from_state(state)

    print(
        f"seed={seed} initial={np.round(initial, 6).tolist()} "
        f"gamma={gamma_best:.6f} beta={beta_best:.6f} "
        f"ideal_expected_cut={ideal_expectation:.6f} "
        f"approx_ratio={ideal_expectation / C_STAR:.6f} "
        f"optimizer_evals={result.nfev}"
    )

    runs.append({
        "seed": seed,
        "initial_gamma": float(initial[0]),
        "initial_beta": float(initial[1]),
        "gamma": float(gamma_best),
        "beta": float(beta_best),
        "ideal_expected_cut": ideal_expectation,
        "approx_ratio": ideal_expectation / C_STAR,
        "optimizer_evals": int(result.nfev),
        "success": None,
    })


# ------------------------------------------------------------
# Select best of five starts; evaluate with official transpilation
# and 4096 ideal shots on Processor B.
# ------------------------------------------------------------
best = max(runs, key=lambda row: row["ideal_expected_cut"])
best_circuit = make_qaoa(best["gamma"], best["beta"])
measured = QuantumCircuit(N)
measured.compose(best_circuit, inplace=True)
measured.measure_all()

transpiled = qff.transpile_for(measured, processor_b)
sim = qff.simulator(noisy=False, processor=processor_b)
counts = sim.run(
    transpiled,
    shots=SHOTS,
    seed_simulator=42,
).result().get_counts()

shot_cuts = []
optimal_shots = 0

for key, count in counts.items():
    bits = qff.counts_to_x(key)
    value = cut_weight(bits)
    shot_cuts.extend([value] * count)
    if tuple(bits) in optimal_bits:
        optimal_shots += count

mean_cut = float(np.mean(shot_cuts))
std_cut = float(np.std(shot_cuts, ddof=1))
best_sampled_cut = max(shot_cuts)
p_opt = optimal_shots / SHOTS

print("\n--- Processor B ideal shot evaluation ---")
print("Best optimization seed:", best["seed"])
print("Mean sampled cut:", round(mean_cut, 6))
print("Sample standard deviation:", round(std_cut, 6))
print("Best sampled cut:", best_sampled_cut)
print("Approximation ratio:", round(mean_cut / C_STAR, 6))
print("P_opt:", round(p_opt, 6))
print("Circuit metrics:", qff.circuit_metrics(measured, processor_b))

Path("results").mkdir(exist_ok=True)
with open("results/qaoa_p1_initializations.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(runs[0].keys()))
    writer.writeheader()
    writer.writerows(runs)

with open("results/qaoa_p1_processor_b_ideal.json", "w", encoding="utf-8") as f:
    json.dump({
        "processor": "Processor B",
        "noisy": False,
        "shots": SHOTS,
        "seed_simulator": 42,
        "exact_optimum": C_STAR,
        "best_initialization_seed": best["seed"],
        "gamma": best["gamma"],
        "beta": best["beta"],
        "mean_cut": mean_cut,
        "sample_std_cut": std_cut,
        "best_sampled_cut": best_sampled_cut,
        "approx_ratio": mean_cut / C_STAR,
        "p_opt": p_opt,
        "optimal_bitstrings": [list(bits) for bits in optimal_bits],
        "circuit_metrics": qff.circuit_metrics(measured, processor_b),
    }, f, indent=2)

print("\nSaved initial results under results/")
