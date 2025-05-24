import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Data Analysis App",
    page_icon="📊"
    )

st.title('XYZ')

st.write('Hello world!')


#df_reshaped = pd.read_csv("data/reshaped.csv")

# Inicializar el estado de la sesión
if "vista_activa" not in st.session_state:
    st.session_state.vista_activa = "kpis"

# Función para cambiar la vista
def cambiar_vista(nueva_vista):
    st.session_state.vista_activa = nueva_vista

# Crear dos columnas para los botones
col1, col2, col3 = st.columns(3)

with col1:
    st.button(
        "📊 Vista Historica de Compras",
        on_click=cambiar_vista,
        args=("kpis",) 
    )

with col2:
    st.button(
        "📈 Vista de Prediccion de Compras",
        on_click=cambiar_vista,
        args=("graficos",)
    )


# Mostrar contenido según la vista activa
if st.session_state.vista_activa == "kpis":
    st.header("Vista Historica de Compras")
    # Aquí colocas tus KPIs






else:
    st.header("Vistade Prediccion de Compras")
    # Aquí colocas tus gráficos y predicciones
