
import copy
import json
from pathlib import Path

from qff_phase2 import validate_processor_d


ROOT = Path(__file__).resolve().parents[1]

with open(ROOT / "processors" / "processor_D.json", encoding="utf-8") as f:
    VALID_PROCESSOR = json.load(f)


def test_valid_processor_d():
    assert validate_processor_d(copy.deepcopy(VALID_PROCESSOR), 6) == []


def test_insufficient_qubits():
    p = copy.deepcopy(VALID_PROCESSOR)
    p["num_qubits"] = 5
    assert validate_processor_d(p, 6)


def test_too_many_qubits():
    p = copy.deepcopy(VALID_PROCESSOR)
    p["num_qubits"] = 13
    assert validate_processor_d(p, 6)


def test_wrong_basis_gates():
    p = copy.deepcopy(VALID_PROCESSOR)
    p["basis_gates"] = ["h", "cx"]
    assert validate_processor_d(p, 6)


def test_invalid_edge():
    p = copy.deepcopy(VALID_PROCESSOR)
    p["edges"].append([0, 9])
    assert validate_processor_d(p, 6)


def test_duplicate_edge():
    p = copy.deepcopy(VALID_PROCESSOR)
    p["edges"].append([1, 0])
    assert validate_processor_d(p, 6)


def test_malformed_edge():
    p = copy.deepcopy(VALID_PROCESSOR)
    p["edges"].append(["bad", 2])
    assert validate_processor_d(p, 6)


def test_disconnected_graph():
    p = copy.deepcopy(VALID_PROCESSOR)
    p["edges"] = [[0, 1], [1, 2]]
    assert validate_processor_d(p, 6)


def test_excessive_degree():
    p = copy.deepcopy(VALID_PROCESSOR)
    p["edges"] = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5]]
    assert validate_processor_d(p, 6)


def test_noise_below_official_minimum():
    p = copy.deepcopy(VALID_PROCESSOR)
    p["noise"]["p2"] = 0.001
    assert validate_processor_d(p, 6)


def test_invalid_noise_value():
    p = copy.deepcopy(VALID_PROCESSOR)
    p["noise"]["p1"] = float("nan")
    assert validate_processor_d(p, 6)


def test_missing_noise():
    p = copy.deepcopy(VALID_PROCESSOR)
    p["noise"] = None
    assert validate_processor_d(p, 6)


def test_non_dictionary_input():
    assert validate_processor_d(None, 6)


def test_boolean_qubit_count():
    p = copy.deepcopy(VALID_PROCESSOR)
    p["num_qubits"] = True
    assert validate_processor_d(p, 6)
def test_malformed_basis_gates():
    p = copy.deepcopy(VALID_PROCESSOR)
    p["basis_gates"] = [["rz"], "cx"]
    assert validate_processor_d(p, 6)
