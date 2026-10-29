import json
from pathlib import Path

out = Path("processors")
out.mkdir(exist_ok=True)

common = {
    "team": "TECHDUDES",
    "problem_statement": "PS-O1",
    "basis_gates": ["rz", "sx", "x", "cx"],
    "noise": {
        "model": "official",
        "p1": 0.001,
        "p2": 0.005,
        "p_readout": 0.01
    }
}

processors = {
    "processor_A.json": {
        "name": "Processor A",
        "num_qubits": 5,
        "edges": [[0, 1], [1, 2], [1, 3], [3, 4]]
    },
    "processor_B.json": {
        "name": "Processor B",
        "num_qubits": 9,
        "edges": [
            [0, 1], [1, 2], [1, 6], [2, 3],
            [2, 6], [2, 5], [3, 4], [4, 5],
            [5, 6], [6, 7], [6, 8], [8, 0]
        ]
    }
}

for filename, processor in processors.items():
    document = {**common, **processor}
    path = out / filename
    path.write_text(
        json.dumps(document, indent=2) + "\n",
        encoding="utf-8"
    )
    print("Created:", path)
