# admin_engine.py

class AdministrationEngine:
    def __init__(self):
        # Dictionnaire pour stocker les parties, indexé par identifiant
        self.games = {}
        # Compteur pour générer des identifiants uniques pour chaque partie
        self.next_game_id = 1

    def init_game(self, nombre_lignes, nombre_colonnes, temps_attente, nombre_tours, nombre_obstacles, nombre_joueurs_max):
        """
        Initialise une nouvelle partie avec les paramètres fournis.
        
        Args:
            nombre_lignes (int): Nombre de lignes du plateau.
            nombre_colonnes (int): Nombre de colonnes du plateau.
            temps_attente (float): Temps d'attente maximal par tour.
            nombre_tours (int): Nombre de tours de la partie.
            nombre_obstacles (int): Nombre d'obstacles.
            nombre_joueurs_max (int): Nombre maximum de joueurs.
            
        Returns:
            dict: Un dictionnaire représentant la partie initialisée.
        """
        try:
            game = {
                "id": self.next_game_id,
                "nombre_lignes": int(nombre_lignes),
                "nombre_colonnes": int(nombre_colonnes),
                "temps_attente": float(temps_attente),
                "nombre_tours": int(nombre_tours),
                "nombre_obstacles": int(nombre_obstacles),
                "nombre_joueurs_max": int(nombre_joueurs_max),
                "status": "initialisé"
            }
        except Exception as e:
            # En cas d'erreur de conversion ou autre, lever une exception
            raise ValueError(f"Erreur lors de la conversion des paramètres : {e}")

        # Stocker la partie et incrémenter le compteur
        self.games[self.next_game_id] = game
        self.next_game_id += 1
        return game

