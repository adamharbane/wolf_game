import requests
import json

def init_game():
    print("\n=== Initialisation de la partie ===")
    try:
        # Saisie des paramètres par l'utilisateur
        nombre_lignes = int(input("Nombre de lignes du plateau: "))
        nombre_colonnes = int(input("Nombre de colonnes du plateau: "))
        temps_attente = float(input("Temps d'attente maximal pour un tour (en secondes): "))
        nombre_tours = int(input("Nombre de tours de la partie: "))
        nombre_obstacles = int(input("Nombre d'obstacles: "))
        nombre_joueurs_max = int(input("Nombre maximum de joueurs: "))
    except ValueError as ve:
        print(f"Erreur de saisie: {ve}")
        return

    # Préparer le JSON de la requête
    data = {
        "nombre_lignes": nombre_lignes,
        "nombre_colonnes": nombre_colonnes,
        "temps_attente": temps_attente,
        "nombre_tours": nombre_tours,
        "nombre_obstacles": nombre_obstacles,
        "nombre_joueurs_max": nombre_joueurs_max
    }
    
    url = "http://127.0.0.1:5000/init_game"
    try:
        response = requests.post(url, json=data)
        print(f"Code de réponse: {response.status_code}")
        try:
            result = response.json()
            print("Réponse reçue:")
            print(json.dumps(result, indent=2))
        except json.JSONDecodeError:
            print("La réponse n'est pas au format JSON:")
            print(response.text)
    except Exception as e:
        print(f"Erreur lors de l'envoi de la requête: {e}")

def check_status():
    print("\n=== Vérification du statut du serveur ===")
    url = "http://127.0.0.1:5000/status"
    try:
        response = requests.get(url)
        print(f"Code de réponse: {response.status_code}")
        try:
            result = response.json()
            print("Réponse reçue:")
            print(json.dumps(result, indent=2))
        except json.JSONDecodeError:
            print("La réponse n'est pas au format JSON:")
            print(response.text)
    except Exception as e:
        print(f"Erreur lors de la requête: {e}")

def main():
    while True:
        print("\n=== Menu Client HTTP ===")
        print("1. Initialiser une partie")
        print("2. Vérifier le statut du serveur")
        print("3. Quitter")
        choix = input("Votre choix (1/2/3) : ")

        if choix == "1":
            init_game()
        elif choix == "2":
            check_status()
        elif choix == "3":
            print("Quitter...")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()

#
# Note: This code is a simplified version of the client HTTP terminal application.
