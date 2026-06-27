import os
from flask import Flask, request
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

app = Flask(__name__)

# 🔑 TOKEN из Render
TOKEN = os.environ.get("TOKEN")

# ⚠️ защита от падения
if not TOKEN:
    print("❌ TOKEN not found in environment variables")

vk_session = vk_api.VkApi(token=TOKEN) if TOKEN else None
vk = vk_session.get_api() if vk_session else None


# 🧠 клавиатура
def menu():
    kb = VkKeyboard(one_time=False)
    kb.add_button("📍 АЗС", color=VkKeyboardColor.PRIMARY)
    kb.add_button("✏️ Сообщить", color=VkKeyboardColor.POSITIVE)
    return kb.get_keyboard()


def send(user_id, text):
    if not vk:
        print("VK not initialized")
        return

    vk.messages.send(
        user_id=user_id,
        message=text,
        keyboard=menu(),
        random_id=0
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

    # 💬 входящие сообщения
    if data.get("type") == "message_new":
        msg = data["object"]["message"]["text"].lower()
        user = data["object"]["message"]["from_id"]

        if msg in ["начать", "start"]:
            send(user, "⛽ Топливо Радар запущен")

        elif msg == "📍 азс":
            send(user, "⛽ АЗС список в разработке")

        elif msg == "✏️ сообщить":
            send(user, "Напишите: АЗС + топливо + статус")

        else:
            send(user, "Команда не распознана")

    return "ok"


# 🚀 запуск сервера Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
