from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from prepare_data import FEATURES, prepare_data


def train_model(X_train, y_train):
    numeric_columns = [column for column in FEATURES if column != "Type"]

    preprocessing = ColumnTransformer([
        ("type", OneHotEncoder(handle_unknown="ignore"), ["Type"]),
        ("measures", StandardScaler(), numeric_columns),
    ])

    model = make_pipeline(
        preprocessing,
        LogisticRegression(class_weight="balanced", max_iter=1000),
    )
    return model.fit(X_train, y_train)


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = prepare_data()
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)

    detected = ((predictions == 1) & (y_test == 1)).sum()
    false_alarms = ((predictions == 1) & (y_test == 0)).sum()

    print(f"Observations d'entraînement : {len(X_train)}")
    print(f"Observations de test : {len(X_test)}")
    print(f"Pannes détectées : {detected} sur {y_test.sum()}")
    print(f"Fausses alertes : {false_alarms}")