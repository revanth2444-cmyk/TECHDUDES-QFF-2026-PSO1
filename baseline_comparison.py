import itertools
import json
import numpy as np

with open("instances.json", encoding="utf-8") as f:
    instance = json.load(f)["PS-O1"]

n = instance["num_vertices"]
edges = instance["weighted_edges"]

def cut_weight(bits):
    return sum(w for u, v, w in edges if bits[u] != bits[v])

all_results = [
    (cut_weight(bits), bits)
    for bits in itertools.product([0, 1], repeat=n)
]

best_cut = max(cut for cut, _ in all_results)
optimal = [bits for cut, bits in all_results if cut == best_cut]

rng = np.random.default_rng(42)
samples = [tuple(rng.integers(0, 2, size=n)) for _ in range(4096)]
random_cuts = np.array([cut_weight(bits) for bits in samples])

print("=== Exact classical baseline ===")
print("Assignments evaluated:", len(all_results))
print("Exact optimum:", best_cut)
print("Optimal assignments:", optimal)

print("\n=== Uniform random baseline ===")
print("Shots:", len(random_cuts))
print("Seed: 42")
print("Mean cut:", round(float(random_cuts.mean()), 6))
print("Sample standard deviation:", round(float(random_cuts.std(ddof=1)), 6))
print("Best sampled cut:", int(random_cuts.max()))
print("Approximation ratio:", round(float(random_cuts.mean() / best_cut), 6))
print("P_opt:", round(float(np.mean(random_cuts == best_cut)), 6))
