"""
Extractor de ventas Perseo via HFSQL ODBC.
Puede usarse directo o importarse en un pipeline Polars/n8n.
"""
import polars as pl
import os
from datetime import datetime
from db import get_connection

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Ajustar estos valores según lo que devuelva explorar_schema.py
TABLA_VENTAS = "FACTURAS"       # nombre real de la tabla (confirmar con explorar_schema.py)
COLUMNA_FECHA = "EMISION"       # columna de fecha


def extraer_ventas(mes: int, anio: int) -> pl.DataFrame:
    fecha_inicio = f"{anio}-{mes:02d}-01"
    if mes == 12:
        fecha_fin = f"{anio + 1}-01-01"
    else:
        fecha_fin = f"{anio}-{mes + 1:02d}-01"

    query = f"""
        SELECT *
        FROM {TABLA_VENTAS}
        WHERE {COLUMNA_FECHA} >= '{fecha_inicio}'
          AND {COLUMNA_FECHA} <  '{fecha_fin}'
    """

    with get_connection() as conn:
        df = pl.read_database(query, conn)

    return df


def guardar_excel(df: pl.DataFrame, mes: int, anio: int):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    nombre_mes = datetime(anio, mes, 1).strftime("%B_%Y").upper()
    ruta = os.path.join(OUTPUT_DIR, f"PERSEO_{nombre_mes}.xlsx")
    df.write_excel(ruta)
    return ruta
