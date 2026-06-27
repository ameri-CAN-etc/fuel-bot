import os
from flask import Flask, request
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

app = Flask(__name__)

# VK TOKEN из Render Environment Variables
TOKEN = os.getenv("TOKEN")

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

# 🧠 Главное меню
def menu():
    kb = VkKeyboard(one_time=False)

    kb.add_button("📍 АЗС", color=VkKeyboardColor.PRIMARY)
    kb.add_button("✏️ Сообщить", color=VkKeyboardColor.POSITIVE)

    return kb.get_keyboard()

# 📤 отправка сообщений
def send(user_id, text):
    vk.messages.send(
        user_id=user_id,
        message=text,
        keyboard=menu(),
        random_id=0
    )

# 🌐 Webhook (Render)
@app.route("/", methods=["POST"])
def main():
    data = request.json

    # 🔑 ПОДТВЕРЖДЕНИЕ VK СЕРВЕРА (ОБЯЗАТЕЛЬНО)
    if data.get("type") == "confirmation":
        return "ca69504a"

    # 💬 ВХОДЯЩИЕ СООБЩЕНИЯ
    if data.get("type") == "message_new":
        msg = data["object"]["message"]["text"].lower()
        user = data["object"]["message"]["from_id"]

        # старт
        if msg in ["начать", "start"]:
            send(user, "⛽ Топливо Радар запущен")

        # список АЗС (заглушка)
        elif msg == "📍 азс":
            send(user, "Список АЗС пока в разработке ⛽")

        # форма сообщения
        elif msg == "✏️ сообщить":
            send(user, "Напишите: АЗС + топливо + статус")

        else:
            send(user, "Команда не распознана")

    return "ok"


# 🚀 запуск сервера
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
