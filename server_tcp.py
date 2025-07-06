#!/usr/bin/env python3
import socket
import threading
import json
import grpc  #

class TCPServer:
    def __init__(self, host="0.0.0.0", port=5001):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Serveur TCP d'administration démarré sur {self.host}:{self.port}")

    def handle_client(self, conn, addr):
        print(f"Connexion établie avec {addr}")
        receive_buffer = ""
        try:
            while True:
                data = conn.recv(4096)
                if not data:
                    print(f"Connexion fermée par {addr}")
                    break
                receive_buffer += data.decode("utf-8")
                # On utilise le délimiteur "\n" pour séparer les messages
                while "\n" in receive_buffer:
                    message, receive_buffer = receive_buffer.split("\n", 1)
                    print(f"Message reçu de {addr}: {message}")
                    try:
                        request = json.loads(message)
                    except json.JSONDecodeError as e:
                        response = {"status": "KO", "response": f"JSON invalide: {e}"}
                        self.send_response(conn, response)
                        continue
                    response = self.process_request(request)
                    self.send_response(conn, response)
        except Exception as e:
            print(f"Erreur avec le client {addr}: {e}")
        finally:
            conn.close()
            print(f"Connexion terminée avec {addr}")

    def send_response(self, conn, response):
        try:
            response_str = json.dumps(response) + "\n"
            conn.sendall(response_str.encode("utf-8"))
            print(f"Réponse envoyée: {response_str.strip()}")
        except Exception as e:
            print(f"Erreur lors de l'envoi de la réponse: {e}")

    def process_request(self, req):
        """
        Traite la requête JSON reçue et renvoie une réponse.
        On suppose que req est un dictionnaire avec au moins la clé 'action'
        et éventuellement 'parameters'.
        """
        action = req.get("action")
        parameters = req.get("parameters", [])
       
        print(f"Action demandée: {action} avec paramètres: {parameters}")
        
        # Pour l'exemple, voici des réponses simulées pour chaque action
        if action == "list":
            # Action : Lister les parties ouvertes non commencées
            return {"status": "OK", "response": {"id_parties": [1, 2, 3]}}
        elif action == "subscribe":
            # Action : Inscription
            # On attend deux paramètres : player et id_party
            # Vérification simplifiée :
            if len(parameters) < 2:
                return {"status": "KO", "response": "Paramètres insuffisants pour l'inscription"}
            # Simuler une réponse
            return {"status": "OK", "response": {"role": "wolf", "id_player": 23}}
        elif action == "party_status":
            # Action : Récupérer l'état du tour
            return {"status": "OK", "response": {"party": {
                "id_party": 23,
                "id_player": 12,
                "started": True,
                "round_in_progress": 12,
                "move": {"next_position": {"row": 0, "col": 1}}
            }}}
        elif action == "gameboard_status":
           
            return {"status": "OK", "response": {"visible_cells": "010010000"}}
        elif action == "move":
            
            if len(parameters) < 3:
                return {"status": "KO", "response": "Paramètres insuffisants pour le déplacement"}
            move_value = None
            for p in parameters:
                if "move" in p:
                    move_value = p["move"]
                    break
            if not move_value:
                return {"status": "KO", "response": "Paramètre 'move' absent"}
            
            # Ici, appelons le moteur de jeu via gRPC.
            try:
             
                result = {"round_in_progress": 12, "move": {"next_position": {"row": 0, "col": 1}}}
                return {"status": "OK", "response": result}
            except Exception as e:
                return {"status": "KO", "response": f"Erreur gRPC: {e}"}
        else:
            return {"status": "KO", "response": "Action non reconnue"}
    
    def run(self):
        while True:
            try:
                conn, addr = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                client_thread.start()
            except KeyboardInterrupt:
                print("Arrêt du serveur.")
                self.server_socket.close()
                break

if __name__ == "__main__":
    # Initialisation du serveur TCP
    HOST = "0.0.0.0"
    PORT = 5001
    server = TCPServer(HOST, PORT)
    server.run()
