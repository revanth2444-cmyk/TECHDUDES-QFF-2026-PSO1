import json
from pathlib import Path

files = [
    "results/o1_reproducible_graph.json",
    "processors/processor_A.json",
    "processors/processor_B.json",
]

for name in files:
    p = Path(name)
    print(f"\n--- {name} ---")
    if not p.exists():
        print("MISSING")
        continue
    data = json.loads(p.read_text(encoding="utf-8-sig"))
    print(json.dumps(data, indent=2))

try:
    import matplotlib
    print("\nmatplotlib:", matplotlib.__version__)
except ImportError:
    print("\nmatplotlib: NOT INSTALLED")
