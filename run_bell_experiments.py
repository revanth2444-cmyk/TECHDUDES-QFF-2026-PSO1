import csv
import json
from pathlib import Path
import qff_phase2 as qff

with open("processors/processor_D.json", encoding="utf-8") as f:
    processor = json.load(f)

errors = qff.validate_processor_d(processor, 6)
if errors:
    raise SystemExit("Processor D validation failed: " + "; ".join(errors))

# Adjacent pair and a graph-diameter pair, determined from the topology.
cm = qff.coupling_map_from_edges(
    processor["edges"], processor["num_qubits"]
)
adjacent_pair = tuple(processor["edges"][0])

distances = [
    (cm.distance(a, b), (a, b))
    for a in range(processor["num_qubits"])
    for b in range(a + 1, processor["num_qubits"])
]
max_distance = max(d for d, pair in distances)
farthest_pair = next(pair for d, pair in distances if d == max_distance)

print("Adjacent pair:", adjacent_pair, "distance:", cm.distance(*adjacent_pair))
print("Farthest pair:", farthest_pair, "distance:", max_distance)

rows = []
for pair_name, pair in [
    ("adjacent", adjacent_pair),
    ("farthest", farthest_pair),
]:
    for noisy in (False, True):
        result = qff.bell_experiment(
            processor=processor,
            physical_pair=pair,
            noisy=noisy,
            shots=4096,
        )
        result["pair_type"] = pair_name
        rows.append(result)
        print(json.dumps(result, indent=2))

out_dir = Path("results")
out_dir.mkdir(exist_ok=True)
json_path = out_dir / "processor_d_bell_results.json"
csv_path = out_dir / "processor_d_bell_results.csv"

json_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

columns = [
    "processor", "pair_type", "pair", "pair_distance", "noisy", "shots",
    "XX", "XX_se", "YY", "YY_se", "ZZ", "ZZ_se",
    "fidelity", "fidelity_se", "cx",
]
with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)

print("\nSaved:", json_path)
print("Saved:", csv_path)
