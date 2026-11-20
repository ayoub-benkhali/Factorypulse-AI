from pathlib import Path

import pandas as pd

project_dir = Path(__file__).resolve().parents[1]
data = pd.read_csv(project_dir / "data" / "raw" / "ai4i2020.csv")

observations = len(data)
failures = data["Machine failure"].eq(1).sum()
failure_rate = failures / observations

print(f"Observations : {observations}")
print(f"Observations avec panne : {failures}")
print(f"Taux de panne : {failure_rate:.2%}")

by_type = data.groupby("Type")["Machine failure"].agg(
    observations="size",
    failures="sum",
)
by_type["failure_rate"] = by_type["failures"] / by_type["observations"]
by_type = by_type.sort_values("failure_rate", ascending=False)

print("\nTaux de panne par type de produit")
print(by_type.to_string(formatters={"failure_rate": "{:.2%}".format}))