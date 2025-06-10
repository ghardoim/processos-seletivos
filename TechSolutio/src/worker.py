from src.agent import ask_ai
from redis import Redis
from os import getenv

from dotenv import load_dotenv
load_dotenv()

redis_client = Redis.from_url(getenv("REDIS_URL"))
print("[Worker] Iniciando processamento de mensagens...")

while True:
    _, msg_json = redis_client.blpop(getenv("QUEUE_NAME"))
    question = msg_json.decode()

    print(f"[Worker] Processando mensagem")
    answer = ask_ai(question)
    
    redis_client.set(question, answer)
    print(f"[Worker] Salvando resposta")