import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json

class HTTPClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Client HTTP - Les Loups")
        
        # Variables pour l'URL et la méthode HTTP
        self.url_var = tk.StringVar(value="http://127.0.0.1:5000")
        self.method_var = tk.StringVar(value="POST")
        # Requête JSON initiale (modifiable selon le protocole)
        self.request_text = tk.StringVar(value='{"action": "list", "parameters": []}')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Cadre pour les paramètres de connexion HTTP
        connection_frame = ttk.LabelFrame(self.root, text="Paramètres HTTP")
        connection_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(connection_frame, text="URL:").pack(side=tk.LEFT, padx=2)
        url_entry = ttk.Entry(connection_frame, textvariable=self.url_var, width=50)
        url_entry.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(connection_frame, text="Méthode:").pack(side=tk.LEFT, padx=2)
        method_combo = ttk.Combobox(connection_frame, textvariable=self.method_var, values=["GET", "POST"], width=8)
        method_combo.pack(side=tk.LEFT, padx=2)
        
        # Cadre pour saisir la requête JSON
        request_frame = ttk.LabelFrame(self.root, text="Requête JSON")
        request_frame.pack(fill=tk.X, padx=5, pady=5)
        
        request_entry = ttk.Entry(request_frame, textvariable=self.request_text, width=50)
        request_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        send_button = ttk.Button(request_frame, text="Envoyer", command=self.send_request)
        send_button.pack(side=tk.LEFT, padx=5)
        
        # Cadre pour afficher la réponse HTTP
        response_frame = ttk.LabelFrame(self.root, text="Réponse HTTP")
        response_frame.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)
        
        self.response_text = scrolledtext.ScrolledText(response_frame, wrap=tk.WORD)
        self.response_text.pack(fill=tk.BOTH, expand=True)
    
    def send_request(self):
        url = self.url_var.get()
        method = self.method_var.get()
        try:
            payload = json.loads(self.request_text.get())
        except json.JSONDecodeError as e:
            messagebox.showerror("Erreur JSON", f"Erreur lors du parsing du JSON : {e}")
            return
        
        try:
            if method == "GET":
                # Pour GET, envoie les paramètres dans l'URL
                response = requests.get(url, params=payload)
            elif method == "POST":
                # Pour POST, envoie la charge en JSON
                response = requests.post(url, json=payload)
            else:
                messagebox.showerror("Erreur", f"Méthode {method} non supportée.")
                return
            
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert(tk.END, f"Statut : {response.status_code}\n")
            try:
                json_response = response.json()
                self.response_text.insert(tk.END, json.dumps(json_response, indent=2))
            except ValueError:
                # Réponse non au format JSON
                self.response_text.insert(tk.END, response.text)
        except Exception as e:
            messagebox.showerror("Erreur HTTP", f"Erreur lors de l'envoi de la requête : {e}")
    
def main():
    root = tk.Tk()
    app = HTTPClientApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()



