
Pipeline em Python/Spark que lê o Excel de eventos, valida, grava RAW, faz merge incremental em Delta (Stage), produz camada Analytics, cria crawler Glue e valida via Athena.

## Requisitos
- Python 3.10+
- Java/Spark 3.x com Delta Lake
- AWS credentials com acesso a S3/Glue/Athena
- Variáveis de ambiente:
  - `S3_BUCKET=bkt-dev1-data-avaliacoes`
  - `AWS_REGION=sa-east-1`
  - `AWS_ACCESS_KEY_ID=<sua_access_key>`
  - `AWS_SECRET_ACCESS_KEY=<sua_secret_key>`
  - `USER_PREFIX=<nome_sobrenome>`
  - `GLUE_CRAWLER_ROLE=<arn_ou_nome_da_role>`

## Execução do pipeline

```bash
docker-compose up
```