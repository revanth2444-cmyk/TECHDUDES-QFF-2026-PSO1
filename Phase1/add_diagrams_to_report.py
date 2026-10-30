from pathlib import Path

report_path = Path("reports/report.md")
report = report_path.read_text(encoding="utf-8")

marker = "## Graph and processor topology diagrams"

section = """
## Graph and processor topology diagrams

### Weighted Max-Cut graph

The graph below is a locally chosen reproducible six-node example. It is not an official organizer-provided benchmark.

![Weighted Max-Cut graph with edge weights](../results/weighted_maxcut_graph.svg)

### Processor A coupling map

Processor A is represented as a five-qubit connectivity graph with four unique undirected connections. The configuration is PDF-derived and pending organizer approval.

![Processor A coupling map](../results/processor_A_coupling.svg)

### Processor B coupling map

Processor B is represented as a nine-qubit connectivity graph with twelve unique undirected connections. The configuration is PDF-derived and pending organizer approval.

![Processor B coupling map](../results/processor_B_coupling.svg)

These are topology diagrams, not hardware-performance or noise visualizations. The basis-gate assumptions and noise parameters still require verification against the final organizer configuration.
"""

if marker in report:
    print("Diagram section already exists; no changes made.")
else:
    report_path.write_text(report.rstrip() + "\n\n" + section.strip() + "\n", encoding="utf-8")
    print("Added diagrams section to reports/report.md")

print("Report size:", report_path.stat().st_size, "bytes")
