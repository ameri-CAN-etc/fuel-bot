import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN")
VK_API = "https://api.vk.com/method/messages.send"
VK_VERSION = "5.131"

# 🧠 защита от дублей (простая in-memory)
seen = set()


# 📤 отправка сообщений
def send(peer_id, text):
    if not TOKEN:
        print("TOKEN NOT FOUND")
        return

    requests.post(
        VK_API,
        data={
            "peer_id": peer_id,
            "message": text,
            "random_id": 0,
            "access_token": TOKEN,
            "v": VK_VERSION
        }
    )


# 🌐 VK webhook
@app.route("/", methods=["POST"])
def main():
    data = request.json

    if not data:
        return "ok"

    # 🔑 подтверждение сервера
    if data.get("type") == "confirmation":
        return "ca69504a"

    if data.get("type") == "message_new":
        msg_id = data["object"]["message"]["id"]

        # 🧠 защита от повторов
        if msg_id in seen:
            return "ok"
        seen.add(msg_id)

        msg = data["object"]["message"]["text"].lower()
        peer_id = data["object"]["message"]["peer_id"]

        if msg in ["начать", "start"]:
            send(peer_id, "⛽ Топливо Радар запущен")

        elif msg == "📍 азс":
            send(peer_id, "⛽ АЗС список пока формируется")

        elif msg == "✏️ сообщить":
            send(peer_id, "Напишите: АЗС + топливо + статус")

        else:
            send(peer_id, "Команда не распознана")

    return "ok"


# 🚀 запуск (Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
