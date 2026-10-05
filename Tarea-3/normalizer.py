# Detección de origen y estandarización al esquema unificado

import re
from datetime import datetime
from config import STATUS_MAPPING, DATE_FORMATS


def parse_timestamp(date_raw: str) -> str:
    """Convierte cadenas de fecha a formato ISO-8601 (YYYY-MM-DDTHH:MM:SS)"""
    if not isinstance(date_raw, str):
        return str(date_raw) if date_raw is not None else ""
        
    date_clean = date_raw.strip()
    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(date_clean, fmt)
            return dt.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            continue
    return date_clean


def detect_and_normalize(raw_record: dict) -> dict:
    """Detecta dinámicamente la fuente (A, B, C) y mapea los datos al esquema estándar"""
    normalized = {
        "id": "",
        "amount": 0.0,
        "currency": "",
        "timestamp": "",
        "status": "",
        "source": "Desconocida"
    }

    # Fuente 1: id, amount ("100.50"), currency, timestamp, status
    if "id" in raw_record and "amount" in raw_record and "timestamp" in raw_record:
        normalized["source"] = "Fuente_A"
        normalized["id"] = str(raw_record.get("id", "")).strip()
        
        try:
            normalized["amount"] = float(raw_record.get("amount", 0))
        except (ValueError, TypeError):
            normalized["amount"] = raw_record.get("amount")

        curr = raw_record.get("currency", "")
        normalized["currency"] = str(curr).upper().strip() if curr else ""
        normalized["timestamp"] = parse_timestamp(str(raw_record.get("timestamp", "")))
        status_raw = str(raw_record.get("status", "")).lower().strip()
        normalized["status"] = STATUS_MAPPING.get(status_raw, status_raw.upper())

    # Fuente 2: transaction_id, total en centavos (25000 -> 250.00), currency_code, created_at, state
    elif "transaction_id" in raw_record and "total" in raw_record and "created_at" in raw_record:
        normalized["source"] = "Fuente_B"
        normalized["id"] = str(raw_record.get("transaction_id", "")).strip()

        try:
            total_val = raw_record.get("total")
            normalized["amount"] = round(float(total_val) / 100.0, 2)
        except (ValueError, TypeError):
            normalized["amount"] = raw_record.get("total")

        curr = raw_record.get("currency_code", "")
        normalized["currency"] = str(curr).upper().strip() if curr else ""
        normalized["timestamp"] = parse_timestamp(str(raw_record.get("created_at", "")))
        state_raw = str(raw_record.get("state", "")).lower().strip()
        normalized["status"] = STATUS_MAPPING.get(state_raw, state_raw.upper())

    # Fuente 3: ref, amount con símbolo ("€99,99"), date, result
    elif "ref" in raw_record and "date" in raw_record and "result" in raw_record:
        normalized["source"] = "Fuente_C"
        normalized["id"] = str(raw_record.get("ref", "")).strip()

        amount_raw = str(raw_record.get("amount", "")).strip()
        extracted_curr = ""
        if "€" in amount_raw:
            extracted_curr = "EUR"
        elif "$" in amount_raw:
            extracted_curr = "USD"
        elif "£" in amount_raw:
            extracted_curr = "GBP"

        normalized["currency"] = extracted_curr or str(raw_record.get("currency", "")).upper().strip()
        clean_amount_str = re.sub(r"[^\d,\.-]", "", amount_raw).replace(",", ".")
        try:
            normalized["amount"] = float(clean_amount_str)
        except (ValueError, TypeError):
            normalized["amount"] = amount_raw

        normalized["timestamp"] = parse_timestamp(str(raw_record.get("date", "")))
        result_raw = str(raw_record.get("result", "")).lower().strip()
        normalized["status"] = STATUS_MAPPING.get(result_raw, result_raw.upper())

    # Estructura no identificada
    else:
        normalized["id"] = str(raw_record.get("id") or raw_record.get("transaction_id") or raw_record.get("ref") or "").strip()
        normalized["source"] = "Desconocida"
        normalized["amount"] = raw_record.get("amount") or raw_record.get("total")
        normalized["currency"] = str(raw_record.get("currency") or raw_record.get("currency_code") or "").upper().strip()
        raw_date = raw_record.get("timestamp") or raw_record.get("created_at") or raw_record.get("date") or ""
        normalized["timestamp"] = parse_timestamp(str(raw_date))
        raw_st = str(raw_record.get("status") or raw_record.get("state") or raw_record.get("result") or "").lower().strip()
        normalized["status"] = STATUS_MAPPING.get(raw_st, raw_st.upper())

    return normalized
