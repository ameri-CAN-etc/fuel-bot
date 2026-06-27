@app.route("/", methods=["POST"])
def main():
    data = request.json

    # 🔑 ПОДТВЕРЖДЕНИЕ VK
    if data.get("type") == "confirmation":
        return "ca69504a"


import os
from flask import Flask, request
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

TOKEN = os.getenv("TOKEN")

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

app = Flask(__name__)

def menu():
    kb = VkKeyboard()
    kb.add_button("📍 АЗС", VkKeyboardColor.PRIMARY)
    kb.add_button("✏️ Сообщить", VkKeyboardColor.POSITIVE)
    return kb.get_keyboard()

def send(user_id, text):
    vk.messages.send(
        user_id=user_id,
        message=text,
        keyboard=menu(),
        random_id=0
    )

@app.route("/", methods=["POST"])
def main():
    data = request.json

    if data["type"] == "message_new":
        msg = data["object"]["message"]["text"].lower()
        user = data["object"]["message"]["from_id"]

        if msg in ["начать", "start"]:
            send(user, "⛽ Топливо Радар\nВыберите действие")

        elif msg == "📍 азс":
            send(user, "Список АЗС пока пуст")

        elif msg == "✏️ сообщить":
            send(user, "Напишите: АЗС + статус")

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
