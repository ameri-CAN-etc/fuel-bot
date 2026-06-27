from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["POST"])
def main():
    print("🔥🔥🔥 ROUTE IS RUNNING 🔥🔥🔥")
    return "ok"

@app.route("/", methods=["GET"])
def get():
    return "WORKS", 200

print("🚀 FILE LOADED")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
