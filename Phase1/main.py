"""Run the classical Max-Cut baseline on the explicitly labeled toy graph."""
import json
from pathlib import Path
from src.problem import exact_max_cut, cut_value

ROOT = Path(__file__).resolve().parent
TOY_PATH = ROOT / "data" / "toy_graph.json"
OUT_PATH = ROOT / "results" / "toy_result.json"


def main():
    graph = json.loads(TOY_PATH.read_text(encoding="utf-8"))
    nodes, edges = graph["nodes"], graph["edges"]

    best_value, best_partition = exact_max_cut(nodes, edges)
    # Independently recompute the value for a basic consistency check.
    checked_value = cut_value(nodes, edges, best_partition)
    assert abs(best_value - checked_value) < 1e-9

    result = {
        "instance_name": graph["instance_name"],
        "official_benchmark": False,
        "warning": graph["warning"],
        "nodes": len(nodes),
        "edges": len(edges),
        "exact_max_cut_value": best_value,
        "best_partition": {str(k): v for k, v in best_partition.items()},
        "verification_passed": True
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("INSTANCE:", result["instance_name"])
    print("OFFICIAL BENCHMARK:", result["official_benchmark"])
    print("Exact maximum cut value:", best_value)
    print("Best partition (node -> side):", best_partition)
    print("Verification passed:", result["verification_passed"])
    print("Saved:", OUT_PATH.relative_to(ROOT))


if __name__ == "__main__":
    main()
