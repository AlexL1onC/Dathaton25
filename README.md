# Datathon Hey Banco 2025

Este repositorio contiene el proyecto desarrollado para el Datathon Hey Banco 2025, cuyo objetivo fue identificar y predecir gastos recurrentes de los usuarios a partir de datos históricos de consumo. La finalidad es ayudar a los usuarios a anticipar sus gastos mensuales y fomentar el ahorro inteligente.

## Objetivo del Proyecto

Diseñar una herramienta de predicción de gastos y visualización financiera que permita a Hey Banco ofrecer recomendaciones personalizadas de ahorro a sus clientes.

## Tecnologías y Herramientas Utilizadas

- Python
  - Pandas, NumPy, Matplotlib, Seaborn
  - Scikit-learn, XGBoost
  - Statsmodels, TensorFlow (LSTM)
- Streamlit
  - Para la construcción de una página web interactiva
- Jupyter Notebooks
  - Análisis exploratorio de datos (EDA)
  - Modelado y evaluación

## Modelos Entrenados

| Modelo                         | Descripción                           | RMSE    |
|-------------------------------|----------------------------------------|---------|
| ARIMA (3,0,0)                 | Modelo autorregresivo clásico          | 20.77   |
| SARIMA (3,0,0)(1,0,1,12)      | Captura estacionalidad mensual         | 21.54   |
| ARCH (1)                      | Modela volatilidad en residuos         | 23.73   |
| XGBoost                       | Árboles de decisión optimizados        | 19.50   |
| LSTM (64 unidades)            | Red neuronal recurrente profunda       | 16.83   |

> El modelo con mejor desempeño fue LSTM, entrenado con una capa de 64 unidades y optimizador Adam.

## Aplicación Web

La aplicación desarrollada con Streamlit permite:

- Visualizar patrones de consumo
- Detectar y listar gastos recurrentes
- Estimar ahorro mensual y anual con base en recomendaciones
- Mostrar resultados por usuario

  ## Integrantes
  //Pedro Soto Juárez
  //Erick Isaac Lascan Otañez
  //Jesús Daniel Guzmán Valenzuela
  //Alexei Carrillo Acosta
