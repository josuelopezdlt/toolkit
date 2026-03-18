"""
Ejecutar UNA VEZ para descubrir las tablas y columnas de Perseo.
Resultado se guarda en output/schema.txt para referencia.
"""
import os
import pyodbc
from db import get_connection, listar_tablas

OUTPUT = os.path.join(os.path.dirname(__file__), "output", "schema.txt")
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)


def explorar():
    print("Conectando a HFSQL...")
    try:
        conn = get_connection()
        print("✔ Conexión exitosa.\n")
    except Exception as e:
        print(f"✖ Error de conexión: {e}")
        print("\nVerifica que el driver HFSQL ODBC esté instalado:")
        print("  https://pcsoft.fr/st/telchargements/hfsql-client.html")
        return

    cursor = conn.cursor()
    tablas = listar_tablas()

    print(f"Tablas encontradas: {len(tablas)}\n")
    lineas = []

    for tabla in sorted(tablas):
        lineas.append(f"\n[{tabla}]")
        print(f"  {tabla}")
        try:
            cols = cursor.columns(table=tabla)
            for col in cols:
                linea = f"    {col.column_name} ({col.type_name})"
                lineas.append(linea)
        except Exception:
            lineas.append("    (error al leer columnas)")

    conn.close()

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print(f"\n✔ Schema completo guardado en: {OUTPUT}")


if __name__ == "__main__":
    explorar()
