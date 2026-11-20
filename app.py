from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

csv_path = Path(__file__).parent / "data" / "raw" / "ai4i2020.csv"
data = pd.read_csv(csv_path)

st.title("FactoryPulse AI")

selected_type = st.selectbox("Type de produit", ["Tous", "L", "M", "H"])

if selected_type != "Tous":
    data = data.loc[data["Type"] == selected_type]

st.metric("Taux de panne", f"{data['Machine failure'].mean():.2%}")

by_type = data.groupby("Type")["Machine failure"].agg(
    observations="size",
    pannes="sum",
)
by_type["Taux de panne (%)"] = 100 * by_type["pannes"] / by_type["observations"]

st.subheader("Taux de panne par type de produit")
st.bar_chart(by_type, y="Taux de panne (%)")

st.subheader("Détail du calcul")
st.dataframe(by_type.style.format({"Taux de panne (%)": "{:.2f}"}))

st.subheader("Taux de panne selon l’usure de l’outil")

wear_band = pd.cut(
    data["Tool wear [min]"],
    bins=[0, 100, 150, 200, float("inf")],
    labels=["0–99 min", "100–149 min", "150–199 min", "200 min et plus"],
    right=False,
)

by_wear = data.groupby(wear_band, observed=False)["Machine failure"].agg(
    observations="size",
    pannes="sum",
)
by_wear.index.name = "Usure de l’outil"
by_wear["Taux de panne (%)"] = (
    100 * by_wear["pannes"] / by_wear["observations"]
)

st.bar_chart(by_wear, y="Taux de panne (%)")
st.dataframe(by_wear.style.format({"Taux de panne (%)": "{:.2f}"}, na_rep="—"))


st.header("Évaluation du modèle")
st.caption("Régression logistique · 2 000 observations de test · Tous types de produits")

matrix_path = Path(__file__).resolve().parent / "reports" / "confusion_matrix.csv"
matrix = pd.read_csv(matrix_path, index_col="État réel")
st.table(matrix)

detected = matrix.loc["En panne", "Alerte"]
missed = matrix.loc["En panne", "Aucune alerte"]
st.metric("Pannes détectées sur le jeu de test", f"{detected} / {detected + missed}")

st.header("Tester une prédiction")
st.caption("Saisis les mesures d’une observation pour obtenir la décision du modèle.")

with st.form("prediction_form"):
    product_type = st.selectbox("Type du produit à tester", ["L", "M", "H"])
    air_temp = st.number_input("Température de l’air (K)", value=300.0, step=0.1)
    process_temp = st.number_input("Température du processus (K)", value=310.0, step=0.1)
    speed = st.number_input("Vitesse de rotation (tr/min)", min_value=0, value=1500)
    torque = st.number_input("Couple (Nm)", min_value=0.0, value=40.0, step=0.1)
    wear = st.number_input("Usure de l’outil (min)", min_value=0, value=100)
    submitted = st.form_submit_button("Tester la prédiction")

if submitted:
    observation = pd.DataFrame([{
        "Type": product_type,
        "Air temperature [K]": air_temp,
        "Process temperature [K]": process_temp,
        "Rotational speed [rpm]": speed,
        "Torque [Nm]": torque,
        "Tool wear [min]": wear,
    }])

    model_path = Path(__file__).resolve().parent / "models" / "failure_model.joblib"
    model = joblib.load(model_path)
    prediction = model.predict(observation)[0]

    if prediction == 1:
        st.warning("Alerte de panne selon le modèle.")
    else:
        st.success("Aucune alerte selon le modèle.")