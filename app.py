import os
import requests
from flask import Flask, request

app = Flask(__name__)

# 🔑 VK token (Render env)
TOKEN = os.environ.get("TOKEN")

VK_API = "https://api.vk.com/method/messages.send"
VK_VERSION = "5.131"

# 👁️⛽ бренд
BOT_TAG = "👁️ БензоГлаз ⛽"

# 🧠 защита от дублей (в памяти)
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
            "message": f"{BOT_TAG}\n{text}",
            "random_id": 0,
            "access_token": TOKEN,
            "v": VK_VERSION
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

    # 💬 сообщения
    if data.get("type") == "message_new":
        obj = data["object"]["message"]

        if not obj:
            return "ok"

        text = obj.get("text") or ""
        peer_id = obj.get("peer_id")
        msg_id = obj.get("id")

        # 🧠 защита от дублей VK
        if msg_id in seen:
            return "ok"
        seen.add(msg_id)

        text = text.lower().strip()

        # 🟢 старт
        if text in ["начать", "start", "бензоглаз"]:
            send(peer_id, "Система активирована")

        # ⛽ АЗС
        elif "азс" in text:
            send(peer_id, "Список АЗС формируется")

        # ✏️ сообщения пользователей
        elif "сообщ" in text:
            send(peer_id, "Напишите: АЗС + топливо + статус")

        # ❌ ничего лишнего не отвечаем
        else:
            return "ok"

    return "ok"


# 🚀 запуск Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
