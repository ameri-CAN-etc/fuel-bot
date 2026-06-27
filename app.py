import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN")
VK_API = "https://api.vk.com/method/messages.send"
VK_VERSION = "5.131"

# 👁️⛽ БензоГлаз заправка
BOT_NAME = "👁️ БензоГлаз ⛽"


# 📤 отправка сообщений
def send(peer_id, text):
    if not TOKEN:
        print("TOKEN NOT FOUND")
        return

    requests.post(
        VK_API,
        data={
            "peer_id": peer_id,
            "message": f"{BOT_NAME}\n{text}",
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

    # 🔑 подтверждение сервера VK
    if data.get("type") == "confirmation":
        return "ca69504a"

    # 💬 сообщения
    if data.get("type") == "message_new":
        obj = data["object"]["message"]

        if not obj:
            return "ok"

        text = obj.get("text", "")
        peer_id = obj.get("peer_id")

        if not text:
            return "ok"

        text = text.lower().strip()

        # 🟢 старт
        if text in ["начать", "start", "бензоглаз"]:
            send(peer_id, "Система активирована")

        # ⛽ АЗС
        elif "азс" in text:
            send(peer_id, "Список АЗС в разработке")

        # ✏️ сообщение
        elif "сообщ" in text:
            send(peer_id, "Напишите: АЗС + топливо + статус")

        # ❗ ничего лишнего НЕ отвечаем
        else:
            return "ok"

    return "ok"


# 🚀 запуск Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
