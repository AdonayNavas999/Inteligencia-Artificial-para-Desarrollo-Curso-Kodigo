# Normalización y Exploración de Transacciones Multifuente

Proyecto modular desarrollado en Python y Streamlit para la ingesta, detección dinámica, normalización, validación y exploración visual de transacciones financieras provenientes de fuentes heterogéneas.

---

## 🏗️ Arquitectura del Sistema y Separación de Módulos

El proyecto sigue una arquitectura modular y desacoplada respetando el principio de responsabilidad única (SRP):

- **`config.py`**: Almacena las reglas globales del sistema, como monedas soportadas (`USD`, `EUR`, `GBP`), formatos de fecha para parseo e ISO-8601 y mapeos de equivalencias de estados heterogéneos (`completed`, `ok` -> `SUCCESS`; `failed`, `rejected` -> `FAILED`; `processing`, `pending` -> `PENDING`).
- **`normalizer.py`**: Contiene la lógica de introspección para detectar dinámicamente la fuente de origen (`Fuente_A`, `Fuente_B`, `Fuente_C` o `Desconocida`) y transformar los campos y tipos heterogéneos hacia el esquema unificado.
- **`validator.py`**: Aplica las 5 reglas de negocio de validación y segrega las transacciones en dos colecciones (`validas` e `invalidas`), añadiendo el motivo explícito del rechazo en el campo `error_reason`.
- **`metrics.py`**: Calcula los agregados analíticos requeridos: total procesadas, válidas vs. inválidas, desglose por estado (Exitosas/Fallidas) y totales acumulados por moneda.
- **`app.py`**: Aplicación web desarrollada con **Streamlit** que proporciona la interfaz interactiva con filtros dinámicos por fuente, estado y moneda, métricas principales y visualización unificada en español.

---

## 📐 Decisiones de Diseño y Reglas de Normalización

### 1. Detección Dinámica de Fuentes
- **Fuente A**: Registros con llaves `id`, `amount`, `currency`, `timestamp`, `status`.
- **Fuente B**: Registros con llaves `transaction_id`, `total`, `currency_code`, `created_at`, `state`.
- **Fuente C**: Registros con llaves `ref`, `amount`, `date`, `result`.
- **Desconocida**: Estructuras no reconocidas o corruptas que no coinciden con ninguna firma de las tres fuentes anteriores.

### 2. Conversiones Específicas
- **Montos en Centavos (Fuente B):** Los enteros (ej. `25000`) se convierten a decimales flotantes dividiendo entre `100.0` (`250.00`).
- **Símbolos y Monedas Implícitas (Fuente C):** Parseo de cadenas con símbolos (`"€99,99"` o `"£89.99"`), extrayendo la moneda (`EUR`, `GBP`) y reemplazando comas por puntos para convertir a `float`.
- **Estandarización de Fechas:** Parseo dinámico de múltiples formatos estándar y conversión al formato normado ISO-8601 (`YYYY-MM-DDTHH:MM:SS`).

---

## 🛡️ Política de Manejo de Registros Inválidos

Se aplica una política de **segregación determinista con reporte de causa**:
1. **Preservación:** Ningún registro se elimina silenciosamente.
2. **Segregación:** Los datos conformes nutren las métricas acumuladas; los no conformes son separados.
3. **Auditoría de Rechazo:** Las transacciones no válidas incluyen el campo `error_reason` indicando la falla específica (ej. *ID vacío*, *Monto negativo*, *Moneda no soportada*, *Fecha no ISO-8601*).

---

## 🤖 Registro de Uso de IA y Decisiones Humanas

- **Asistencia de IA:** Generación de la estructura modular base, patrones regex para limpieza de montos y componentes visuales de Streamlit.
- **Decisiones y Ajustes Humanos:**
  - Establecimiento explícito del modelo final de datos y las 5 reglas de validación en `validator.py`.
  - Simplificación de la interfaz a una **sección de vista unificada** con tablas renombradas al español (`ID`, `Monto`, `Moneda`, `Fecha (ISO)`, `Estado`, `Fuente`, `Motivo de Error`).
  - Opciones fijas e invariables en los filtros laterales de Streamlit para posibilitar la exploración de todos los estados y casos borde (incluyendo fuentes `Desconocida`).
  - Documentación técnica limpia, directa y concisa en el código sin comentarios sobre el historial de cambios.

---

## 🚀 Ejecución de la Aplicación

Para instalar dependencias y ejecutar la interfaz web:

```powershell
pip install streamlit pandas
python -m streamlit run app.py
```
