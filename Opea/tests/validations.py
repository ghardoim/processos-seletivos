from src.validations import validate_clientes, validate_enderecos
import pandas as pd

def test_validate_clientes_rejects_bad_email_and_cpf():
    df = pd.DataFrame(
        [
            {
                "id_cliente": 1,
                "nome": "Ana",
                "email": "anaexample.com",
                "cpf": "11111111111",
                "data_nascimento": "1990-01-01",
                "status": "ativo",
                "data_evento": "2023-12-01 10:00:00",
            }
        ]
    )
    valid, errors = validate_clientes(df)
    assert valid.empty
    assert any(err["campo"] == "email" for err in errors)
    assert any(err["campo"] == "cpf" for err in errors)

def test_validate_enderecos_checks_referential_integrity_and_formats():
    df = pd.DataFrame(
        [
            {
                "id_endereco": 1,
                "id_cliente": 99,
                "cep": "1234567",
                "logradouro": "Rua A",
                "numero": "100",
                "bairro": "Centro",
                "cidade": "Sao Paulo",
                "estado": "SPO",
                "data_evento": "2023-12-01 10:00:00",
            }
        ]
    )
    valid, errors = validate_enderecos(df, clientes_ids=[1, 2, 3])
    assert valid.empty
    assert any(err["campo"] == "id_cliente" for err in errors)
    assert any(err["campo"] == "cep" for err in errors)
    assert any(err["campo"] == "estado" for err in errors)
