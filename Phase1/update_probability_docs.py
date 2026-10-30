import json
from pathlib import Path

report_path = Path("reports/report.md")
notebook_path = Path("main.ipynb")
result_path = Path("results/o1_optimal_probability.json")

data = json.loads(result_path.read_text(encoding="utf-8"))

# Add the probability results to the report once.
report = report_path.read_text(encoding="utf-8")
heading = "## Optimal-bitstring probability"

if heading not in report:
    section = f"""

{heading}

For the reproducible local example (not an official organizer-provided
benchmark), the exact noiseless statevector calculation gives:

- Exact Max-Cut optimum: **{data['exact_max_cut_value']}**
- Optimized QAOA objective: **{data['qaoa_objective_value']}**
- Probability of measuring any optimal bitstring: **{data['optimal_bitstring_probability_percent']:.4f}%**
- Optimal bitstrings (in x0-to-x5 order): `{data['optimal_bitstrings_x0_to_x5'][0]}` and `{data['optimal_bitstrings_x0_to_x5'][1]}`
- Probability of each optimal bitstring: **{100 * data['individual_optimal_bitstring_probabilities'][data['optimal_bitstrings_x0_to_x5'][0]]:.4f}%** and **{100 * data['individual_optimal_bitstring_probabilities'][data['optimal_bitstrings_x0_to_x5'][1]]:.4f}%**

This is an ideal statevector probability, not a hardware-measured success
probability. No hardware noise or shot sampling is included. The graph is a
local reproducible example, not an official benchmark.
"""
    report_path.write_text(report.rstrip() + "\n" + section, encoding="utf-8")
    print("Added optimal-bitstring probability to report.")
else:
    print("Report probability section already exists; left unchanged.")

# Add a results cell to the notebook once.
nb = json.loads(notebook_path.read_text(encoding="utf-8"))
marker = "o1_optimal_probability.json"

already_added = any(
    cell.get("cell_type") == "code"
    and marker in "".join(cell.get("source", []))
    for cell in nb["cells"]
)

if not already_added:
    nb["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Optimal-bitstring probability\n",
            "\n",
            "The following result is an exact noiseless statevector estimate for the local example graph, not a hardware-measured probability or an official benchmark.\n"
        ]
    })
    nb["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import json\n",
            "from pathlib import Path\n",
            "\n",
            "probability_result = json.loads(\n",
            "    Path('results/o1_optimal_probability.json').read_text(encoding='utf-8')\n",
            ")\n",
            "print(f\"Exact Max-Cut optimum: {probability_result['exact_max_cut_value']}\")\n",
            "print(f\"QAOA objective: {probability_result['qaoa_objective_value']}\")\n",
            "print(f\"Optimal-bitstring probability: {probability_result['optimal_bitstring_probability_percent']:.4f}%\")\n",
            "print('Optimal bitstrings:', ', '.join(probability_result['optimal_bitstrings_x0_to_x5']))\n",
            "print('Method:', probability_result['probability_method'])\n",
            "print('Limitations:', '; '.join(probability_result['limitations']))\n"
        ]
    })
    notebook_path.write_text(
        json.dumps(nb, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print("Added probability results cell to notebook.")
else:
    print("Notebook probability cell already exists; left unchanged.")

# Validate the notebook JSON and required files.
json.loads(notebook_path.read_text(encoding="utf-8"))
assert heading in report_path.read_text(encoding="utf-8")
assert result_path.exists()
print("Validation passed: report, notebook JSON, and probability JSON are present.")
print(f"Notebook cells: {len(nb['cells'])}")
