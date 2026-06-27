from flask import Flask, request
import json
import requests

app = Flask(__name__)

TOKEN = "PUT_YOUR_TOKEN_HERE"

VK_API = "https://api.vk.com/method/messages.send"
VK_VERSION = "5.131"

BOT_TAG = "👁️ БензоГлаз ⛽"


def send(peer_id, text):
    r = requests.post(
        VK_API,
        data={
            "peer_id": peer_id,
            "message": f"{BOT_TAG}\n{text}",
            "random_id": 0,
            "access_token": TOKEN,
            "v": VK_VERSION
        }
    )
    print("VK RESPONSE:", r.text)


@app.route("/", methods=["POST"])
def main():
    raw = request.get_data(as_text=True)

    print("RAW:", raw)

    data = json.loads(raw)

    print("EVENT:", data)

    if data["type"] == "message_new":

        obj = data["object"]["message"]

        text = obj.get("text", "").lower()
        peer_id = obj.get("peer_id")

        print("TEXT:", text)
        print("PEER:", peer_id)

        if text == "start":
            send(peer_id, "Система БензоГлаз активирована 👁️⛽")
        else:
            send(peer_id, "Выберите действие")

    return "ok"


@app.route("/", methods=["GET"])
def test():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
