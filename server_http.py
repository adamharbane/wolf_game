#!/usr/bin/env python3


from flask import Flask, request, jsonify
import logging
import sys

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False  # Pour conserver l'ordre dans les réponses JSON

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# --- Fonctions stubs pour simuler la communication ---

def send_to_admin(message):
    """
    Simulation d'envoi d'un message vers l'admin_engine via TCP.
    Retourne une réponse simulée.
    """
    logging.info(f"(Simulé) Envoi à admin_engine: {message}")
    # On peut simuler différentes réponses en fonction du message
    if message.startswith("CREATE_GAME:"):
        game_name = message.split(":", 1)[1]
        return f"Partie '{game_name}' créée avec succès."
    elif message == "LIST_GAMES":
        return [1, 2, 3]
    elif message.startswith("SUBSCRIBE:"):
        # Retourne un rôle et un id_player simulés.
        return {"role": "wolf", "id_player": 23}
    else:
        return f"Réponse simulée pour {message}"

def send_move(player_id, game_id, row, col):
    """
    Simulation d'un appel gRPC vers le moteur de jeu (game_engine) pour exécuter un déplacement.
    Ici, on simule simplement un résultat "OK" pour tout déplacement.
    """
    logging.info(f"(Simulé) Appel gRPC : player_id={player_id}, game_id={game_id}, move=({row}, {col})")
    # Simule une réponse du game_engine ; vous pouvez simuler plus d'informations ici.
    return "OK"

# --- Endpoints Flask ---

@app.route("/")
def home():
    """Page d'accueil du serveur HTTP."""
    return jsonify({"message": "Bienvenue sur le serveur HTTP du jeu Les Loups 🐺"})

@app.route("/start", methods=["POST"])
def start_game():
    """
    Démarre une nouvelle partie.
    Entrée attendue : JSON avec la clé "name" pour le nom de la partie.
    Utilise send_to_admin pour communiquer avec l'admin_engine (simulé).
    """
    try:
        data = request.get_json(force=True)
        game_name = data.get("name")
        if not game_name:
            raise ValueError("Le nom de la partie est requis.")
        message = f"CREATE_GAME:{game_name}"
        logging.info(f"Démarrage d'une partie : {game_name}")
        response = send_to_admin(message)
        return jsonify({"status": "OK", "admin_response": response})
    except Exception as e:
        logging.error(f"Erreur dans /start: {e}")
        return jsonify({"status": "KO", "error": str(e)}), 400

@app.route("/move", methods=["POST"])
def move():
    """
    Exécute un déplacement dans une partie.
    Entrée attendue : JSON contenant "player_id", "game_id" et "move" (ex: "01").
    Utilise send_move pour appeler le moteur de jeu (simulé en gRPC).
    """
    try:
        data = request.get_json(force=True)
        for field in ("player_id", "game_id", "move"):
            if field not in data:
                raise ValueError(f"Le champ '{field}' est requis.")
        player_id = int(data.get("player_id"))
        game_id = int(data.get("game_id"))
        move_str = data.get("move")
        if not (isinstance(move_str, str) and len(move_str) == 2):
            raise ValueError("Le paramètre move doit être une chaîne de 2 caractères.")
        
        # Extraction de la direction pour log (ici simple)
        row = int(move_str[0])
        col = int(move_str[1])
        logging.info(f"Demande de déplacement: player_id={player_id}, game_id={game_id}, move={move_str}")
        result = send_move(player_id, game_id, row, col)
        status = "OK" if result == "OK" else "KO"
        return jsonify({
            "status": status,
            "move": {"row": row, "col": col},
            "result": result
        })
    except Exception as e:
        logging.error(f"Erreur dans /move: {e}")
        return jsonify({"status": "KO", "error": str(e)}), 400

@app.route("/status", methods=["GET"])
def status():
    """
    Retourne un statut préliminaire statique du serveur.
    À adapter pour renvoyer des informations réelles sur l'état d'une partie.
    """
    try:
        return jsonify({
            "status": "OK",
            "message": "Statut du serveur: la partie est en cours ou terminée selon vos actions."
        })
    except Exception as e:
        logging.error(f"Erreur dans /status: {e}")
        return jsonify({"status": "KO", "error": str(e)}), 400

@app.route("/list", methods=["GET"])
def list_games():
    """
    Liste les parties ouvertes non commencées.
    Utilise send_to_admin pour communiquer avec l'admin_engine (simulé).
    """
    try:
        message = "LIST_GAMES"
        logging.info("Requête pour lister les parties ouvertes.")
        response = send_to_admin(message)
        return jsonify({"status": "OK", "response": {"id_parties": response}})
    except Exception as e:
        logging.error(f"Erreur dans /list: {e}")
        return jsonify({"status": "KO", "error": str(e)}), 400

@app.route("/subscribe", methods=["POST"])
def subscribe():
    """
    Permet à un joueur de s'inscrire à une partie.
    Entrée attendue : JSON contenant "player" et "id_party".
    Utilise send_to_admin pour communiquer avec l'admin_engine (simulé).
    """
    try:
        data = request.get_json(force=True)
        for field in ("player", "id_party"):
            if field not in data:
                raise ValueError(f"Le champ '{field}' est requis.")
        player = data.get("player")
        id_party = data.get("id_party")
        message = f"SUBSCRIBE:{player}:{id_party}"
        logging.info(f"Demande d'inscription: {message}")
        response = send_to_admin(message)
        return jsonify({"status": "OK", "response": response})
    except Exception as e:
        logging.error(f"Erreur dans /subscribe: {e}")
        return jsonify({"status": "KO", "error": str(e)}), 400

if __name__ == "__main__":
    try:
        app.run(port=8000, debug=True)
    except Exception as e:
        logging.error(f"Erreur critique dans le serveur HTTP: {e}")
        sys.exit(1)
