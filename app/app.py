from flask import Flask, jsonify

app = Flask(__name__)
VERSION = "v1"


@app.get("/healthz")
def healthz():
    return jsonify(status="ok", version=VERSION)


@app.get("/")
def index():
    return jsonify(message="cicd-lab", version=VERSION)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
