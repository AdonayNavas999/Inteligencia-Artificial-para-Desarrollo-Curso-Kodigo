# Cálculo de agregados y resumen de métricas

from typing import List, Dict


def calculate_metrics(valid_transactions: List[dict], invalid_transactions: List[dict]) -> dict:
    """Calcula totales procesados, estado de ejecuciones y sumas acumuladas por moneda"""
    total_valid = len(valid_transactions)
    total_invalid = len(invalid_transactions)
    total_processed = total_valid + total_invalid

    status_counts = {
        "SUCCESS": 0,
        "FAILED": 0,
        "PENDING": 0
    }

    currency_totals = {}

    for tx in valid_transactions:
        # Conteo por estado
        st = tx.get("status")
        if st in status_counts:
            status_counts[st] += 1
        else:
            status_counts[st] = 1

        # Acumulado de montos por moneda en transacciones válidas
        curr = tx.get("currency", "UNKNOWN")
        amt = tx.get("amount", 0.0)
        currency_totals[curr] = round(currency_totals.get(curr, 0.0) + amt, 2)

    return {
        "total_processed": total_processed,
        "total_valid": total_valid,
        "total_invalid": total_invalid,
        "status_counts": status_counts,
        "currency_totals": currency_totals
    }
