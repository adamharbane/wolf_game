import random

class Game:
    def __init__(self, rows, cols, num_obstacles):
        """
        Initialise un nouveau plateau de jeu.
        :param rows: Nombre de lignes du plateau.
        :param cols: Nombre de colonnes du plateau.
        :param num_obstacles: Nombre d'obstacles à placer.
        """
        self.rows = rows
        self.cols = cols
        # Création du plateau : initialement toutes les cases sont vides (0)
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.place_obstacles(num_obstacles)

    def place_obstacles(self, num_obstacles):
        """
        Place un nombre défini d'obstacles dans des positions aléatoires sur le plateau.
        Un obstacle est représenté par le code 3.
        """
        count = 0
        while count < num_obstacles:
            r = random.randrange(self.rows)
            c = random.randrange(self.cols)
            if self.board[r][c] == 0:
                self.board[r][c] = 3
                count += 1

    def is_valid_move(self, current_position, move_vector):
        """
        Vérifie que le déplacement demandé est valide selon les règles du jeu.
        
        :param current_position: tuple (row, col) de la position actuelle.
        :param move_vector: string ou tuple indiquant le déplacement.
                            Exemples : "01" (0 lignes, 1 colonne) ou (0, 1)
        :return: tuple (new_row, new_col) si le déplacement est valide,
                 sinon lève une exception ValueError.
        """
        # Si move_vector est une chaîne, on la transforme en deux entiers.
        if isinstance(move_vector, str):
            if len(move_vector) != 2:
                raise ValueError("Le vecteur de déplacement doit être une chaîne de 2 caractères")
            try:
                dr = int(move_vector[0])
                dc = int(move_vector[1])
            except ValueError:
                raise ValueError("Les composantes du vecteur de déplacement doivent être des nombres entiers")
        elif isinstance(move_vector, tuple) and len(move_vector) == 2:
            dr, dc = move_vector
        else:
            raise ValueError("Le vecteur de déplacement doit être une chaîne de 2 caractères ou un tuple de 2 entiers")
        
        # Condition de déplacement passif : par exemple, "00" ou (0, 0) permet de passer son tour
        if dr == 0 and dc == 0:
            return current_position  # Indique qu'aucun déplacement n'est effectué (passer le tour)

        # Vérifier que le mouvement est strictement vertical ou horizontal, pas en diagonale.
        if dr != 0 and dc != 0:
            raise ValueError("Déplacement invalide : Le déplacement doit être en ligne ou en colonne uniquement (pas en diagonale)")

        new_r = current_position[0] + dr
        new_c = current_position[1] + dc

        # Vérification des limites du plateau
        if new_r < 0 or new_r >= self.rows or new_c < 0 or new_c >= self.cols:
            raise ValueError("Déplacement invalide : Hors du plateau")

        # Vérifier si la destination contient un obstacle (code 3)
        if self.board[new_r][new_c] == 3:
            raise ValueError("Déplacement invalide : La case destination contient un obstacle")

        return (new_r, new_c)

    def move_player(self, current_position, move_vector, player_role):
        """
        Effectue le déplacement du joueur si la demande est valide.
        
        :param current_position: tuple (row, col) de la position actuelle du joueur.
        :param move_vector: vecteur de déplacement (string "01" ou tuple (0,1)).
        :param player_role: rôle du joueur ("villager" ou "wolf") pour mettre à jour le plateau.
        :return: tuple (new_row, new_col) si le déplacement est effectué.
        """
        try:
            new_position = self.is_valid_move(current_position, move_vector)
        except ValueError as e:
            # Ici, si le déplacement est invalide, le tour est perdu.
            # On peut renvoyer une valeur particulière ou lever l'exception.
            raise ValueError(f"Déplacement invalide, tour perdu: {e}")

        # Mise à jour du plateau :
        r_old, c_old = current_position
        r_new, c_new = new_position

        # Vider l'ancienne position si le joueur se déplace (ne rien faire pour un tour passé)
        if (r_old, c_old) != (r_new, c_new):
            self.board[r_old][c_old] = 0

            # Affecter la nouvelle position: 1 pour villageois, 2 pour loup
            self.board[r_new][c_new] = 1 if player_role == "villager" else 2

        return new_position

    def display_board(self):
        """Affiche le plateau de manière lisible dans la console."""
        mapping = {0: ".", 1: "V", 2: "L", 3: "X"}
        for row in self.board:
            print(" ".join(mapping[cell] for cell in row))
        print()

# Exemple d'utilisation du moteur de jeu
if __name__ == "__main__":
    game = Game(5, 5, 3)  # Plateau 5x5 avec 3 obstacles
    print("Plateau initial :")
    game.display_board()

    # Position initiale supposée d'un joueur (par exemple, en haut à gauche)
    player_position = (0, 0)
    # On place le joueur sur le plateau (pour cet exemple, supposons un villageois)
    game.board[player_position[0]][player_position[1]] = 1
    
    print("Plateau avec joueur placé en (0,0) :")
    game.display_board()
    
    # Tentative de déplacement en déplaçant de 0 lignes et 1 colonne ("01")
    try:
        new_position = game.move_player(player_position, "01", "villager")
        print("Nouveau déplacement réussi vers :", new_position)
    except ValueError as ve:
        print("Erreur lors du déplacement :", ve)
    
    print("Plateau après déplacement :")
    game.display_board()

