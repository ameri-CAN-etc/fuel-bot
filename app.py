import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN")
VK_API = "https://api.vk.com/method/messages.send"
VK_VERSION = "5.131"

BOT_TAG = "👁️ БензоГлаз ⛽"

# 🧠 защита от дублей
seen = set()


# 📦 КНОПКИ ГЛАВНОГО МЕНЮ
def keyboard_main():
    return json.dumps({
        "one_time": False,
        "buttons": [
            [
                {
                    "action": {
                        "type": "text",
                        "label": "📍 Регион"
                    },
                    "color": "primary"
                },
                {
                    "action": {
                        "type": "text",
                        "label": "⛽ АЗС рядом"
                    },
                    "color": "positive"
                }
            ],
            [
                {
                    "action": {
                        "type": "text",
                        "label": "ℹ️ Инструкция"
                    },
                    "color": "secondary"
                }
            ]
        ]
    }, ensure_ascii=False)


# 📤 отправка сообщений
def send(peer_id, text):
    requests.post(
        VK_API,
        data={
            "peer_id": peer_id,
            "message": f"{BOT_TAG}\n{text}",
            "keyboard": keyboard_main(),
            "random_id": 0,
            "access_token": TOKEN,
            "v": VK_VERSION
        }
    )


# 🌐 webhook
@app.route("/", methods=["POST"])
def main():
    data = request.json

    if not data:
        return "ok"

    # 🔑 подтверждение VK
    if data.get("type") == "confirmation":
        return "ca69504a"

    if data.get("type") == "message_new":
        obj = data["object"]["message"]

        text = (obj.get("text") or "").lower().strip()
        peer_id = obj.get("peer_id")
        msg_id = obj.get("id")

        # 🧠 защита от дублей
        if msg_id in seen:
            return "ok"
        seen.add(msg_id)

        # 📍 инструкция
        if "инстр" in text:
            send(peer_id,
                 "📌 Как работает БензоГлаз:\n"
                 "1. Выберите Регион\n"
                 "2. Выберите АЗС\n"
                 "3. Отправьте геолокацию\n"
                 "4. Получите ближайшие АЗС\n"
                 "👍 / 👎 — голосование")

        # 📍 регионы
        elif "регион" in text:
            send(peer_id,
                 "🌍 Регионы:\n"
                 "1. Тамбовская область\n"
                 "2. Московская область\n"
                 "3. Санкт-Петербург")

        # ⛽ АЗС рядом
        elif "азс рядом" in text:
            send(peer_id,
                 "📍 Отправьте геолокацию для поиска ближайших АЗС")

        # 📍 геолокация
        elif obj.get("geo"):
            coords = obj["geo"].get("coordinates")
            send(peer_id,
                 f"📍 Геолокация получена: {coords}\n⛽ Ищу ближайшие АЗС...")

        # 🟢 старт
        elif text in ["начать", "start", "бензоглаз"]:
            send(peer_id, "Система БензоГлаз активирована")

        else:
            # 🧠 всегда возвращаем меню
            send(peer_id, "Выберите действие:")

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
