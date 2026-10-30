from pathlib import Path

p = Path("calculate_optimal_probability.py")
s = p.read_text(encoding="utf-8")

s = s.replace(
    'bound_circuit = qaoa.ansatz.assign_parameters(optimal_point)\nstate = Statevector.from_instruction(bound_circuit)',
    'bound_circuit = qaoa.ansatz.assign_parameters(optimal_point)\n'
    'bound_circuit = bound_circuit.remove_final_measurements(inplace=False)\n'
    'state = Statevector.from_instruction(bound_circuit)'
)

p.write_text(s, encoding="utf-8")
print("Updated probability script.")
