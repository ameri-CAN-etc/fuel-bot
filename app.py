import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN")
VK_API = "https://api.vk.com/method/messages.send"
VK_VERSION = "5.131"

BOT_TAG = "👁️ БензоГлаз ⛽"


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


def send(peer_id, text):
    try:
        response = requests.post(
            VK_API,
            data={
                "peer_id": peer_id,
                "message": f"{BOT_TAG}\n{text}",
                "keyboard": keyboard_main(),
                "random_id": 0,
                "access_token": TOKEN,
                "v": VK_VERSION
            },
            timeout=10
        )

        print("VK RESPONSE:", response.text)

    except Exception as e:
        print("SEND ERROR:", str(e))


@app.route("/", methods=["POST"])
def main():
    data = request.json
    print("VK EVENT:", data)

    if not data:
        return "ok"

    # Подтверждение сервера VK
    if data.get("type") == "confirmation":
        return "ca69504a"

    # Интересуют только новые сообщения
    if data.get("type") != "message_new":
        return "ok"

    obj = data.get("object", {}).get("message", {})

    peer_id = obj.get("peer_id")
    text = (obj.get("text") or "").lower().strip()

    # Пришла геолокация
    if obj.get("geo"):
        coords = obj["geo"].get("coordinates")
        send(
            peer_id,
            f"📍 Геолокация получена.\n"
            f"Координаты: {coords}\n"
            f"⛽ Поиск ближайших АЗС пока в разработке."
        )
        return "ok"

    # Инструкция
    if "инстр" in text:
        send(
            peer_id,
            "Как пользоваться БензоГлаз:\n\n"
            "1️⃣ Нажмите «📍 Регион».\n"
            "2️⃣ Выберите регион.\n"
            "3️⃣ Нажмите «⛽ АЗС рядом».\n"
            "4️⃣ Отправьте геолокацию.\n"
            "5️⃣ Получите список ближайших АЗС и статус топлива."
        )
        return "ok"

    # Регион
    if "регион" in text:
        send(
            peer_id,
            "🌍 Выбор регионов пока в разработке.\n"
            "Сначала запускаем Тамбовскую область, затем всю Россию."
        )
        return "ok"

    # АЗС рядом
    if "азс рядом" in text:
        send(
            peer_id,
            "📍 Отправьте геолокацию через «Скрепка → Местоположение», и я подберу ближайшие АЗС."
        )
        return "ok"

    # Любое другое сообщение
    send(
        peer_id,
        "Добро пожаловать в БензоГлаз.\nВыберите действие с помощью кнопок ниже."
    )

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
