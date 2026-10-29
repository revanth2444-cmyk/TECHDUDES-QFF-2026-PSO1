import json
from pathlib import Path
import qff_phase2 as qff

path = Path("processor_D_template.json")
p = json.loads(path.read_text(encoding="utf-8"))

p["team"] = "TECHDUDES"
p["problem_statement"] = "PS-O1"
p["design_rationale"] = (
    "The connected 9-qubit topology provides 12 couplings with maximum degree 3, "
    "supporting six logical qubits while providing multiple routing paths for "
    "two-qubit operations. It is designed to avoid the five-qubit capacity "
    "bottleneck of Processor A and offer alternative routes for mapping the "
    "weighted Max-Cut QAOA circuit."
)

errors = qff.validate_processor_d(p, 6)
if errors:
    raise SystemExit("Processor D validation failed:\n- " + "\n- ".join(errors))

path.write_text(json.dumps(p, indent=2) + "\n", encoding="utf-8")
print("Processor D updated and validated successfully.")
print(json.dumps(p, indent=2))
