from flask import Flask, request, jsonify
from admin_tcp_client import send_to_admin
from grpc_client import send_move

app = Flask(__name__)

@app.route("/")
def home():
    return "Bienvenue sur le serveur HTTP du jeu Les Loups 🐺"

@app.route("/start", methods=["POST"])
def start_game():
    game_name = request.json.get("name")
    message = f"CREATE_GAME:{game_name}"
    response = send_to_admin(message)
    return jsonify({"admin_response": response})

@app.route("/move", methods=["POST"])
def move():
    player_id = int(request.json.get("player_id"))
    game_id = int(request.json.get("game_id"))
    direction = request.json.get("move")  # ex: "01"
    row, col = int(direction[0]), int(direction[1])

    result = send_move(player_id, game_id, row, col)
    return jsonify({
        "status": "OK" if result == "OK" else "KO",
        "move": {"row": row, "col": col}
    })

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "message": "Cette route retournera bientôt le statut d'une partie."
    })

if __name__ == "__main__":
    app.run(port=8000, debug=True)
