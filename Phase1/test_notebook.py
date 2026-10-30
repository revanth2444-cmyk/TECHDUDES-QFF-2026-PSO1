import json
from pathlib import Path

nb = json.loads(Path("main.ipynb").read_text(encoding="utf-8"))
ns = {}

for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        try:
            exec(compile(source, f"notebook_cell_{i}", "exec"), ns)
        except Exception as e:
            print(f"FAILED cell {i}: {type(e).__name__}: {e}")
            raise

print("\nAll notebook code cells executed successfully.")
