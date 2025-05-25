import streamlit as st
import pandas as pd
import numpy as np
from KPI_FC import plot_user_transactions
import plotly.express as px
import altair as alt
from KPI_Jesus import graficar_promedio_usuario, graficar_gasto_por_servicio
from Porcentaje_Frecuencia import graficar_top5_comercios
from LSTM import predecir_usuario_adelante
import joblib
from tensorflow.keras.models import load_model
from kpiahorro import ahorro_interes_compuesto_diario
from anomalias_combinadas import detectar_anomalias_combinadas
from ComercioPrediccion import probabilidad_consumo_en_dia

data = pd.read_csv('df_merged_final.csv')





st.set_page_config(
    page_title="CashFlow",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

st.markdown(
    """
    <style>
    /* Estilo general del sidebar */
    [data-testid="stSidebar"] {
        background-color: #e0f7ef;
        padding: 2rem 1rem;
        border-radius: 0 1rem 1rem 0;
        box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
    }

    /* Título del sidebar */
    [data-testid="stSidebar"] h1 {
        font-size: 2rem !important;
        color: #1e3932 !important;
        font-weight: 700 !important;
        margin-bottom: 1rem;
    }

    /* Subtítulos */
    [data-testid="stSidebar"] h3 {
        color: #1e3932 !important;
        font-size: 1.2rem !important;
        margin-top: 1.5rem;
    }

    /* Selectbox */
    .stSelectbox > div {
        background-color: #fff;
        border-radius: 8px;
        padding: 0.5rem;
        box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);
    }

    /* Botones */
    .stButton button {
        background-color: #1e3932;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }

    .stButton button:hover {
        background-color: #145c4c;
    }

    /* Divider */
    .st-emotion-cache-1avcm0n {
        margin-top: 1rem;
        margin-bottom: 1rem;
        border-color: #ccc;
    }

        .metric-label {
        font-size: 1rem;
        color: #6c757d;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .stPlotlyChart {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    .stDataFrame {
        margin-top: 1rem;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    .block-container {
        padding-top: 2rem;
    }

    .kpi-box {
        padding: 1.5rem;
        background-color: #f9f9f9;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        margin-bottom: 1.5rem;
    }

    .stSubheader {
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)



with st.sidebar:
    st.title('Hey, CashFlow!')
    
    year_list = list(data['id'].unique())[::-1]
    selected_usuario = st.selectbox('Selecciona un Usuario', year_list, index=len(year_list)-1)

    df_selected_usuario = data[data['id'] == selected_usuario]
    df_selected_usuario_sorted = df_selected_usuario.sort_values(by="monto", ascending=False)

    if "vista_activa" not in st.session_state:
        st.session_state.vista_activa = "kpis"

    def cambiar_vista(nueva_vista):
        st.session_state.vista_activa = nueva_vista

    st.divider()
    st.subheader("Selecciona una Vista")

    col1, col2 = st.columns(2)

    with col1:
        st.button("Historial", on_click=cambiar_vista, args=("kpis",))

    with col2:
        st.button("Predicción", on_click=cambiar_vista, args=("graficos",))




# Mostrar contenido según la vista activa
if st.session_state.vista_activa == "kpis":
    st.markdown("## Vista Histórica de Compras")
    st.markdown("---")

    data = pd.read_csv('df_merged_final.csv')
    usuario = data[data['id'] == selected_usuario]

    col = st.columns((2.5, 3.5), gap='large')

    # === Columna 1 ===
    with col[0]:
        st.subheader("🏪 Top 5 Comercios frecuentes anual")
        fig = graficar_gasto_por_servicio('df_merged_final.csv', selected_usuario, top_n=5)
        st.plotly_chart(fig, use_container_width=True)

        # Ajuste visual
        st.markdown(
           """
           <style>
           .element-container:has(.js-plotly-plot) + .element-container {margin-top: -80px;}
           </style>
           """, unsafe_allow_html=True)

        ftop5 = graficar_top5_comercios(selected_usuario, data)
        st.data_editor(ftop5, use_container_width=True, hide_index=True, disabled=True)

    # === Columna 2 ===
    with col[1]:
        st.subheader("💰 Gastos Totales")

        usuario['fecha'] = pd.to_datetime(usuario['fecha'])
        usuario['año_mes'] = usuario['fecha'].dt.to_period('M')
        gastos_mensuales = usuario.groupby('año_mes')['monto'].sum().sort_index()

        if len(gastos_mensuales) >= 2:
            gasto_ultimo_mes = gastos_mensuales.iloc[-1]
            gasto_mes_anterior = gastos_mensuales.iloc[-2]
            delta = gasto_ultimo_mes - gasto_mes_anterior
        elif len(gastos_mensuales) == 1:
            gasto_ultimo_mes = gastos_mensuales.iloc[-1]
            gasto_mes_anterior = 0
            delta = gasto_ultimo_mes
        else:
            gasto_ultimo_mes = 0
            delta = 0

        col = st.columns((2.5, 2.5, 2.5), gap='large')
        with col[0]:
            st.metric(
                label=f"Gasto Total Mensual ({gastos_mensuales.index[-1] if len(gastos_mensuales) > 0 else ''})",
                value=f"${gasto_ultimo_mes:,.0f}",
                delta=int(delta),
                delta_color="normal"
            )
        resumen = graficar_promedio_usuario('df_merged_final.csv', selected_usuario)
        with col[1]:
            st.metric(
                label="Promedio Mensual",
                value=f"${resumen['Monto'][1]:,.2f}",
                delta=None
            )
        with col[2]:
            st.metric(
                label="Promedio Semanal",
                value=f"${resumen['Monto'][0]:,.2f}",
                delta=None
            )

        fig2 = px.line(
            usuario, x='fecha', y='monto',
            title='Gastos a lo largo del tiempo',
            labels={'fecha': 'Fecha', 'monto': 'Monto ($)'},
        )

        fig2.update_layout(
            height=450,
            xaxis=dict(tickangle=45),
            hovermode="x unified",
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor="#fff",
        )

        st.plotly_chart(fig2, use_container_width=True)
        


else:
    st.markdown("## Vista de Predicción de Compras")
    st.markdown("---")

    scaler_cargado = joblib.load('scaler_model.save')
    model_cargado = load_model('modelo_lstm.h5')
    data2 = pd.read_csv('df_merged_clean.csv')

    col = st.columns((2.5, 3.5), gap='large')

    # === Columna 1 ===
    with col[0]:
        st.subheader("📊 Predicciones de Compras")
  

        # Filtros interactivos
        dias = st.slider("Cantidad de días a proyectar", min_value=30, max_value=365, value=120, step=1)
        tasa = st.slider("Tasa anual (%)", min_value=1, max_value=30, value=10, step=1) / 100
        predicciones = predecir_usuario_adelante(
                data2, selected_usuario, model_cargado,
                scaler_cargado, n_lags=3, timesteps=5, pasos_a_predecir=dias
            )
        
        ahorros = ahorro_interes_compuesto_diario(predicciones, tasa_anual=tasa, meses=dias//30)

        st.metric(
            label="Predicción última recurrencia de compra",
            value=f"${predicciones[-1]:,.2f}" if predicciones else "N/A",
        )


        st.metric(
            label="Ahorro proyectado (interés compuesto)",
            value=f"${ahorros[-1]:,.2f}",
        )

        # Gráfico de evolución del ahorro
        df_ahorros = pd.DataFrame({
            'Día': range(1, len(ahorros) + 1),
            'Ahorro': ahorros
        })

        fig5 = alt.Chart(df_ahorros).mark_line(
            color="#34a0a4"
        ).encode(
            x=alt.X('Día', title='Días'),
            y=alt.Y('Ahorro', title='Ahorro ($)'),
            tooltip=['Día', 'Ahorro']
        ).properties(
            title='📈 Ahorro proyectado con Interés Compuesto',
            height=300
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        )

        st.altair_chart(fig5, use_container_width=True)

    # === Columna 2 ===
    with col[1]:
        st.subheader("⚠️ Anomalías y Predicción de Consumo")

        fechas, montos = detectar_anomalias_combinadas(data2, selected_usuario)

        if fechas:
            with st.container():
                st.markdown("### 🔍 Anomalías Detectadas")
                for f, m in zip(fechas, montos):
                    st.markdown(f"- **{f.date()}** → `${m:,.2f}`")
        else:
            st.success("✅ No se detectaron anomalías en las compras recientes.")

        data = pd.read_csv('df_merged_final.csv')
        comercio_top = data[data['id'] == selected_usuario]['comercio'].mode()[0]
        resultado = probabilidad_consumo_en_dia(data, dia_objetivo=15, usuario=selected_usuario)

        st.markdown("### 📅 Predicción por Día")
        prob_total = 0
        dias_rango = range(1, 14)  # Por ejemplo, del día 15 al 21

        for dia in dias_rango:
            resultado = probabilidad_consumo_en_dia(data, dia_objetivo=dia, usuario=selected_usuario)
            # Solo sumar si el comercio más probable es el comercio_top
            if resultado['prediccion_dia_siguiente']['comercio_mas_probable'] == comercio_top:
                prob_total += resultado['probabilidad_consumo_en_dia']

        st.metric(
            label=f"Probabilidad total de compra en {comercio_top} (días 1-14)",
            value=f"{prob_total:.2f}%"
        )

        prob_total1 = 0
        dias_rango1 = range(15, 30)  # Por ejemplo, del día 15 al 21

        for dia in dias_rango1:
            resultado = probabilidad_consumo_en_dia(data, dia_objetivo=dia, usuario=selected_usuario)
            # Solo sumar si el comercio más probable es el comercio_top
            if resultado['prediccion_dia_siguiente']['comercio_mas_probable'] == comercio_top:
                prob_total1 += resultado['probabilidad_consumo_en_dia']

        st.metric(
            label=f"Probabilidad total de compra en {comercio_top} (días 15-30)",
            value=f"{prob_total1:.2f}%"
        )
        st.markdown("---")

