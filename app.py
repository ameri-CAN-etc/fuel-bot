import os
import requests
from flask import Flask, request

app = Flask(__name__)

# 🔑 TOKEN из Render
TOKEN = os.environ.get("TOKEN")

VK_API_VERSION = "5.131"


# 📤 отправка сообщения через VK API (СТАБИЛЬНО)
def send(peer_id, text):
    if not TOKEN:
        print("NO TOKEN")
        return

    requests.post(
        "https://api.vk.com/method/messages.send",
        data={
            "peer_id": peer_id,
            "message": text,
            "random_id": 0,
            "access_token": TOKEN,
            "v": VK_API_VERSION
        }
    )


# 🌐 webhook VK
@app.route("/", methods=["POST"])
def main():
    data = request.json

    if not data:
        return "ok"

    # 🔑 подтверждение сервера VK
    if data.get("type") == "confirmation":
        return "ca69504a"

    # 💬 входящее сообщение
    if data.get("type") == "message_new":
        obj = data["object"]["message"]
        text = obj.get("text", "").lower()
        peer_id = obj.get("peer_id")

        if text in ["начать", "start"]:
            send(peer_id, "⛽ Топливо Радар запущен")

        elif text == "📍 азс":
            send(peer_id, "⛽ Список АЗС пока в разработке")

        elif text == "✏️ сообщить":
            send(peer_id, "Напишите: АЗС + топливо + статус")

        else:
            send(peer_id, "Команда не распознана")

    return "ok"


# 🚀 запуск сервера Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
