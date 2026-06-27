import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN")

VK_API = "https://api.vk.com/method/messages.send"
VK_VERSION = "5.131"

BOT_TAG = "👁️ БензоГлаз ⛽"


def send(peer_id, text):
    print("SEND TO:", peer_id)
    print("TEXT:", text)

    r = requests.post(
        VK_API,
        data={
            "peer_id": peer_id,
            "message": f"{BOT_TAG}\n{text}",
            "random_id": 0,
            "access_token": TOKEN,
            "v": VK_VERSION
        },
        timeout=10
    )

    print("VK RESPONSE:", r.text)


@app.route("/", methods=["POST"])
def main():
    data = request.json

    print("🔥 RAW EVENT:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    if data.get("type") == "confirmation":
        return "d06b1962"

    if data.get("type") != "message_new":
        return "ok"

    obj = data["object"]["message"]

    print("📩 MESSAGE OBJECT:", obj)

    peer_id = obj.get("peer_id")
    text = obj.get("text", "")

    print("👤 peer_id:", peer_id)
    print("💬 text:", text)

    if not peer_id:
        print("❌ NO peer_id!")
        return "ok"

    # простая проверка
    send(peer_id, "БензоГлаз онлайн ⛽👁️")

    return "ok"


@app.route("/", methods=["GET"])
def test():
    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
