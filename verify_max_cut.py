from itertools import product
import json
from pathlib import Path

instance = json.loads(
    Path("data/instance.json").read_text(encoding="utf-8")
)
edges = instance["PS-O1"]["weighted_edges"]
n = instance["PS-O1"]["num_vertices"]

def cut_value(bits):
    return sum(
        weight for u, v, weight in edges
        if bits[u] != bits[v]
    )

all_cuts = [
    (cut_value(bits), bits)
    for bits in product([0, 1], repeat=n)
]
best = max(value for value, bits in all_cuts)
optimal = [bits for value, bits in all_cuts if value == best]

print("Assignments checked:", len(all_cuts))
print("Exact maximum cut:", best)
print("Optimal assignments:", optimal)

assert len(all_cuts) == 64
assert best == 22
assert len(optimal) == 2
print("Verification passed.")
