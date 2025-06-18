from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/play", methods=["POST"])
def play():
    data = request.get_json()
    move = data.get("move")

    result = jouer_uno(move)  # Fonction à adapter selon ton code existant

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
