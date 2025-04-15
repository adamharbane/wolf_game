from flask import Flask, request, jsonify

app = Flask(__name__)

# Pour stocker temporairement les parties (tu pourras remplacer ça par PostgreSQL plus tard)
games = []
game_counter = 1

@app.route("/")
def home():
    return jsonify({"message": "Bienvenue sur le serveur Admin HTTP"})


@app.route("/create_game", methods=["POST"])
def create_game():
    global game_counter
    data = request.get_json()

    required_keys = ["name", "rows", "cols", "max_players", "nb_obstacles", "nb_rounds", "timeout"]
    if not all(k in data for k in required_keys):
        return jsonify({"status": "KO", "error": "Paramètres manquants"}), 400

    new_game = {
        "id": game_counter,
        "name": data["name"],
        "rows": data["rows"],
        "cols": data["cols"],
        "max_players": data["max_players"],
        "nb_obstacles": data["nb_obstacles"],
        "nb_rounds": data["nb_rounds"],
        "timeout": data["timeout"]
    }

    games.append(new_game)
    game_counter += 1

    return jsonify({
        "status": "OK",
        "msg": "Partie créée avec succès",
        "game": new_game
    }), 200


@app.route("/games", methods=["GET"])
def list_games():
    return jsonify({"games": games})

if __name__ == "__main__":
    app.run(port=5051, debug=True)
