import csv
import json
from pathlib import Path

result_files = [
    Path("results/qaoa_p1_processor_b_ideal.json"),
    Path("results/qaoa_p1_processor_b_noisy.json"),
    Path("results/qaoa_p1_processor_d.json"),
]

columns = [
    "processor", "noisy", "noise_model", "shots", "seed_simulator",
    "exact_optimum", "best_initialization_seed", "gamma", "beta",
    "mean_cut", "sample_std_cut", "best_sampled_cut",
    "approx_ratio", "r_best", "p_opt", "executable",
    "logical_qubits", "physical_qubits", "logical_cx", "cx",
    "one_q_gates", "depth", "two_q_depth", "swaps", "cx_overhead",
    "notes",
]

metric_columns = [
    "executable", "logical_qubits", "physical_qubits", "logical_cx",
    "cx", "one_q_gates", "depth", "two_q_depth", "swaps", "cx_overhead",
]

rows = []

for path in result_files:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = [data]

    for result in data:
        row = {key: result.get(key, "") for key in columns}
        metrics = result.get("circuit_metrics", {})
        for key in metric_columns:
            row[key] = metrics.get(key, "")
        row["notes"] = ""
        rows.append(row)

# Processor A has 5 physical qubits, but PS-O1 needs 6 logical qubits.
# Record its non-executable status without inventing benchmark measurements.
for noisy in (False, True):
    rows.append({
        "processor": "Processor A",
        "noisy": noisy,
        "noise_model": "official" if noisy else "none",
        "shots": 4096,
        "seed_simulator": 42,
        "exact_optimum": 22,
        "executable": False,
        "logical_qubits": 6,
        "physical_qubits": 5,
        "notes": "Not executable: 5 physical qubits available, 6 logical qubits required."
    })

# Put rows in a predictable A/B/D order, ideal before noisy.
rows.sort(key=lambda r: (
    {"Processor A": 0, "Processor B": 1, "Processor D": 2}.get(r["processor"], 99),
    bool(r["noisy"])
))

output = Path("results/tables/results.csv")
output.parent.mkdir(parents=True, exist_ok=True)

with output.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)

print(f"Created {output} with {len(rows)} rows.")
