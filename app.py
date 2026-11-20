from pathlib import Path

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