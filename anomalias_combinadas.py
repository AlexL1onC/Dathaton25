
from sklearn.ensemble import IsolationForest
import pandas as pd

def detectar_anomalias_combinadas(data, usuario_id, contamination=0.05, z_umbral=3):
    data = data.copy()
    data['fecha'] = pd.to_datetime(data['fecha'])
    usuario_data = data[data['id'] == usuario_id].sort_values(by='fecha')
    usuario_data.set_index('fecha', inplace=True)

    if len(usuario_data) < 20:
        return None, None

    fecha_fin = usuario_data.index.max()
    fecha_validacion_inicio = fecha_fin - pd.Timedelta(days=30)
    fecha_entrenamiento_inicio = fecha_validacion_inicio - pd.Timedelta(days=180)

    entrenamiento = usuario_data[(usuario_data.index >= fecha_entrenamiento_inicio) &
                                 (usuario_data.index < fecha_validacion_inicio)].copy()
    validacion = usuario_data[usuario_data.index >= fecha_validacion_inicio].copy()

    if len(entrenamiento) < 10 or len(validacion) < 5:
        return None, None

    # Estadísticas del entrenamiento
    mu = entrenamiento['monto'].mean()
    sigma = entrenamiento['monto'].std()

    # Isolation Forest
    modelo = IsolationForest(n_estimators=100, contamination=contamination, random_state=42)
    modelo.fit(entrenamiento[['monto']])
    validacion['anomaly_iforest'] = modelo.predict(validacion[['monto']])
    validacion['score_iforest'] = modelo.decision_function(validacion[['monto']])

    # Z-score y filtro de anomalías hacia arriba
    validacion['z_score'] = (validacion['monto'] - mu) / sigma
    validacion['anomaly_z'] = validacion['z_score'].apply(lambda z: -1 if z > z_umbral else 1)

    # Anomalía total si monto es alto y algún detector la marca
    validacion['anomaly_total'] = validacion.apply(
        lambda row: -1 if (
            row['monto'] > mu and (row['anomaly_iforest'] == -1 or row['anomaly_z'] == -1)
        ) else 1,
        axis=1
    )

    # Extraer solo anomalías
    anomalías = validacion[validacion['anomaly_total'] == -1]
    fechas_anomalas = anomalías.index.to_list()
    montos_anomalos = anomalías['monto'].to_list()

    return fechas_anomalas, montos_anomalos