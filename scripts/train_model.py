from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import confusion_matrix

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
    tn, fp, fn, tp = confusion_matrix(y_test, predictions, labels=[0, 1]).ravel()

    print("\nMatrice de confusion")
    print(f"{'État réel':<16}{'Aucune alerte':>16}{'Alerte':>10}")
    print(f"{'Sans panne':<16}{tn:>16}{fp:>10}")
    print(f"{'En panne':<16}{fn:>16}{tp:>10}")

    print(f"\nRappel : {tp} pannes détectées sur {tp + fn} ({tp / (tp + fn):.1%})")
    print(f"Fausses alertes : {fp} sur {tp + fp} alertes déclenchées")