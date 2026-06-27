from flask import Flask, request

app = Flask(__name__)

CONFIRM = "d06b1962"


@app.route("/", methods=["POST"])
def main():
    print("========== NEW REQUEST ==========")

    print("HEADERS:", dict(request.headers))
    print("METHOD:", request.method)

    raw = request.get_data(as_text=True)
    print("RAW BODY:", raw)

    try:
        data = request.get_json(silent=True)
        print("JSON PARSED:", data)
    except Exception as e:
        print("JSON ERROR:", e)

    if "confirmation" in raw:
        return CONFIRM

    print("=================================")
    return "ok"


@app.route("/", methods=["GET"])
def test():
    return "BOT OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
