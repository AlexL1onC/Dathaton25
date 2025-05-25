import pandas as pd
import plotly.express as px

def graficar_promedio_usuario(ruta_csv, nombre_usuario):
    df = pd.read_csv(ruta_csv)
    df['fecha'] = pd.to_datetime(df['fecha'])
    usuarios_unicos = df['id'].unique()

    try:
        indice = int(nombre_usuario.replace("Usuario ", "")) - 1
    except:
        print("Formato inválido. Usa: 'Usuario 1', 'Usuario 2', etc.")
        return

    if indice < 0 or indice >= len(usuarios_unicos):
        print(f"{nombre_usuario} no existe.")
        return

    usuario_id = usuarios_unicos[indice]
    df_usuario = df[df['id'] == usuario_id].copy()
    df_usuario['año'] = df_usuario['fecha'].dt.isocalendar().year
    df_usuario['semana'] = df_usuario['fecha'].dt.isocalendar().week
    promedio_semanal = df_usuario.groupby(['año', 'semana'])['monto'].sum().mean()
    promedio_mensual = promedio_semanal * 4.345

    resumen = pd.DataFrame({
        'Tipo': ['Promedio Semanal', 'Promedio Mensual'],
        'Monto': [promedio_semanal, promedio_mensual],
        'Texto': [f"${promedio_semanal:,.2f}", f"${promedio_mensual:,.2f}"]
    })

    fig = px.bar(
        resumen,
        x='Monto',
        y='Tipo',
        text='Texto',
        title=f'Gasto semanal y mensual estimado de {nombre_usuario}',
        color='Tipo',
        color_discrete_sequence=['#1f77b4', '#ff7f0e']
    )

    fig.update_traces(
        textposition='inside',
        textfont_size=42
    )

    fig.update_layout(
        yaxis_title="",
        xaxis_title="Monto estimado (MXN)",
        showlegend=False,
        uniformtext_minsize=12,
        uniformtext_mode='show',
        height=500
    )

    return fig


def graficar_gasto_por_servicio(ruta_csv, nombre_usuario, top_n=5):
    df = pd.read_csv(ruta_csv)
    df['fecha'] = pd.to_datetime(df['fecha'])
    usuarios_unicos = df['id'].unique()

    try:
        indice = int(nombre_usuario.replace("Usuario ", "")) - 1
    except:
        print("Formato inválido. Usa: 'Usuario 1', 'Usuario 2', etc.")
        return

    if indice < 0 or indice >= len(usuarios_unicos):
        print(f"{nombre_usuario} no existe.")
        return

    usuario_id = usuarios_unicos[indice]
    df_usuario = df[df['id'] == usuario_id].copy()

    resumen = df_usuario.groupby('comercio')['monto'].sum().reset_index()
    resumen = resumen.sort_values(by='monto', ascending=False)

    top = resumen.head(top_n)
    otros = resumen.iloc[top_n:]
    otros_sum = otros['monto'].sum()

    if otros_sum > 0:
        otros_row = pd.DataFrame({'comercio': ['Otros'], 'monto': [otros_sum]})
        resumen_final = pd.concat([top, otros_row], ignore_index=True)
    else:
        resumen_final = top

    resumen_final['monto'] = resumen_final['monto'].round(2)

    fig = px.pie(
        resumen_final,
        names='comercio',
        values='monto',
        title=f"Gasto histórico por comercio - {nombre_usuario} (Top {top_n} + Otros)",
        hole=0.4
    )
    fig.update_traces(textinfo='label+percent', hovertemplate='%{label}: $%{value:,.2f}<extra></extra>')
    
    return fig
