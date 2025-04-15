import random

# Constantes globales définissant les contenus du plateau
EMPTY = 0       # Case vide
VILLAGER = 1    # Villageois
WOLF = 2        # Loup
OBSTACLE = 3    # Obstacle

class Game:
    def __init__(self, rows, cols, num_obstacles, max_turns):
        """
        Initialise un nouveau plateau de jeu avec des dimensions données 
        et place aléatoirement un nombre défini d'obstacles.
        
        :param rows: Nombre de lignes du plateau.
        :param cols: Nombre de colonnes du plateau.
        :param num_obstacles: Nombre d'obstacles à placer.
        :param max_turns: Nombre maximum de tours autorisés avant de terminer la partie.
        """
        self.rows = rows
        self.cols = cols
        # Création du plateau : toutes les cases sont initialement vides (EMPTY)
        self.board = [[EMPTY for _ in range(cols)] for _ in range(rows)]
        self.place_obstacles(num_obstacles)
        self.game_over = False  # Indique la fin de la partie
        self.turn = 0         # Compteur de tours
        self.max_turns = max_turns  # Nombre maximum de tours avant fin de partie

    def place_obstacles(self, num_obstacles):
        """
        Place aléatoirement num_obstacles obstacles (OBSTACLE) sur le plateau.
        """
        count = 0
        while count < num_obstacles:
            r = random.randrange(self.rows)
            c = random.randrange(self.cols)
            if self.board[r][c] == EMPTY:
                self.board[r][c] = OBSTACLE
                count += 1

    def is_valid_move(self, current_position, move_vector):
        """
        Vérifie que le vecteur de déplacement est valide.
        
        :param current_position: tuple (row, col) indiquant la position actuelle.
        :param move_vector: chaîne de 2 caractères (ex : "01") ou tuple (0, 1).
        :return: tuple (new_row, new_col) si le déplacement est valide.
        :raises ValueError: en cas de vecteur invalide, déplacement diagonal ou hors plateau.
        """
        if isinstance(move_vector, str):
            if len(move_vector) != 2:
                raise ValueError("Le vecteur de déplacement doit être une chaîne de 2 caractères")
            try:
                dr = int(move_vector[0])
                dc = int(move_vector[1])
            except ValueError:
                raise ValueError("Les composantes du vecteur doivent être des nombres entiers")
        elif isinstance(move_vector, tuple) and len(move_vector) == 2:
            dr, dc = move_vector
        else:
            raise ValueError("Le vecteur de déplacement doit être une chaîne de 2 caractères ou un tuple de 2 entiers")

        if dr == 0 and dc == 0:
            return current_position

        if dr != 0 and dc != 0:
            raise ValueError("Déplacement invalide : déplacements diagonaux interdits")

        new_r = current_position[0] + dr
        new_c = current_position[1] + dc

        if new_r < 0 or new_r >= self.rows or new_c < 0 or new_c >= self.cols:
            raise ValueError("Déplacement invalide : Hors du plateau")
        if self.board[new_r][new_c] == OBSTACLE:
            raise ValueError("Déplacement invalide : La case destination contient un obstacle")
        return (new_r, new_c)

    def move_player(self, current_position, move_vector, player_role):
        """
        Effectue le déplacement du joueur vers la nouvelle position si le mouvement est valide.
        Pour une collision :
          - Si le joueur est wolf et se déplace sur la case d'un villageois, le loup gagne.
          - Si le joueur est villager et se déplace sur la case d'un loup, le villageois gagne.
        Le NPC reste statique.
        
        Si le déplacement est normal, le joueur se déplace et le compteur de tours est incrémenté.
        Si le nombre maximum de tours est atteint, la partie se termine.
        
        :param current_position: tuple (row, col) de la position actuelle du joueur.
        :param move_vector: vecteur de déplacement (string "01" ou tuple (0,1)).
        :param player_role: "villager" ou "wolf".
        :return: tuple (new_row, new_col) si le déplacement est effectué.
        :raises ValueError: si le déplacement est invalide.
        """
        try:
            new_position = self.is_valid_move(current_position, move_vector)
        except ValueError as e:
            raise ValueError(f"Déplacement invalide, tour perdu: {e}")

        r_old, c_old = current_position
        r_new, c_new = new_position
        expected_value = VILLAGER if player_role == "villager" else WOLF

        # Si la case cible contient déjà un personnage
        if self.board[r_new][c_new] in (VILLAGER, WOLF):
            # Si la case contient le personnage opposé, collision et fin de partie
            if self.board[r_new][c_new] != expected_value:
                self.board[r_old][c_old] = EMPTY
                self.board[r_new][c_new] = expected_value
                self.turn += 1
                self.game_over = True
                return new_position
            else:
                raise ValueError("Déplacement impossible : la case est déjà occupée par le même type.")
        else:
            # Déplacement normal
            self.board[r_old][c_old] = EMPTY
            self.board[r_new][c_new] = expected_value
            self.turn += 1
            # Vérification du nombre maximum de tours
            if self.turn >= self.max_turns:
                self.game_over = True
            return new_position

    def display_board(self):
        """
        Affiche le plateau de jeu dans le terminal (pour débogage), ainsi que le numéro de tour.
        """
        mapping = {EMPTY: ".", VILLAGER: "V", WOLF: "W", OBSTACLE: "X"}
        for row in self.board:
            print(" ".join(mapping[cell] for cell in row))
        print(f"Tour: {self.turn}\n")

# Bloc de test pour le mode terminal
if __name__ == "__main__":
    # Pour le test, on fixe le nombre maximum de tours à 5
    game = Game(5, 5, 3, max_turns=5)
    print("Plateau initial:")
    game.display_board()

    # Positionnement initial : joueur en (0,0) et NPC en (rows-1, cols-1)
    player_position = (0, 0)
    npc_position = (game.rows - 1, game.cols - 1)
    game.board[player_position[0]][player_position[1]] = VILLAGER  # Joueur villageois
    game.board[npc_position[0]][npc_position[1]] = WOLF            # NPC loup

    print("Plateau après placement:")
    game.display_board()

    # Exemple 1 : déplacement normal (supposons "01" vers la droite)
    try:
        new_position = game.move_player(player_position, "01", "villager")
        print("Déplacement réussi vers:", new_position)
    except ValueError as ve:
        print("Erreur lors du déplacement:", ve)
    game.display_board()

    # Exemple 2 : repositionnement pour collision
    if not game.game_over:
        # On repositionne le joueur près du NPC, par exemple en (4,3) si le NPC est en (4,4)
        player_position = (game.rows - 1, game.cols - 2)
        game.board[player_position[0]][player_position[1]] = VILLAGER
        print("Plateau avant collision (positionnement stratégique):")
        game.display_board()

        try:
            # Déplacement vers la droite ("01") pour atteindre le NPC
            new_position = game.move_player(player_position, "01", "villager")
            print("Déplacement en collision réussi vers:", new_position)
        except ValueError as ve:
            print("Erreur lors du déplacement en collision:", ve)
        game.display_board()

        if game.game_over:
            print("Partie terminée : victoire du joueur (collision détectée ou maximum de tours atteint).")
        else:
            print("Partie en cours.")
    else:
        print("Partie déjà terminée après le premier déplacement.")