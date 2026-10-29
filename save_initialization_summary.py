import csv
import numpy as np
from pathlib import Path

with open("results/qaoa_p1_initializations.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

ratios = np.array([float(r["approx_ratio"]) for r in rows])
cuts = np.array([float(r["ideal_expected_cut"]) for r in rows])

summary = [{
    "initialization_count": len(rows),
    "seeds": ";".join(r["seed"] for r in rows),
    "mean_ideal_expected_cut": cuts.mean(),
    "mean_approx_ratio": ratios.mean(),
    "population_std_approx_ratio": ratios.std(ddof=0),
    "sample_std_approx_ratio": ratios.std(ddof=1),
    "best_seed": rows[int(ratios.argmax())]["seed"],
    "best_approx_ratio": ratios.max(),
}]

out = Path("results/tables/initialization_summary.csv")
with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=summary[0].keys())
    writer.writeheader()
    writer.writerows(summary)

print("Saved:", out)
print("Rows:", len(summary))
