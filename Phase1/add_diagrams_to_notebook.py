import json
from pathlib import Path

path = Path("main.ipynb")
nb = json.loads(path.read_text(encoding="utf-8"))

marker = "Graph and processor topology diagrams"
exists = any(
    cell["cell_type"] == "markdown"
    and marker in "".join(cell.get("source", []))
    for cell in nb["cells"]
)

if exists:
    print("Diagram cell already exists; notebook unchanged.")
else:
    source = """## Graph and processor topology diagrams

The six-node weighted graph is a local reproducible example, not an official benchmark.

### Weighted Max-Cut graph
![Weighted Max-Cut graph](results/weighted_maxcut_graph.svg)

### Processor A coupling map
PDF-derived topology; pending organizer approval.

![Processor A coupling map](results/processor_A_coupling.svg)

### Processor B coupling map
PDF-derived topology; pending organizer approval.

![Processor B coupling map](results/processor_B_coupling.svg)

These are connectivity diagrams, not hardware-noise or performance visualizations.
"""
    nb["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True)
    })
    path.write_text(json.dumps(nb, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Added diagram cell to main.ipynb")

check = json.loads(path.read_text(encoding="utf-8"))
print("Notebook cells:", len(check["cells"]))
print("Notebook JSON: valid")
