
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
@st.cache_data
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

# Sidebar para filtros
st.sidebar.header("🎛️ Filtros")

selected_classes = st.sidebar.multiselect(
    "Selecciona las clases de pasajeros:",
    options=[1, 2, 3],
    default=[1, 2, 3]
)

age_range = st.sidebar.slider(
    "Rango de edad:",
    min_value=0,
    max_value=80,
    value=(0, 80),
    step=1
)

show_male = st.sidebar.checkbox("Mostrar hombres", value=True)
show_female = st.sidebar.checkbox("Mostrar mujeres", value=True)

# Filtrar los datos
df_filtered = df.copy()
df_filtered = df_filtered[df_filtered['Pclass'].isin(selected_classes)]
df_filtered = df_filtered[(df_filtered['Age'] >= age_range[0]) & (df_filtered['Age'] <= age_range[1])]

gender_filter = []
if show_male:
    gender_filter.append('male')
if show_female:
    gender_filter.append('female')
    
if gender_filter:
    df_filtered = df_filtered[df_filtered['Sex'].isin(gender_filter)]

# Mostrar datos filtrados
st.header("📈 Datos Filtrados")
st.write(f"Mostrando {len(df_filtered)} de {len(df)} pasajeros")

if len(df_filtered) > 0:
    # Visualizaciones
    st.subheader("🚻 Supervivencia por Género")
    col1, col2 = st.columns(2)
    
    with col1:
        survival_by_gender = df_filtered.groupby(['Sex', 'Survived']).size().unstack(fill_value=0)
        if not survival_by_gender.empty:
            fig, ax = plt.subplots(figsize=(8, 6))
            survival_by_gender.plot(kind='bar', ax=ax)
            ax.set_title('Supervivencia por Género')
            ax.set_xlabel('Género')
            ax.set_ylabel('Número de Pasajeros')
            ax.legend(['No Sobrevivió', 'Sobrevivió'])
            plt.xticks(rotation=0)
            st.pyplot(fig)
    
    with col2:
        survival_rate = df_filtered.groupby('Sex')['Survived'].mean()
        st.write("**Tasa de Supervivencia:**")
        for gender in survival_rate.index:
            st.write(f"- {gender.title()}: {survival_rate[gender]:.1%}")

    # Análisis personalizado
    st.subheader("🔍 Análisis Personalizado")
    analysis_type = st.selectbox(
        "Selecciona el tipo de análisis:",
        ["Supervivencia por Clase", "Supervivencia por Puerto de Embarque", "Datos Raw"]
    )
    
    if analysis_type == "Supervivencia por Clase":
        class_survival = df_filtered.groupby('Pclass')['Survived'].mean()
        st.bar_chart(class_survival)
        
    elif analysis_type == "Supervivencia por Puerto de Embarque":
        port_survival = df_filtered.dropna(subset=['Embarked']).groupby('Embarked')['Survived'].mean()
        st.bar_chart(port_survival)
        
    elif analysis_type == "Datos Raw":
        st.dataframe(df_filtered)
else:
    st.warning("No hay datos que coincidan con los filtros seleccionados.")
