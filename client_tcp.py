import tkinter as tk
from tkinter import ttk, simpledialog
import socket
import json
import threading
from tkinter import messagebox  # Optionnel pour les pop-ups

class TCPClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Client TCP - Les Loups")
        
        # Variables de connexion
        self.host_var = tk.StringVar(value="127.0.0.1")
        self.port_var = tk.StringVar(value="5001")
        
        # Variable de requête JSON (modifiable manuellement aussi)
        self.request_text = tk.StringVar(value='{"action": "list", "parameters": []}')
        
        # Zone d'affichage pour les logs
        self.log_text = None
        
        # Zone dédiée aux notifications
        self.notify_list = None

        # Socket et thread pour la réception
        self.client_socket = None
        self.receive_thread = None
        self.running = False
        self.receive_buffer = ""
        
        self.create_widgets()
        
    def create_widgets(self):
        # Cadre de connexion
        connection_frame = ttk.LabelFrame(self.root, text="Connexion")
        connection_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(connection_frame, text="Host:").pack(side=tk.LEFT, padx=2)
        host_entry = ttk.Entry(connection_frame, textvariable=self.host_var, width=15)
        host_entry.pack(side=tk.LEFT, padx=2)
        ttk.Label(connection_frame, text="Port:").pack(side=tk.LEFT, padx=2)
        port_entry = ttk.Entry(connection_frame, textvariable=self.port_var, width=5)
        port_entry.pack(side=tk.LEFT, padx=2)
        connect_button = ttk.Button(connection_frame, text="Se connecter", command=self.connect_to_server)
        connect_button.pack(side=tk.LEFT, padx=5)
        disconnect_button = ttk.Button(connection_frame, text="Déconnexion", command=self.disconnect)
        disconnect_button.pack(side=tk.LEFT, padx=5)
        
        # Cadre pour saisir une requête JSON
        request_frame = ttk.LabelFrame(self.root, text="Requête JSON (modifiable)")
        request_frame.pack(fill=tk.X, padx=5, pady=5)
        request_entry = ttk.Entry(request_frame, textvariable=self.request_text, width=50)
        request_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        send_button = ttk.Button(request_frame, text="Envoyer", command=self.send_request)
        send_button.pack(side=tk.LEFT, padx=5)
        
        # Cadre pour les actions prédéfinies
        actions_frame = ttk.LabelFrame(self.root, text="Actions Pré-définies")
        actions_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(actions_frame, text="Liste des parties", command=self.send_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="S'inscrire", command=self.send_subscribe).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="État du tour", command=self.send_party_status).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="État du plateau", command=self.send_gameboard_status).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="Déplacer", command=self.send_move).pack(side=tk.LEFT, padx=5)
        
        # Cadre des logs
        log_frame = ttk.LabelFrame(self.root, text="Logs")
        log_frame.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)
        self.log_text = tk.Text(log_frame, wrap="word")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Cadre des notifications
        notify_frame = ttk.LabelFrame(self.root, text="Notifications")
        notify_frame.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)
        self.notify_list = tk.Listbox(notify_frame)
        self.notify_list.pack(fill=tk.BOTH, expand=True)

    def connect_to_server(self):
        if self.client_socket:
            self.log("Déjà connecté.")
            return
        host = self.host_var.get()
        try:
            port = int(self.port_var.get())
        except ValueError:
            self.log("Le port doit être un nombre.")
            return
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            self.running = True
            self.log(f"Connecté au serveur {host}:{port}")
            self.receive_thread = threading.Thread(target=self.listen_server, daemon=True)
            self.receive_thread.start()
        except Exception as e:
            self.log(f"Erreur de connexion : {e}")
            self.client_socket = None

    def disconnect(self):
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except Exception as e:
                self.log(f"Erreur lors de la fermeture du socket : {e}")
            self.client_socket = None
            self.log("Déconnecté du serveur.")

    def send_request(self):
        if not self.client_socket:
            self.log("Pas de connexion au serveur.")
            return
        try:
            request_data = self.request_text.get()
            # Ajoute un délimiteur pour le message (ici \n)
            message = request_data + "\n"
            self.log(f"Envoi de la requête : {message.strip()}")
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            self.log(f"Erreur lors de l'envoi : {e}")

    def listen_server(self):
        self.receive_buffer = ""
        while self.running and self.client_socket:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    self.log("La connexion a été fermée par le serveur.")
                    self.disconnect()
                    break
                self.receive_buffer += data.decode('utf-8')
                while "\n" in self.receive_buffer:
                    message, self.receive_buffer = self.receive_buffer.split("\n", 1)
                    self.log(f"Réponse reçue : {message}")
                    try:
                        response_json = json.loads(message)
                        self.log(f"Réponse JSON parsée : {response_json}")
                        # Vérifier si le message est une notification (par exemple, une action particulière)
                        self.check_for_notification(response_json)
                    except json.JSONDecodeError:
                        self.log("Erreur lors du parsing du JSON")
            except Exception as e:
                self.log(f"Erreur lors de la réception : {e}")
                self.disconnect()
                break

    def log(self, message):
        if self.log_text:
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)
        else:
            print(message)
    
    # Fonction de notification
    def notify(self, message):
        """Ajoute une notification dans la zone de notifications et affiche éventuellement une pop-up."""
        if self.notify_list:
            self.notify_list.insert(tk.END, message)
        # Optionnel : afficher une pop-up de notification
        # messagebox.showinfo("Notification", message)
    
    # Vérifie la réponse pour voir si c'est une notification à afficher
    def check_for_notification(self, response):
        # Ici, vous pouvez définir votre logique pour déterminer si la réponse contient une notification
        # Par exemple, si l'action est "party_status" et que l'état du tour change, on peut notifier l'utilisateur.
        if response.get("status") == "OK":
            # Exemple : notifier lorsque le tour est en progression et que la position suivante a changé
            if "response" in response and "party" in response["response"]:
                party_info = response["response"]["party"]
                if "round_in_progress" in party_info and party_info["round_in_progress"] != -1:
                    # On construit un message de notification
                    note = f"Tour en cours: Partie {party_info.get('id_party')}, Action du joueur {party_info.get('id_player')}, prochaine position: {party_info['move'].get('next_position')}"
                    self.notify(note)
        # Vous pouvez étendre cette logique pour d'autres types de notifications

    # Méthodes pour envoyer les requêtes prédéfinies
    def send_list(self):
        request = {"action": "list", "parameters": []}
        self.request_text.set(json.dumps(request))
        self.send_request()

    def send_subscribe(self):
        player = simpledialog.askstring("S'inscrire", "Entrez le nom du joueur:")
        id_party = simpledialog.askinteger("S'inscrire", "Entrez l'ID de la partie:")
        if player is None or id_party is None:
            self.log("Inscription annulée.")
            return
        request = {
            "action": "subscribe",
            "parameters": [
                {"player": player},
                {"id_party": id_party}
            ]
        }
        self.request_text.set(json.dumps(request))
        self.send_request()

    def send_party_status(self):
        id_player = simpledialog.askinteger("État du tour", "Entrez l'ID du joueur:")
        id_party = simpledialog.askinteger("État du tour", "Entrez l'ID de la partie:")
        if id_player is None or id_party is None:
            self.log("Requête d'état du tour annulée.")
            return
        request = {
            "action": "party_status",
            "parameters": [
                {"id_player": id_player},
                {"id_party": id_party}
            ]
        }
        self.request_text.set(json.dumps(request))
        self.send_request()

    def send_gameboard_status(self):
        id_party = simpledialog.askinteger("État du plateau", "Entrez l'ID de la partie:")
        id_player = simpledialog.askinteger("État du plateau", "Entrez l'ID du joueur:")
        if id_party is None or id_player is None:
            self.log("Requête d'état du plateau annulée.")
            return
        request = {
            "action": "gameboard_status",
            "parameters": [
                {"id_party": id_party},
                {"id_player": id_player}
            ]
        }
        self.request_text.set(json.dumps(request))
        self.send_request()

    def send_move(self):
        id_party = simpledialog.askinteger("Déplacer", "Entrez l'ID de la partie:")
        id_player = simpledialog.askinteger("Déplacer", "Entrez l'ID du joueur:")
        move_value = simpledialog.askstring("Déplacer", "Entrez le vecteur de déplacement (ex: '01'):")
        if id_party is None or id_player is None or move_value is None:
            self.log("Requête de déplacement annulée.")
            return
        request = {
            "action": "move",
            "parameters": [
                {"id_party": id_party},
                {"id_player": id_player},
                {"move": move_value}
            ]
        }
        self.request_text.set(json.dumps(request))
        self.send_request()

    def on_close(self):
        self.disconnect()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = TCPClientApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

if __name__ == "__main__":
    main()

