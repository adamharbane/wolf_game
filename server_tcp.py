import socket
import json
from grpc_client import send_move

HOST = 'localhost'
PORT = 5000

def handle_client(conn):
    try:
        data = conn.recv(4096).decode()
        print("Reçu :", data)

        request = json.loads(data)
        action = request.get("action")
        params = {p.get("id_party") or p.get("id_player") or p.get("move") or p.get("player"): p
                  for p in request.get("parameters", [])}

        if action == "move":
            id_party = int(params["id_party"]["id_party"])
            id_player = int(params["id_player"]["id_player"])
            move = params["move"]["move"]
            row, col = int(move[0]), int(move[1])
            result = send_move(id_player, id_party, row, col)

            response = {
                "status": "OK" if result == "OK" else "KO",
                "response": {
                    "move": {
                        "next_position": {"row": row, "col": col}
                    }
                }
            }
        else:
            response = {
                "status": "KO",
                "response": {"message": "Action non supportée"}
            }

    except Exception as e:
        print("Erreur :", e)
        response = {"status": "KO", "response": {"message": str(e)}}

    conn.send(json.dumps(response).encode())
    conn.close()

def start_tcp_server():
    print(f"[TCP] Serveur démarré sur {HOST}:{PORT}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    while True:
        conn, addr = server.accept()
        print(f"[TCP] Nouvelle connexion de {addr}")
        handle_client(conn)

if __name__ == "__main__":
    start_tcp_server()
