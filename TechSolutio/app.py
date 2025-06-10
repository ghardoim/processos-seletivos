from flask import Flask, request, jsonify
from pydantic import ValidationError
from src.models import Chat
from redis import Redis
from os import getenv

app = Flask(__name__)

from dotenv import load_dotenv
load_dotenv()

redis_client = Redis.from_url(getenv("REDIS_URL"))

@app.route("/history", methods=["GET"])
def history():
    items = redis_client.lrange(getenv("QUEUE_NAME"), -10, -1)

    history = []
    for item in items:
        answer = redis_client.get(question := item.decode())
        answer = answer.decode() if answer else ""

        history.append({"pergunta": question, "resposta": answer})
    return jsonify({"history": history})

@app.route("/send-message", methods=["POST"])
def send_message():
    try:
        data = Chat(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    redis_client.rpush(getenv("QUEUE_NAME"), data.message)
    while True:
        if answer := redis_client.get(data.message):
            answer = answer.decode()
            break

    return jsonify({"ia": answer, "message": data.message})

if __name__ == "__main__":
    app.run(debug=True)
