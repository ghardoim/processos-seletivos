from typing import Dict, Iterable, List, Tuple
from datetime import datetime as dt
from re import compile

import pandas as pd

EMAIL_PATTERN = compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z0-9]+$")
CPF_PATTERN = compile(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")
CEP_PATTERN = compile(r"^\d{5}-\d{3}$")
UF_PATTERN = compile(r"^[A-Z]{2}$")

def _validate_required(value) -> bool:
    return not (pd.isna(value) or (isinstance(value, str) and not value.strip()))

def _validate_date(value: str, fmt: str) -> bool:
    try:
        dt.strptime(str(value), fmt)
        return True
    except Exception:
        return False

def validate_clientes(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[Dict]]:

    required_fields = ["id_cliente", "nome", "email", "cpf", "status", "data_nascimento", "data_evento"]
    errors: List[Dict] = []
    valid_rows = []

    for idx, row in df.iterrows():
        row_errors: List[Dict] = []
        for field in required_fields:
            if not _validate_required(row.get(field)):
                row_errors.append(_error(idx, field, row.get(field), f"campo {field} obrigatório ausente"))

        for field, pattern in zip(required_fields[2:4], (EMAIL_PATTERN, CPF_PATTERN)):
            if not pattern.match(str(row.get(field, ""))):
                row_errors.append(_error(idx, field, row.get(field), f"{field} inválido"))

        if row.get("status") not in {"ativo", "inativo", "suspenso"}:
            row_errors.append(_error(idx, "status", row.get("status"), "status inválido"))

        if not _validate_date(row.get("data_nascimento"), "%Y-%m-%d"):
            row_errors.append(_error(idx, "data_nascimento", row.get("data_nascimento"), "data_nascimento inválida (YYYY-MM-DD)"))
        if not _validate_date(row.get("data_evento"), "%Y-%m-%d %H:%M:%S"):
            row_errors.append(_error(idx, "data_evento", row.get("data_evento"), "data_evento inválido (YYYY-MM-DD HH:MM:SS)"))

        if row_errors:
            errors.extend(row_errors)
        else:
            valid_rows.append(row)

    valid_df = pd.DataFrame(valid_rows) if valid_rows else pd.DataFrame(columns=df.columns)
    return valid_df, errors

def validate_enderecos(df: pd.DataFrame, clientes_ids: Iterable[int]) -> Tuple[pd.DataFrame, List[Dict]]:

    required_fields = ["id_endereco", "id_cliente", "logradouro", "numero", "bairro", "cidade", "data_evento", "cep", "estado"]
    clientes_set = set(clientes_ids)
    errors: List[Dict] = []
    valid_rows = []

    for idx, row in df.iterrows():
        row_errors: List[Dict] = []
        for field in required_fields:
            if not _validate_required(row.get(field)):
                row_errors.append(_error(idx, field, row.get(field), f"campo {field} obrigatório ausente"))

        if row.get("id_cliente") not in clientes_set:
            row_errors.append(_error(idx, "id_cliente", row.get("id_cliente"), "id_cliente não existe em clientes"))

        for field, pattern in zip(required_fields[-2:], (CEP_PATTERN, UF_PATTERN)):
            if not pattern.match(str(row.get(field, ""))):
                row_errors.append(_error(idx, field, row.get(field), f"{field} com formato não esperado."))

        if not _validate_date(row.get("data_evento"), "%Y-%m-%d %H:%M:%S"):
            row_errors.append(_error(idx, "data_evento", row.get("data_evento"), "data_evento inválido (YYYY-MM-DD HH:MM:SS)"))

        if row_errors:
            errors.extend(row_errors)
        else:
            valid_rows.append(row)

    valid_df = pd.DataFrame(valid_rows) if valid_rows else pd.DataFrame(columns=df.columns)
    return valid_df, errors

def _error(idx: int, field: str, value, reason: str) -> Dict:
    return {"linha": idx + 2, "campo": field, "valor": value, "motivo": reason}
