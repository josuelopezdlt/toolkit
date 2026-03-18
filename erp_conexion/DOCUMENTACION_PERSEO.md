# Documentación Técnica: Integración de Datos Perseo ERP
**Empresa:** PLASTICNARANJO S.A.
**Usuario:** JLOPEZ / Josue Lopez

## 1. Infraestructura Detectada
A través del análisis del sistema Perseo Software x64 instalado en la estación `DESKTOP-J66K58O`, se identificó la siguiente infraestructura de red:

| Componente | Detalle | Puerto | Protocolo |
| :--- | :--- | :--- | :--- |
| **Servidor Principal** | 192.168.100.4 | - | - |
| **Base de Datos (HFSQL)** | WinDev HyperFile SQL | 5588 | Binario Propietario |
| **Servidor Web** | Apache 2.4.57 (Win64) | 80 / 443 | HTTP/HTTPS |
| **Middleware API** | WinDev 29 (wd290awws64.dll) | 80 | REST/SOAP |

## 2. Bases de Datos y Estructura
*   **Nombre de la DB Inferred:** `9967231265_db0000000001` (RUC de PlasticNaranjo).
*   **Motor de Base de Datos:** HFSQL (HyperFile SQL) de PC SOFT.
*   **Archivos de configuración:** `C:\ProgramData\Perseo-Soft\Perseo Software\`.

### Columnas Identificadas en Reportes de Ventas
Al descargar el archivo de ventas masivo, estas son las columnas clave que el sistema genera:
- **EMISION:** Fecha de la factura (Columna crítica para filtrado).
- **COMPROBANTE:** Número de factura.
- **CLIENTE:** Nombre o Razón Social del comprador.
- **TOTAL:** Monto final del documento.
*(Y todas las columnas adicionales que el ERP exporta por defecto)*.

## 3. Conectividad y Acceso Masivo
Debido a que el puerto **5588** utiliza un protocolo binario cerrado de WinDev y no es SQL estándar (PostgreSQL/MySQL), la mejor forma de acceso masivo actualmente es la **Exportación de Reportes**.

### Flujo de Trabajo para Descarga Masiva (Actual)
1.  **En Perseo ERP:** Generar el reporte masivo de "Ventas" o "Inventario" en formato Excel.
2.  **En Python:** Ejecutar el script `perseo_extractor_completo.py`.
3.  **Resultado:** Obtendrás un archivo limpio en el Escritorio llamado `PERSEO_MARZO_COMPLETO.xlsx` filtrado por el mes de Marzo y con todas las columnas disponibles.

## 4. Notas de Seguridad
- No compartir la contraseña `j0052*` fuera de entornos seguros.
- Las rutas de API encontradas (`/api/v1/login`) están vivas en el puerto 80 del servidor Apache, pero requieren una estructura de "POST" específica de WinDev para autenticar.

---
*Documentación generada por Gemini CLI - 17 de Marzo de 2026*
