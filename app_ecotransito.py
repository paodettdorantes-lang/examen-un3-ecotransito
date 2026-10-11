# ==========================================================================
# TAREA 4: SCRIPT DE STREAMLIT (app_ecotransito.py)
# ==========================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Configuración de página
st.set_page_config(page_title="Sistema EcoTránsito CDMX", layout="wide")

st.title("Sistema EcoTránsito CDMX")

# Carga de datos base de las tareas anteriores (simulado)
@st.cache_data
def cargar_datos():
    
    data = {
        'ID_Registro': ['REG-001', 'REG-002', 'REG-003', 'REG-004', 'REG-005', 'REG-006', 'REG-007', 'REG-008', 'REG-009', 'REG-010'],
        'Zona_Estacion': ['Centro_Historico', 'Centro_Historico', 'Centro_Historico', 'Zona_Oriente', 'Zona_Oriente', 'Zona_Oriente', 'Zona_Sur', 'Zona_Sur', 'Zona_Sur', 'Zona_Sur'],
        'Concentracion_PM25': [35.4, 42.1, 38.75, 120.5, 76.45, 32.55, 18.2, 20.1, 19.5, 19.5],
        'Nivel_NO2': [42.1, 48.5, 51.0, 89.2, 82.0, 195.0, 22.4, 33.75, 25.1, 25.1],
        'Indice_Trafico_Vehicular': [85.0, 92.5, 88.0, 98.0, 91.2, 15.0, 45.0, 42.1, 43.5, 41.0]
    }
    return pd.DataFrame(data)

df = cargar_datos()

# 2. Carga y filtrado de datos con barra lateral
st.sidebar.header("Filtros de Análisis")
zonas_disponibles = df['Zona_Estacion'].unique()
zonas_seleccionadas = st.sidebar.multiselect(
    "Selecciona las zonas:", 
    options=zonas_disponibles, 
    default=zonas_disponibles
)

# Aplicar filtro de zona al dataframe
df_filtrado = df[df['Zona_Estacion'].isin(zonas_seleccionadas)]

# 3. Métricas principales (KPIs)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Lecturas Activas", value=len(df_filtrado))

with col2:
    pm25_prom = df_filtrado['Concentracion_PM25'].mean() if not df_filtrado.empty else 0
    st.metric(label="Promedio PM₂.₅ (μg/m³)", value=f"{pm25_prom:.2f}")

with col3:
    trafico_max = df_filtrado['Indice_Trafico_Vehicular'].max() if not df_filtrado.empty else 0
    st.metric(label="Máximo Tráfico Vehicular", value=f"{trafico_max:.1f}")

# 4. Pestañas interactivas de visualización (Plotly + Seaborn)
tab1, tab2 = st.tabs(["Dispersión Tráfico vs PM2.5", "Calor de Correlación"])

with tab1:
    st.subheader("Relación entre Tráfico Vehicular y Concentración de PM2.5")
    if not df_filtrado.empty:
        fig = px.scatter(
            df_filtrado, 
            x="Indice_Trafico_Vehicular", 
            y="Concentracion_PM25", 
            color="Zona_Estacion",
            labels={"Indice_Trafico_Vehicular": "Índice de Tráfico", "Concentracion_PM25": "PM2.5 (μg/m³)"}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Selecciona al menos una zona para ver el gráfico.")

with tab2:
    st.subheader("Matriz de Correlación de Variables Numéricas")
    cols_num = ['Concentracion_PM25', 'Nivel_NO2', 'Indice_Trafico_Vehicular']
    
    if not df_filtrado.empty and len(df_filtrado) > 1:
        fig_sns, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(df_filtrado[cols_num].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        st.pyplot(fig_sns)
    else:
        st.warning("Se necesitan más datos filtrados para calcular correlaciones.")


