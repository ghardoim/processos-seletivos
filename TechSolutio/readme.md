# Microserviço IA - TechSolutio

## Executando com Docker Compose

1. Configure o arquivo `.env` com as variáveis:
   - `REDIS_URL=www.redis.com`
   - `QUEUE_NAME=mensagens`
   - `GOOGLE_API_KEY=...` (sua chave Gemini)

2. Suba os serviços:
```bash
docker compose -f docker/docker-compose.yml up --build
```

## Exemplos de uso

Enviar mensagem:
```bash
curl -X POST http://localhost:8000/send-message \
  -H "Content-Type: application/json" \
  -d '{"to": "+5511999999999", "message": "Quero saber sobre meus débitos"}'
```

Ver histórico:
```bash
curl http://localhost:8000/history
```

## Observações
- O histórico mostra as últimas 10 interações (pergunta e resposta).
- O worker é iniciado automaticamente pelo Docker Compose.
- O serviço utiliza LangChain + Gemini para respostas IA.
