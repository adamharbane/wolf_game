from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

games = []
game_counter = 1

@app.route("/")
def home():
    return render_template("create_game.html", game=None)

@app.route("/create_game", methods=["POST"])
def create_game():
    global game_counter
    data = request.form  # récupère le formulaire HTML

    new_game = {
        "id": game_counter,
        "name": data["name"],
        "rows": int(data["rows"]),
        "cols": int(data["cols"]),
        "max_players": int(data["max_players"]),
        "nb_obstacles": int(data["nb_obstacles"]),
        "nb_rounds": int(data["nb_rounds"]),
        "timeout": int(data["timeout"])
    }

    games.append(new_game)
    game_counter += 1

    return render_template("create_game.html", game=new_game)
