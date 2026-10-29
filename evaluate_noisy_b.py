import json
from pathlib import Path
import numpy as np
from qiskit import QuantumCircuit
import qff_phase2 as qff

with open("instances.json", encoding="utf-8") as f:
    data = json.load(f)

instance = data["PS-O1"]
n = instance["num_vertices"]
edges = [tuple(e) for e in instance["weighted_edges"]]
c_star = 22
shots = 4096

processor_data = data["processors"]["B"]
processor_b = {
    "name": "Processor B",
    "num_qubits": processor_data["num_qubits"],
    "edges": [tuple(e) for e in processor_data["edges"]],
    "basis_gates": data["processors"]["D_limits"]["basis_gates"],
}

with open("results/qaoa_p1_processor_b_ideal.json", encoding="utf-8") as f:
    ideal = json.load(f)

gamma = ideal["gamma"]
beta = ideal["beta"]

qc = QuantumCircuit(n)
qc.h(range(n))
for u, v, w in edges:
    qc.rzz(-gamma * w, u, v)
qc.rx(2.0 * beta, range(n))
qc.measure_all()

transpiled = qff.transpile_for(qc, processor_b)
sim = qff.simulator(noisy=True, processor=processor_b)
counts = sim.run(transpiled, shots=shots, seed_simulator=42).result().get_counts()

def cut_weight(bits):
    return sum(w for u, v, w in edges if bits[u] != bits[v])

optimal_bits = {tuple(bits) for bits in ideal["optimal_bitstrings"]}
cut_samples = []
optimal_count = 0

for key, count in counts.items():
    bits = tuple(qff.counts_to_x(key))
    cut_samples.extend([cut_weight(bits)] * count)
    if bits in optimal_bits:
        optimal_count += count

mean_cut = float(np.mean(cut_samples))
std_cut = float(np.std(cut_samples, ddof=1))
best_cut = int(max(cut_samples))
p_opt = optimal_count / shots

result = {
    "processor": "Processor B",
    "noisy": True,
    "noise_model": "official",
    "shots": shots,
    "seed_simulator": 42,
    "exact_optimum": c_star,
    "best_initialization_seed": ideal["best_initialization_seed"],
    "gamma": gamma,
    "beta": beta,
    "mean_cut": mean_cut,
    "sample_std_cut": std_cut,
    "best_sampled_cut": best_cut,
    "approx_ratio": mean_cut / c_star,
    "p_opt": p_opt,
    "circuit_metrics": qff.circuit_metrics(qc, processor_b),
}

Path("results").mkdir(exist_ok=True)
out = Path("results/qaoa_p1_processor_b_noisy.json")
out.write_text(json.dumps(result, indent=2), encoding="utf-8")

print("Processor B — official noisy evaluation")
print(json.dumps(result, indent=2))
print(f"\nSaved: {out}")
