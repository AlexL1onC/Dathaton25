
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joblib
from tensorflow.keras.models import load_model

data = pd.read_csv('df_merged_clean.csv')

data['fecha'] = pd.to_datetime(data['fecha'])

timesteps = 5

# Función para crear secuencias
def crear_secuencias(X, y, timesteps):
    X_seqs, y_seqs = [], []
    for i in range(len(X) - timesteps):
        X_seqs.append(X[i:i+timesteps])
        y_seqs.append(y[i+timesteps])
    return np.array(X_seqs), np.array(y_seqs)

# Filtrar Usuario 1 y preparar datos
usuario_1 = data[data['id'] == 'Usuario 1'].copy()
usuario_1 = usuario_1.sort_values(by='fecha')
usuario_1.set_index('fecha', inplace=True)
serie = usuario_1['monto']

# Crear función para ventanas temporales
def crear_ventanas(serie, n_lags=5):
    df = pd.DataFrame()
    for i in range(n_lags):
        df[f'lag_{i+1}'] = serie.shift(i+1)
    df['target'] = serie.values
    df.dropna(inplace=True)
    return df

# Crear dataset supervisado
n_lags = 3
datos = crear_ventanas(serie, n_lags)

# Fechas límites para split
fecha_fin = datos.index.max()
fecha_validacion_inicio = fecha_fin - pd.DateOffset(months=1)
fecha_entrenamiento_inicio = fecha_fin - pd.DateOffset(months=5)

# Filtrar conjunto de entrenamiento y validación
datos_filtrados = datos[(datos.index >= fecha_entrenamiento_inicio)]

entrenamiento = datos_filtrados[datos_filtrados.index < fecha_validacion_inicio]
validacion = datos_filtrados[datos_filtrados.index >= fecha_validacion_inicio]

# Separar variables
X_train, y_train = entrenamiento.drop('target', axis=1).values, entrenamiento['target'].values
X_test, y_test = validacion.drop('target', axis=1).values, validacion['target'].values



def predecir_usuario_adelante(data, usuario_id, modelo, scaler, n_lags, timesteps, pasos_a_predecir):
    """
    Realiza predicciones hacia adelante para un usuario específico con un modelo ya entrenado.
    
    Parámetros:
    - data: DataFrame completo con columnas 'id', 'fecha', 'monto'.
    - usuario_id: id del usuario a predecir (string).
    - modelo: modelo Keras LSTM ya entrenado.
    - scaler: StandardScaler ya ajustado con los datos de entrenamiento.
    - n_lags: número de lags usados para crear el dataset supervisado.
    - timesteps: número de timesteps para las secuencias LSTM.
    - pasos_a_predecir: número de pasos (días) a predecir hacia adelante.
    
    Retorna:
    - lista con las predicciones hacia adelante (escaladas).
    """
    # 1. Filtrar y preparar serie para el usuario
    usuario = data[data['id'] == usuario_id].copy()
    usuario = usuario.sort_values(by='fecha')
    usuario.set_index('fecha', inplace=True)
    usuario.index = pd.to_datetime(usuario.index)
    serie = usuario['monto']

    # 2. Crear dataset supervisado
    datos_usuario = crear_ventanas(serie, n_lags)

    # 3. Definir fechas para validar
    fecha_fin = datos_usuario.index.max()
    fecha_validacion_inicio = fecha_fin - pd.DateOffset(months=1)
    fecha_entrenamiento_inicio = fecha_fin - pd.DateOffset(months=5)

    datos_filtrados = datos_usuario[(datos_usuario.index >= fecha_entrenamiento_inicio)]
    validacion = datos_filtrados[datos_filtrados.index >= fecha_validacion_inicio]

    X_test, y_test = validacion.drop('target', axis=1).values, validacion['target'].values

    # 4. Escalar (usar scaler ya ajustado)
    X_test_scaled = scaler.transform(X_test)

    # 5. Crear secuencias
    X_test_seq, y_test_seq = crear_secuencias(X_test_scaled, y_test, timesteps)
    if X_test_seq.ndim == 2:
        X_test_seq = np.expand_dims(X_test_seq, -1)

    # 6. Predicciones hacia adelante
    ultima_secuencia_real = X_test_seq[-1].copy()
    predicciones_futuras = []
    secuencia_actual = ultima_secuencia_real.copy()

    for _ in range(pasos_a_predecir):
        prediccion = modelo.predict(secuencia_actual[np.newaxis, :, :])[0, 0]
        predicciones_futuras.append(prediccion)
        nueva_secuencia = np.roll(secuencia_actual, shift=-1, axis=0)
        nueva_secuencia[-1, 0] = prediccion
        secuencia_actual = nueva_secuencia

    return predicciones_futuras



