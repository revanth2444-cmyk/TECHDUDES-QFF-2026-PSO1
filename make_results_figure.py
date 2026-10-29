import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path.cwd()
source = root / "results" / "tables" / "results.csv"
out_dir = root / "results" / "figures"
out_dir.mkdir(parents=True, exist_ok=True)

with source.open("r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

labels = []
means = []
for row in rows:
    if row.get("executable", "").strip().lower() != "true":
        continue
    try:
        mean = float(row["mean_cut"])
    except (ValueError, TypeError, KeyError):
        continue
    processor = row["processor"]
    condition = "Noisy" if row["noisy"].strip().lower() == "true" else "Ideal"
    labels.append(f"{processor}\n{condition}")
    means.append(mean)

if not labels:
    raise ValueError("No executable mean-cut results found in results.csv")

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(labels, means)
ax.axhline(22, linestyle="--", label="Exact optimum = 22")
ax.set_ylabel("Mean sampled cut")
ax.set_title("QAOA p=1: Mean Cut by Processor and Condition")
ax.set_ylim(0, 24)
ax.legend()
ax.bar_label(bars, fmt="%.2f", padding=3)
fig.tight_layout()

output = out_dir / "qaoa_mean_cut.png"
fig.savefig(output, dpi=160)
plt.close(fig)
print("Saved figure:", output)
print("Bars:", len(labels))
