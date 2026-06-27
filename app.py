from flask import Flask, request
import json

app = Flask(__name__)

CONFIRM = "d06b1962"


@app.route("/", methods=["POST"])
def main():
    raw = request.get_data(as_text=True)

    print("RAW DATA:", raw)

    try:
        data = json.loads(raw)
    except Exception as e:
        print("JSON PARSE ERROR:", e)
        return "ok"

    print("EVENT:", data)

    if data.get("type") == "confirmation":
        return CONFIRM

    if data.get("type") == "message_new":
        print("MESSAGE RECEIVED")

    return "ok"


@app.route("/", methods=["GET"])
def test():
    return "OK BOT IS RUNNING", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
