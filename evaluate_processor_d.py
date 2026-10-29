import json
from pathlib import Path
import numpy as np
from qiskit import QuantumCircuit
import qff_phase2 as qff

SHOTS = 4096
SEED = 42
C_STAR = 22

with open("instances.json", encoding="utf-8") as f:
    data = json.load(f)

instance = data["PS-O1"]
n = instance["num_vertices"]
edges = [tuple(e) for e in instance["weighted_edges"]]

with open("processors/processor_D.json", encoding="utf-8") as f:
    processor = json.load(f)

errors = qff.validate_processor_d(processor, n)
if errors:
    raise SystemExit("Processor D validation failed:\n- " + "\n- ".join(errors))

with open("results/qaoa_p1_processor_b_ideal.json", encoding="utf-8") as f:
    reference = json.load(f)

gamma = reference["gamma"]
beta = reference["beta"]
optimal_bits = {tuple(bits) for bits in reference["optimal_bitstrings"]}

qc = QuantumCircuit(n)
qc.h(range(n))
for u, v, w in edges:
    qc.rzz(-gamma * w, u, v)
qc.rx(2.0 * beta, range(n))
qc.measure_all()

def cut_weight(bits):
    return sum(w for u, v, w in edges if bits[u] != bits[v])

results = []
for noisy in (False, True):
    transpiled = qff.transpile_for(qc, processor)
    simulator = qff.simulator(noisy=noisy, processor=processor)
    counts = simulator.run(
        transpiled, shots=SHOTS, seed_simulator=SEED
    ).result().get_counts()

    total = 0
    cut_sum = 0.0
    cut_sq_sum = 0.0
    best_cut = 0
    optimal_count = 0

    for key, count in counts.items():
        bits = tuple(qff.counts_to_x(key))
        cut = cut_weight(bits)
        total += count
        cut_sum += cut * count
        cut_sq_sum += cut * cut * count
        best_cut = max(best_cut, cut)
        if bits in optimal_bits:
            optimal_count += count

    mean_cut = cut_sum / total
    variance = (cut_sq_sum - total * mean_cut**2) / (total - 1)
    metrics = qff.circuit_metrics(qc, processor)

    row = {
        "processor": "Processor D",
        "noisy": noisy,
        "noise_model": "official" if noisy else "none",
        "shots": total,
        "seed_simulator": SEED,
        "exact_optimum": C_STAR,
        "best_initialization_seed": reference["best_initialization_seed"],
        "gamma": gamma,
        "beta": beta,
        "mean_cut": mean_cut,
        "sample_std_cut": float(max(0.0, variance) ** 0.5),
        "best_sampled_cut": best_cut,
        "approx_ratio": mean_cut / C_STAR,
        "r_best": best_cut / C_STAR,
        "p_opt": optimal_count / total,
        "circuit_metrics": metrics,
    }
    results.append(row)
    print("\n" + ("NOISY" if noisy else "IDEAL") + " Processor D")
    print(json.dumps(row, indent=2))

Path("results").mkdir(exist_ok=True)
out = Path("results/qaoa_p1_processor_d.json")
out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
print(f"\nSaved results to {out}")
