from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

CSV_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "ai4i2020.csv"

FEATURES = [
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
]


def prepare_data():
    data = pd.read_csv(CSV_PATH)
    X = data[FEATURES]
    y = data["Machine failure"]

    return train_test_split(X, y, test_size=0.20, stratify=y, random_state=42)


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = prepare_data()

    print(f"Variables d'entrée : {X_train.shape[1]}")
    print(f"Entraînement : {len(X_train)} observations, {y_train.sum()} pannes")
    print(f"Test : {len(X_test)} observations, {y_test.sum()} pannes")