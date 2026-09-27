import re

# Regex estricto
REGEX_LOG = r"^\[(INFO|WARNING|ERROR)\]\s+(\d{4}-\d{2}-\d{2})\s+(.*)$"

def parsear_linea(linea):
    """
    Analiza una línea individual del archivo de log.
    Devuelve:
        tuple: (nivel, fecha, mensaje) si la línea es válida.
        None: si la línea está mal formateada o es inválida.
    """
    linea = linea.strip()
    coincidencia = re.match(REGEX_LOG, linea)
    
    if coincidencia:
        return coincidencia.groups() # (nivel, fecha, mensaje)
    return None

def analizar_archivo_logs(ruta_archivo):
    """
    Lee el archivo de logs línea por línea y recopila estadísticas.
    """
    conteo_niveles = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0
    }
    lineas_invalidas = 0
    total_lineas = 0

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                # Omitir líneas completamente vacías si existen
                if not linea.strip():
                    continue
                
                total_lineas += 1
                resultado = parsear_linea(linea)
                
                if resultado:
                    nivel, fecha, mensaje = resultado
                    if nivel in conteo_niveles:
                        conteo_niveles[nivel] += 1
                else:
                    lineas_invalidas += 1

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta '{ruta_archivo}'")
        return None

    return {
        "total": total_lineas,
        "niveles": conteo_niveles,
        "invalidas": lineas_invalidas
    }

def imprimir_resumen(estadisticas):
    """
    Imprime en consola los resultados en un formato claro y limpio.
    """
    if not estadisticas:
        return

    print("=" * 40)
    print("      RESUMEN DEL ANÁLISIS DE LOGS      ")
    print("=" * 40)
    print(f"Total de eventos procesados : {estadisticas['total']}")
    print("-" * 40)
    print("Detalle por nivel de evento:")
    print(f"  - INFO    : {estadisticas['niveles']['INFO']}")
    print(f"  - WARNING : {estadisticas['niveles']['WARNING']}")
    print(f"  - ERROR   : {estadisticas['niveles']['ERROR']}")
    print("-" * 40)
    print(f"Líneas mal formateadas     : {estadisticas['invalidas']}")
    print("=" * 40)

def main():
    ruta = "logs_con_errores.txt"
    estadisticas = analizar_archivo_logs(ruta)
    imprimir_resumen(estadisticas)

if __name__ == "__main__":
    main()
