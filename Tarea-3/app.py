# Aplicación interactiva con Streamlit para exploración de transacciones

import json
import os
import streamlit as st
import pandas as pd

from normalizer import detect_and_normalize
from validator import process_and_segregate_transactions
from metrics import calculate_metrics

# Configuración inicial de la página
st.set_page_config(
    page_title="Normalización de Transacciones",
    layout="wide"
)

st.title("Normalización y Exploración de Transacciones Multifuente")

# Carga por defecto del archivo de prueba o subida de archivo personal
default_path = os.path.join(os.path.dirname(__file__), "input_data.json")
raw_data = None

uploaded_file = st.sidebar.file_uploader("Cargar archivo JSON", type=["json"])

if uploaded_file is not None:
    try:
        raw_data = json.load(uploaded_file)
    except Exception as e:
        st.sidebar.error(f"Error al leer JSON: {e}")
elif os.path.exists(default_path):
    with open(default_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

if raw_data:
    # Procesar y separar transacciones según reglas de negocio
    valid_txs, invalid_txs = process_and_segregate_transactions(raw_data, detect_and_normalize)
    metrics = calculate_metrics(valid_txs, invalid_txs)

    # 1. Resumen de métricas principales
    st.subheader("Métricas Principales")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.metric("Procesadas", metrics["total_processed"])
    col2.metric("Válidas", metrics["total_valid"])
    col3.metric("Inválidas", metrics["total_invalid"])
    col4.metric("Exitosas", metrics["status_counts"].get("SUCCESS", 0))
    col5.metric("Fallidas", metrics["status_counts"].get("FAILED", 0))

    # Totales acumulados por moneda
    if metrics["currency_totals"]:
        st.markdown("##### Totales Acumulados por Moneda")
        curr_cols = st.columns(max(len(metrics["currency_totals"]), 1))
        for idx, (curr, total) in enumerate(metrics["currency_totals"].items()):
            curr_cols[idx].metric(f"Total {curr}", f"{total:,.2f} {curr}")

    st.markdown("---")

    # 2. Filtros laterales de exploración
    st.sidebar.header("Filtros de Exploración")

    ALL_SOURCES = ["Fuente_A", "Fuente_B", "Fuente_C", "Desconocida"]
    ALL_STATUSES = ["SUCCESS", "FAILED", "PENDING"]
    ALL_CURRENCIES = ["USD", "EUR", "GBP"]

    selected_sources = st.sidebar.multiselect("Filtrar por Fuente", options=ALL_SOURCES, default=ALL_SOURCES)
    selected_statuses = st.sidebar.multiselect("Filtrar por Estado", options=ALL_STATUSES, default=ALL_STATUSES)
    selected_currencies = st.sidebar.multiselect("Filtrar por Moneda", options=ALL_CURRENCIES, default=ALL_CURRENCIES)

    # Filtrar transacciones válidas
    filtered_valid = [
        tx for tx in valid_txs
        if tx.get("source") in selected_sources
        and tx.get("status") in selected_statuses
        and tx.get("currency") in selected_currencies
    ]

    # Filtrar registros inválidos
    filtered_invalid = [
        tx for tx in invalid_txs
        if tx.get("source") in selected_sources
        and tx.get("status") in selected_statuses
        and (not tx.get("currency") or tx.get("currency") in selected_currencies or "Moneda" in tx.get("error_reason", ""))
    ]

    # Mapeo de nombres de columnas al español para la interfaz gráfica
    COLUMN_RENAMES = {
        "id": "ID",
        "amount": "Monto",
        "currency": "Moneda",
        "timestamp": "Fecha (ISO)",
        "status": "Estado",
        "source": "Fuente",
        "error_reason": "Motivo de Error"
    }

    # 3. Vista única de tablas dentro de la sección "Transacciones"
    st.subheader("Transacciones")

    # Mostrar tabla de transacciones válidas
    if filtered_valid:
        df_valid = pd.DataFrame(filtered_valid)
        cols_order = ["id", "amount", "currency", "timestamp", "status", "source"]
        df_valid = df_valid[[c for c in cols_order if c in df_valid.columns]]
        df_valid = df_valid.rename(columns=COLUMN_RENAMES)
        st.dataframe(df_valid, use_container_width=True)
    else:
        st.info("No hay transacciones válidas para los filtros seleccionados.")

    # Línea divisoria y sección de registros inválidos en la misma vista
    if filtered_invalid:
        st.markdown("---")
        st.subheader("Registros Inválidos")
        df_invalid = pd.DataFrame(filtered_invalid)
        cols_inv = ["id", "error_reason", "amount", "currency", "timestamp", "status", "source"]
        df_invalid = df_invalid[[c for c in cols_inv if c in df_invalid.columns]]
        df_invalid = df_invalid.rename(columns=COLUMN_RENAMES)
        st.dataframe(df_invalid, use_container_width=True)

else:
    st.warning("No se encontraron datos para procesar.")
