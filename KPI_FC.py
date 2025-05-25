import pandas as pd
import plotly.express as px
from ipywidgets import interact, widgets

# Cargar el CSV
df = pd.read_csv("df_merged_final.csv")  # Reemplaza con tu ruta

# Convertir la columna de fecha a datetime
df['date'] = pd.to_datetime(df['fecha'])

# Widget para seleccionar usuario
user_ids = df['id'].unique()

def plot_user_transactions(user_id):
    # Filtrar datos del usuario
    user_data = df[df['id'] == user_id]
    
    if user_data.empty:
        print("Usuario no encontrado o sin transacciones.")
        return
    
    # Agrupar por fecha y sumar montos
    history = user_data.groupby('date')['monto'].sum().reset_index()
    
    # Crear gráfico interactivo con Plotly
    fig = px.line(
        history,
        x='date',
        y='monto',
        markers=True,  # Añade marcadores en los puntos
        title=f'Histórico de Transacciones - Usuario {user_id}',
        labels={'date': 'Fecha', 'monto': 'Monto Total'},
    )
    
    # Personalizar diseño
    fig.update_layout(
        hovermode='x unified',  # Muestra tooltips al pasar el mouse
        xaxis=dict(tickangle=45),  # Rotar etiquetas del eje X
        showlegend=False,
    )
    
    # Mostrar el gráfico
    fig.show()


# Ejemplo manual (si no usas el widget interactivo)
# plot_user_transactions('Usuario 1')  # Cambia el ID según sea necesario
