import socket
import json
from grpc_client import send_move
from admin_tcp_client import send_to_admin

HOST = 'localhost'
PORT = 5000

def handle_client(conn):
    try:
        data = conn.recv(4096).decode()
        print("[TCP] Reçu :", data)
        request = json.loads(data)
        action = request.get("action")
        params = {k: v for d in request.get("parameters", []) for k, v in d.items()}

        # === Gestion des actions ===
        if action == "move":
            id_party = int(params["id_party"])
            id_player = int(params["id_player"])
            move = params["move"]
            row, col = int(move[0]), int(move[1])
            grpc_result = send_move(id_player, id_party, row, col)

            response = {
                "status": "OK" if grpc_result == "OK" else "KO",
                "response": {
                    "round_in_progress": 12,  # à remplacer par appel réel
                    "move": {
                        "next_position": {
                            "row": row,
                            "col": col
                        }
                    }
                }
            }

        elif action == "list":
            # Exemple : demander au service admin les parties
            admin_response = send_to_admin("LIST_GAMES")
            response = {
                "status": "OK",
                "response": {
                    "id_parties": [int(x) for x in admin_response.split(',')]
                }
            }

        elif action == "subscribe":
            # Exemple de message à l’admin
            player_name = params["player"]
            party_id = int(params["id_party"])
            admin_response = send_to_admin(f"SUBSCRIBE:{player_name}:{party_id}")
            role, player_id = admin_response.split(":")
            response = {
                "status": "OK",
                "response": {
                    "role": role,
                    "id_player": int(player_id)
                }
            }

        elif action == "party_status":
            response = {
                "status": "OK",
                "response": {
                    "party": {
                        "id_party": int(params["id_party"]),
                        "id_player": int(params["id_player"]),
                        "started": True,
                        "round_in_progress": 3,
                        "move": {
                            "next_position": {
                                "row": 1,
                                "col": 1
                            }
                        }
                    }
                }
            }

        elif action == "gameboard_status":
            response = {
                "status": "OK",
                "response": {
                    "visible_cells": "010010000"
                }
            }

        else:
            response = {
                "status": "KO",
                "response": {"message": f"Action non supportée : {action}"}
            }

    except Exception as e:
        print("[TCP] Erreur :", e)
        response = {"status": "KO", "response": {"message": str(e)}}

    conn.send(json.dumps(response).encode())
    conn.close()

def start_tcp_server():
    print(f"[TCP] Serveur TCP démarré sur {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        while True:
            conn, addr = server.accept()
            print(f"[TCP] Connexion de {addr}")
            handle_client(conn)

if __name__ == "__main__":
    start_tcp_server()
