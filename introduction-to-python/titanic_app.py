
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar la página
st.set_page_config(
    page_title="Análisis del Titanic",
    page_icon="🚢",
    layout="wide"
)

# Título principal
st.title("🚢 Análisis de Supervivencia del Titanic")
st.markdown("### Una aplicación interactiva para explorar los datos del Titanic")

# Cargar los datos
@st.cache_data  # Cache para mejorar rendimiento
def load_data():
    return pd.read_csv("C:\\Users\\franp\\Downloads\\train.csv")

df = load_data()

# Mostrar información básica
st.header("📊 Información General")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de Pasajeros", len(df))
with col2:
    st.metric("Supervivientes", df['Survived'].sum())
with col3:
    st.metric("Tasa de Supervivencia", f"{df['Survived'].mean():.1%}")

# Mostrar los primeros datos
st.subheader("Primeras filas de los datos")
st.dataframe(df.head())
