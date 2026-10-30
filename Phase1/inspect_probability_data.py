import json
from pathlib import Path

for name in [
    "results/o1_ab_benchmark.json",
    "results/common_subproblem_comparison.json",
]:
    p = Path(name)
    print(f"\n--- {name} ---")
    data = json.loads(p.read_text(encoding="utf-8-sig"))
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            print(f"{key}: {json.dumps(value)[:1200]}")
        else:
            print(f"{key}: {value}")

print("\n--- QAOA script files ---")
for name in ["benchmark_ab.py", "compare_common_subproblem.py"]:
    p = Path(name)
    print(f"{name}: {'exists' if p.exists() else 'missing'}")
