import pandas as pd
def probabilidad_consumo_en_dia(df, dia_objetivo, usuario):

    # Asegurar que la fecha sea tipo datetime
    df['fecha'] = pd.to_datetime(df['fecha'])

    # Agregar columna con día del mes
    df['dia_mes'] = df['fecha'].dt.day

    # Filtrar datos del usuario
    df_usuario = df[df['id'] == usuario].copy()

    if df_usuario.empty:
        return {
            'error': f"No hay datos para el usuario {usuario}."
        }

    # Paso 1: obtener comercio de mayor consumo del usuario (por monto)
    total_por_comercio = df_usuario.groupby('comercio')['monto'].sum().reset_index()
    comercio_top = total_por_comercio.sort_values('monto', ascending=False).head(1)['comercio'].values[0]

    # Filtrar el DataFrame del usuario para conservar solo su comercio top
    df_top = df_usuario[df_usuario['comercio'] == comercio_top]

    # Paso 2: calcular la probabilidad de consumo en el día objetivo
    total_consumos = len(df_top)
    consumos_en_dia = (df_top['dia_mes'] == dia_objetivo).sum()

    probabilidad = (consumos_en_dia / total_consumos) * 100 if total_consumos > 0 else 0

    # Paso 3: predecir el comercio más probable en ek día n 
    dia_siguiente = dia_objetivo   
    df_dia_siguiente = df_usuario[df_usuario['dia_mes'] == dia_siguiente]

    comercio_mas_probable = (
        df_dia_siguiente['comercio'].value_counts().idxmax()
        if not df_dia_siguiente.empty else 'No hay datos'
    )

    return {
        'usuario': usuario,
        'probabilidad_consumo_en_dia': round(probabilidad, 2),
        'comercio_top_usuario': comercio_top,
        'prediccion_dia_siguiente': {
            'dia': dia_siguiente,
            'comercio_mas_probable': comercio_mas_probable
        },
        'comercios_frecuentes': df_usuario['comercio'].value_counts().reset_index().rename(columns={'index': 'comercio', 'comercio': 'frecuencia'})
    }
