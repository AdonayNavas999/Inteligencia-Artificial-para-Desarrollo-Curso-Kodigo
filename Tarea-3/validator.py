# Reglas de validación de negocio y segregación de registros

from typing import List, Dict, Tuple
from datetime import datetime
from config import SUPPORTED_CURRENCIES

VALID_STATUSES = {"SUCCESS", "FAILED", "PENDING"}


def validate_transaction(record: dict) -> Tuple[bool, str]:
    """Evalúa un registro según las 5 reglas de negocio requeridas"""
    # 1. ID no vacío
    record_id = record.get("id")
    if not record_id or not str(record_id).strip():
        return False, "ID de transacción nulo o vacío"

    # 2. Monto positivo (> 0)
    amount = record.get("amount")
    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        return False, f"Monto no numérico ({amount})"
    if amount <= 0:
        return False, f"Monto debe ser mayor que 0 (Valor actual: {amount})"

    # 3. Moneda soportada (USD, EUR, GBP)
    currency = record.get("currency")
    if not currency or currency not in SUPPORTED_CURRENCIES:
        return False, f"Moneda no soportada '{currency}'"

    # 4. Formato de fecha ISO-8601
    timestamp = record.get("timestamp")
    if not timestamp or not isinstance(timestamp, str):
        return False, "Timestamp ausente o no válido"
    try:
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return False, f"Fecha no cumple con formato ISO-8601 ('{timestamp}')"

    # 5. Estado permitido (SUCCESS, FAILED, PENDING)
    status = record.get("status")
    if not status or status not in VALID_STATUSES:
        return False, f"Estado no permitido '{status}'"

    return True, ""


def process_and_segregate_transactions(raw_records: List[dict], normalize_func) -> Tuple[List[dict], List[dict]]:
    """Normaliza y separa registros en listas de válidos e inválidos"""
    validas = []
    invalidas = []

    for raw in raw_records:
        norm = normalize_func(raw)
        is_valid, reason = validate_transaction(norm)
        if is_valid:
            validas.append(norm)
        else:
            norm_with_error = dict(norm)
            norm_with_error["error_reason"] = reason
            norm_with_error["raw_record"] = raw
            invalidas.append(norm_with_error)

    return validas, invalidas
