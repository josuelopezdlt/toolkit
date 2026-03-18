from datetime import datetime
from perseo_extractor import extraer_ventas, guardar_excel

MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}


def pedir_entero(mensaje: str, minimo: int, maximo: int) -> int:
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"  Valor entre {minimo} y {maximo}.")
        except ValueError:
            print("  Solo números enteros.")


def main():
    hoy = datetime.today()
    print("=" * 45)
    print("   EXTRACTOR PERSEO — CONSULTA POR PERIODO")
    print("=" * 45)

    anio = pedir_entero(f"Año  [{hoy.year}]: ", 2000, 2100)
    mes  = pedir_entero("Mes  (1-12): ", 1, 12)

    print(f"\nConsultando {MESES[mes]} {anio} directamente en Perseo...")
    print("-" * 45)

    try:
        df = extraer_ventas(mes=mes, anio=anio)

        if df.is_empty():
            print(f"ℹ Sin registros para {MESES[mes]} {anio}.")
            return

        ruta = guardar_excel(df, mes=mes, anio=anio)
        print(f"✔ {len(df)} registros extraídos.")
        print(f"   Guardado en: {ruta}")

    except Exception as e:
        print(f"✖ Error: {e}")


if __name__ == "__main__":
    main()
