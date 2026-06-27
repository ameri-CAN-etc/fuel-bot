from flask import Flask, request
import os

app = Flask(__name__)

CONFIRM = "d06b1962"


@app.route("/", methods=["POST"])
def main():
    data = request.json

    print("EVENT RECEIVED:", data)

    if data.get("type") == "confirmation":
        return CONFIRM

    if data.get("type") == "message_new":
        print("MESSAGE OK")

    return "ok"


@app.route("/", methods=["GET"])
def test():
    return "OK BOT IS RUNNING", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
