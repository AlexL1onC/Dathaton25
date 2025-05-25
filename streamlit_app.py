import streamlit as st
import pandas as pd
import numpy as np
from KPI_FC import plot_user_transactions
import plotly.express as px
import altair as alt
from KPI_Jesus import graficar_promedio_usuario, graficar_gasto_por_servicio
from Porcentaje_Frecuencia import graficar_top5_comercios

data = pd.read_csv('df_merged_final.csv')

st.set_page_config(
    page_title="Identificacion de Usuario",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


with st.sidebar:
    st.title('XYZ')
    
    year_list = list(data['id'].unique())[::-1]
    
    selected_usuario = st.selectbox('Selecciona un Usuario', year_list, index=len(year_list)-1)
    df_selected_usuario = data[data['id'] == selected_usuario]
    df_selected_usuario_sorted = df_selected_usuario.sort_values(by="monto", ascending=False)

    if "vista_activa" not in st.session_state:
        st.session_state.vista_activa = "kpis"

    # Función para cambiar la vista
    def cambiar_vista(nueva_vista):
        st.session_state.vista_activa = nueva_vista

    # Crear dos columnas para los botones
    col1, col2 = st.columns(2)

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
    data = pd.read_csv('df_merged_final.csv')
    # Filtrar y ordenar los datos del Usuario 1 por fecha
    usuario = data[data['id'] == selected_usuario]

    col = st.columns((2.5, 3.5, 2), gap='medium')
    with col[0]:
       st.subheader("Top 5 Comercios")
       fig = graficar_gasto_por_servicio('df_merged_final.csv', selected_usuario, top_n=5)
       st.plotly_chart(fig, use_container_width=True)

       ftop5 = graficar_top5_comercios(selected_usuario, data)
       st.dataframe(ftop5, use_container_width=True)
       


    with col[1]:
        st.subheader("Gastos Totales")
        st.metric(label="Gastos Totales", value=f"${usuario['monto'].sum():,.0f}", delta=f"${usuario['monto'].sum():,.0f}")

        fig2 = px.line(usuario, x='fecha', y='monto',
                title='Gastos del Usuario 1 a lo largo del tiempo',
                labels={'fecha': 'Fecha', 'monto': 'Monto ($)'})
    
        fig2.update_layout(
        height=500,
        xaxis=dict(tickangle=45),
        hovermode="x unified")
        st.plotly_chart(fig2, use_container_width=True)

    with col[2]:
        fig3 = graficar_promedio_usuario('df_merged_final.csv', selected_usuario) 
        st.plotly_chart(fig3, use_container_width=True)

        
    


else:
    st.header("Vistade Prediccion de Compras")
    # Aquí colocas tus gráficos y predicciones
