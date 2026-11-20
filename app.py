from pathlib import Path

import pandas as pd
import streamlit as st

csv_path = Path(__file__).parent / "data" / "raw" / "ai4i2020.csv"
data = pd.read_csv(csv_path)

st.title("FactoryPulse AI")
st.metric("Taux de panne global", f"{data['Machine failure'].mean():.2%}")

by_type = data.groupby("Type")["Machine failure"].agg(
    observations="size",
    pannes="sum",
)
by_type["Taux de panne (%)"] = 100 * by_type["pannes"] / by_type["observations"]

st.subheader("Taux de panne par type de produit")
st.bar_chart(by_type, y="Taux de panne (%)")

st.subheader("Détail du calcul")
st.dataframe(by_type.style.format({"Taux de panne (%)": "{:.2f}"}))