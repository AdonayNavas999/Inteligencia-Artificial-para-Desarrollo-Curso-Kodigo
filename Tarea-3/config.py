# Configuración de mapeos, reglas y constantes globales del sistema

# Mapeo normalizado de estados heterogéneos
STATUS_MAPPING = {
    "completed": "SUCCESS",
    "ok": "SUCCESS",
    "success": "SUCCESS",
    "completado": "SUCCESS",
    "failed": "FAILED",
    "error": "FAILED",
    "rejected": "FAILED",
    "fallido": "FAILED",
    "pending": "PENDING",
    "processing": "PENDING",
    "pendiente": "PENDING"
}

# Formatos de fecha soportados para parsear a ISO-8601
DATE_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%d/%m/%Y %H:%M",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%d"
]

# Lista blanca de monedas válidas
SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP"]
