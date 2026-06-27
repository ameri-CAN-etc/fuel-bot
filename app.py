import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN")

VK_API = "https://api.vk.com/method/messages.send"
VK_VERSION = "5.131"

BOT_TAG = "👁️ БензоГлаз ⛽"


# ---------------- KEYBOARD ----------------
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


# ---------------- SEND ----------------
def send(peer_id, text):
    try:
        r = requests.post(
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

        print("VK RESPONSE:", r.text)

    except Exception as e:
        print("SEND ERROR:", str(e))


# ---------------- WEBHOOK ----------------
@app.route("/", methods=["POST"])
def main():
    data = request.json

    print("EVENT:", data)

    if not data:
        return "ok"

    # confirmation VK
    if data.get("type") == "confirmation":
        return "d06b1962"

    if data.get("type") != "message_new":
        return "ok"

    obj = data["object"]["message"]

    peer_id = obj.get("peer_id")
    text = (obj.get("text") or "").lower().strip()

    geo = obj.get("geo")

    # ---------------- GEO ----------------
    if geo:
        coords = geo.get("coordinates")
        send(
            peer_id,
            f"📍 Геолокация получена:\n{coords}\n\n"
            "⛽ Ищу ближайшие АЗС (пока базовый режим)."
        )
        return "ok"

    # ---------------- MENU ----------------
    if "инстр" in text:
        send(
            peer_id,
            "ℹ️ БензоГлаз:\n\n"
            "📍 Регион → выбор области\n"
            "⛽ АЗС рядом → отправь геолокацию\n"
            "🗺️ Система покажет ближайшие заправки"
        )
        return "ok"

    if "регион" in text:
        send(
            peer_id,
            "🌍 Регионы:\n"
            "• Тамбовская область\n"
            "• Московская область\n"
            "• Санкт-Петербург\n\n"
            "🧭 Скоро: вся Россия"
        )
        return "ok"

    if "азс" in text:
        send(
            peer_id,
            "📍 Отправь геолокацию через:\n"
            "Скрепка → Местоположение"
        )
        return "ok"

    # ---------------- START ----------------
    if text in ["start", "начать", "бензоглаз"]:
        send(
            peer_id,
            "Система БензоГлаз активирована 👁️⛽\nВыберите действие:"
        )
        return "ok"

    # ---------------- DEFAULT ----------------
    send(peer_id, "Выберите действие через меню 👇")
    return "ok"


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
