#!/usr/bin/env python3
"""
Client HTTP Terminal pour le projet 'Les Loups' – version avancée
-------------------------------------------------------------------
Ce script permet d'interagir avec un serveur HTTP pour :
  - Initialiser une partie
  - Vérifier le statut du serveur
  - Afficher l'historique des réponses reçues
  - Réinitialiser les paramètres (option de redémarrage)
Le script intègre une gestion avancée des erreurs et une journalisation détaillée.
"""

import requests
import json
import sys
import logging

# Configuration globale
BASE_URL = "http://127.0.0.1:5000"
TIMEOUT = 10  # timeout en secondes
LOG_FILE = "client_http_terminal_complex.log"

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

class HTTPClient:
    """
    Classe pour gérer l'interaction avec le serveur HTTP dans le cadre du projet.
    """
    def __init__(self, base_url=BASE_URL, timeout=TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.last_response = None
        self.history = []  # Historique complet des réponses

    def _send_request(self, method, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        logging.info(f"Envoi d'une requête {method} à {url} avec data={data}")
        try:
            if method.upper() == "POST":
                response = requests.post(url, json=data, timeout=self.timeout)
            elif method.upper() == "GET":
                response = requests.get(url, timeout=self.timeout)
            else:
                raise ValueError(f"Méthode HTTP non supportée: {method}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Erreur lors de l'envoi de la requête: {e}")
            print(f"Erreur lors de l'envoi de la requête: {e}")
            return None
        
        logging.info(f"Code de réponse: {response.status_code}")
        try:
            result = response.json()
        except json.JSONDecodeError:
            logging.error("La réponse n'est pas au format JSON")
            print("Erreur: La réponse n'est pas au format JSON.")
            print(response.text)
            return None
        
        self.last_response = result
        self.history.append(result)
        logging.info(f"Réponse reçue: {result}")
        return result

    def init_game(self, data):
        """
        Envoie une requête POST pour initialiser une partie.
        """
        return self._send_request("POST", "/init_game", data)

    def check_status(self):
        """
        Envoie une requête GET pour vérifier le statut du serveur.
        """
        return self._send_request("GET", "/status")

    def print_history(self):
        """
        Affiche l'historique complet des réponses.
        """
        if not self.history:
            print("Aucune réponse enregistrée.")
            return
        print("\n=== Historique des réponses ===")
        for i, resp in enumerate(self.history, start=1):
            print(f"--- Réponse {i} ---")
            print(json.dumps(resp, indent=2, ensure_ascii=False))
            print("-------------------------")
    
def prompt_int(prompt, default=None):
    """Demande une valeur entière avec gestion d'erreur et possibilité de valeur par défaut."""
    while True:
        s = input(prompt)
        if s.strip() == "" and default is not None:
            return default
        try:
            return int(s)
        except ValueError:
            print("Erreur : veuillez saisir un entier valide.")

def prompt_float(prompt, default=None):
    """Demande une valeur flottante avec gestion d'erreur et valeur par défaut."""
    while True:
        s = input(prompt)
        if s.strip() == "" and default is not None:
            return default
        try:
            return float(s)
        except ValueError:
            print("Erreur : veuillez saisir un nombre valide.")

def build_init_data():
    """Construit les données d'initialisation du jeu basées sur la saisie utilisateur."""
    print("\n=== Initialisation de la partie ===")
    data = {}
    try:
        data["nombre_lignes"] = prompt_int("Nombre de lignes du plateau: ")
        data["nombre_colonnes"] = prompt_int("Nombre de colonnes du plateau: ")
        data["temps_attente"] = prompt_float("Temps d'attente maximal pour un tour (secondes): ")
        data["nombre_tours"] = prompt_int("Nombre de tours de la partie: ")
        data["nombre_obstacles"] = prompt_int("Nombre d'obstacles: ")
        data["nombre_joueurs_max"] = prompt_int("Nombre maximum de joueurs: ")
    except Exception as e:
        print(f"Erreur lors de la saisie: {e}")
        return None
    return data

def print_menu():
    """Affiche le menu interactif."""
    print("\n=== Menu Client HTTP Avancé ===")
    print("1. Initialiser une partie")
    print("2. Vérifier le statut du serveur")
    print("3. Afficher la dernière réponse du serveur")
    print("4. Afficher l'historique complet des réponses")
    print("5. Quitter")

def main():
    client = HTTPClient()
    
    while True:
        print_menu()
        choix = input("Votre choix (1/2/3/4/5): ").strip()
        if choix == "1":
            data = build_init_data()
            if data is None:
                continue
            result = client.init_game(data)
            if result is not None:
                print("\nRéponse du serveur (initialisation):")
                print(json.dumps(result, indent=2, ensure_ascii=False))
        elif choix == "2":
            result = client.check_status()
            if result is not None:
                print("\nRéponse du serveur (statut):")
                print(json.dumps(result, indent=2, ensure_ascii=False))
        elif choix == "3":
            if client.last_response is not None:
                print("\n=== Dernière réponse du serveur ===")
                print(json.dumps(client.last_response, indent=2, ensure_ascii=False))
            else:
                print("Aucune réponse enregistrée.")
        elif choix == "4":
            client.print_history()
        elif choix == "5":
            print("Quitter...")
            break
        else:
            print("Choix invalide. Veuillez entrer 1, 2, 3, 4 ou 5.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nArrêt du client.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Erreur inattendue: {e}")
        print(f"Erreur inattendue: {e}")
        sys.exit(1)
