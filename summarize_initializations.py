import csv
import numpy as np

with open("results/qaoa_p1_initializations.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

ratios = np.array([float(row["approx_ratio"]) for row in rows])
expected_cuts = np.array([float(row["ideal_expected_cut"]) for row in rows])

print("Initialization count:", len(rows))
print("Seeds:", [int(row["seed"]) for row in rows])
print("Mean ideal expected cut:", round(float(expected_cuts.mean()), 6))
print("Mean approximation ratio:", round(float(ratios.mean()), 6))
print("Population std of approximation ratio:", round(float(ratios.std(ddof=0)), 6))
print("Sample std of approximation ratio:", round(float(ratios.std(ddof=1)), 6))
print("Best ratio:", round(float(ratios.max()), 6))
print("Best seed:", int(rows[int(ratios.argmax())]["seed"]))
