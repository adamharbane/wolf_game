#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog, filedialog
import requests
import json
import sys
import logging
import os
from datetime import datetime

# --- Configuration Globale ---
BASE_URL = "http://127.0.0.1:5000"
TIMEOUT = 10  # Timeout pour les requêtes HTTP
LOG_FILE = "client_http_complex.log"
HISTORY_FILE = "request_history.txt"

# --- Configuration du Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

# --- Classe HTTPClientComplex ---
class HTTPClientComplex:
    def __init__(self, base_url=BASE_URL, timeout=TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.last_response = None
        self.history = []  # Historique sous forme de liste de dicts

    def _send_request(self, method, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        logging.info(f"Envoi d'une requête {method} à {url} avec data={data}")
        try:
            if method.upper() == "POST":
                response = requests.post(url, json=data, timeout=self.timeout)
            elif method.upper() == "GET":
                response = requests.get(url, timeout=self.timeout, params=data)
            else:
                raise ValueError(f"Méthode HTTP non supportée: {method}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Erreur lors de l'envoi de la requête: {e}")
            raise Exception(f"Erreur lors de l'envoi de la requête : {e}")
        
        logging.info(f"Code de réponse: {response.status_code}")
        try:
            result = response.json()
        except json.JSONDecodeError:
            logging.error("Réponse non JSON reçue")
            raise Exception("La réponse n'est pas au format JSON.\n" + response.text)
        
        self.last_response = result
        entry = {
            "timestamp": datetime.now().isoformat(),
            "method": method.upper(),
            "url": url,
            "request": data,
            "response": result
        }
        self.history.append(entry)
        logging.info(f"Réponse reçue: {result}")
        return result

    def init_game(self, data):
        return self._send_request("POST", "/init_game", data)

    def check_status(self):
        return self._send_request("GET", "/status")

    def save_history_to_file(self, filename=HISTORY_FILE):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
            logging.info(f"Historique sauvegardé dans {filename}")
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde de l'historique : {e}")
            raise Exception(f"Erreur lors de la sauvegarde de l'historique : {e}")

# --- Classe GUI pour le Client HTTP Complex ---
class HTTPClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Client HTTP Complex - Les Loups")
        # Instance du client HTTP
        self.client = HTTPClientComplex()
        # Création de l'interface en onglets via Notebook
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.create_config_tab()
        self.create_request_tab()
        self.create_history_tab()
        self.create_log_tab()
        self.last_response_text = ""

    def create_config_tab(self):
        """Onglet pour configurer l'URL de base, la méthode et autres options."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Configuration")
        
        ttk.Label(frame, text="URL de Base:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.url_entry = ttk.Entry(frame, width=50)
        self.url_entry.insert(0, BASE_URL)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Timeout (sec):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.timeout_entry = ttk.Entry(frame, width=10)
        self.timeout_entry.insert(0, str(TIMEOUT))
        self.timeout_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Button(frame, text="Appliquer", command=self.apply_config).grid(row=2, column=0, columnspan=2, pady=5)

    def apply_config(self):
        """Met à jour la configuration du client."""
        new_url = self.url_entry.get().strip()
        try:
            new_timeout = float(self.timeout_entry.get().strip())
        except ValueError:
            messagebox.showerror("Erreur de configuration", "Le timeout doit être un nombre.")
            return
        self.client.base_url = new_url
        self.client.timeout = new_timeout
        messagebox.showinfo("Configuration", "Configuration mise à jour.")
    
    def create_request_tab(self):
        """Onglet pour saisir et envoyer des requêtes HTTP."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Requête")
        
        # Sélecteur de méthode HTTP
        ttk.Label(frame, text="Méthode:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.method_var = tk.StringVar(value="POST")
        method_combo = ttk.Combobox(frame, textvariable=self.method_var, values=["GET", "POST"], width=8)
        method_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Zone pour saisir le JSON de la requête
        ttk.Label(frame, text="Corps de la requête (JSON):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.request_text = tk.Text(frame, height=8, width=60)
        self.request_text.insert(tk.END, '{"action": "list", "parameters": []}')
        self.request_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        # Boutons pour envoyer des requêtes prédéfinies
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(btn_frame, text="Envoyer", command=self.send_request).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Liste", command=self.send_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Statut", command=self.send_status).pack(side=tk.LEFT, padx=5)
    
    def send_request(self):
        """Envoie la requête saisie manuellement."""
        method = self.method_var.get().strip().upper()
        try:
            data = json.loads(self.request_text.get("1.0", tk.END))
        except json.JSONDecodeError as e:
            messagebox.showerror("Erreur JSON", f"Erreur lors du parsing du JSON : {e}")
            return
        try:
            if method == "GET":
                result = self.client._send_request("GET", "/init_game", data)  # ou un autre endpoint
            elif method == "POST":
                result = self.client._send_request("POST", "/init_game", data)
            else:
                messagebox.showerror("Erreur", f"Méthode {method} non supportée.")
                return
            self.last_response_text = json.dumps(result, indent=2, ensure_ascii=False)
            self.update_history(f"Requête {method} vers /init_game\n{json.dumps(data)}\nRéponse:\n{self.last_response_text}")
            messagebox.showinfo("Réponse", f"Statut: {result.get('status')}")
        except Exception as e:
            messagebox.showerror("Erreur HTTP", f"Erreur lors de l'envoi de la requête : {e}")

    def send_list(self):
        """Envoie une requête prédéfinie pour lister les parties."""
        request_data = {"action": "list", "parameters": []}
        self.request_text.delete("1.0", tk.END)
        self.request_text.insert(tk.END, json.dumps(request_data, indent=2))
        self.send_request()

    def send_status(self):
        """Envoie une requête prédéfinie pour vérifier le statut du serveur."""
        try:
            result = self.client.check_status()
            self.last_response_text = json.dumps(result, indent=2, ensure_ascii=False)
            self.update_history(f"Requête GET vers /status\nRéponse:\n{self.last_response_text}")
            messagebox.showinfo("Statut", f"Statut: {result.get('status')}")
        except Exception as e:
            messagebox.showerror("Erreur HTTP", f"Erreur lors de la requête : {e}")

    def create_history_tab(self):
        """Onglet pour afficher l'historique des requêtes et réponses."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Historique")
        # Listbox pour afficher l'historique
        self.history_listbox = tk.Listbox(frame, height=15)
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        # Bouton pour sauvegarder l'historique dans un fichier
        btn = ttk.Button(frame, text="Sauvegarder l'historique", command=self.save_history)
        btn.pack(pady=(0,5))

    def update_history(self, entry):
        """Ajoute une entrée à l'historique et l'affiche dans la Listbox."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_entry = f"[{timestamp}] {entry}"
        self.history_listbox.insert(tk.END, full_entry)
    
    def save_history(self):
        """Sauvegarde l'historique dans un fichier choisi par l'utilisateur."""
        filename = filedialog.asksaveasfilename(title="Sauvegarder l'historique", 
                                                defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    for entry in self.client.history:
                        f.write(json.dumps(entry, indent=2, ensure_ascii=False) + "\n")
                messagebox.showinfo("Historique", f"Historique sauvegardé dans {filename}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde de l'historique : {e}")

    def create_log_tab(self):
        """Onglet pour afficher les logs détaillés."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Logs")
        self.log_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        # Charger le contenu du fichier de log si existant
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                self.log_text.insert(tk.END, f.read())

def main():
    root = tk.Tk()
    app = HTTPClientGUI(root)
    root.mainloop()

if __name__ == "__main__":
    from datetime import datetime  # Importé ici pour update_history
    import os
    main()
