import random

# Constantes pour le plateau
EMPTY = 0       # Rien
VILLAGER = 1    # Villageois
WOLF = 2        # Loup
OBSTACLE = 3    # Obstacle

class Board:
    def __init__(self, rows, cols, num_obstacles):
        """
        Crée un plateau de jeu de dimensions rows x cols et place un nombre défini d'obstacles.
        """
        self.rows = rows
        self.cols = cols
        self.grid = [[EMPTY for _ in range(cols)] for _ in range(rows)]
        self.place_obstacles(num_obstacles)
    
    def place_obstacles(self, num_obstacles):
        """
        Place aléatoirement num_obstacles obstacles (code OBSTACLE) sur le plateau.
        """
        count = 0
        while count < num_obstacles:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.grid[r][c] == EMPTY:
                self.grid[r][c] = OBSTACLE
                count += 1
    
    def is_within_bounds(self, pos):
        """
        Vérifie que la position pos (tuple (r, c)) se trouve dans les limites du plateau.
        """
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_empty(self, pos):
        """
        Vérifie si la cellule à la position pos est vide.
        """
        r, c = pos
        return self.grid[r][c] == EMPTY

    def update_cell(self, pos, value):
        """
        Met à jour la valeur de la cellule de la position pos.
        """
        r, c = pos
        self.grid[r][c] = value

    def display(self):
        """
        Affiche le plateau dans la console en traduisant les codes en symboles.
        """
        # On définit une correspondance entre le code et un symbole pour l'affichage
        mapping = {
            EMPTY: ".",
            VILLAGER: "V",
            WOLF: "W",
            OBSTACLE: "X"
        }
        print("Plateau de jeu :")
        for row in self.grid:
            print(" ".join(mapping[cell] for cell in row))
        print()


class Player:
    def __init__(self, player_id, name, role):
        """
        Représente un joueur (ou personnage).
        :param player_id: Identifiant du joueur.
        :param name: Nom du joueur.
        :param role: Rôle ("loup" ou "villageois").
        """
        self.id = player_id
        self.name = name
        self.role = role
        self.position = None

    def set_position(self, pos):
        self.position = pos


class Game:
    def __init__(self, rows, cols, num_obstacles, wait_time, role_choice):
        """
        Initialise la partie en créant le plateau et en plaçant les personnages.
        :param rows: Nombre de lignes du plateau.
        :param cols: Nombre de colonnes du plateau.
        :param num_obstacles: Nombre d'obstacles à placer.
        :param wait_time: Temps d'attente maximal par tour (non utilisé ici, à intégrer plus tard).
        :param role_choice: Le rôle choisi par le joueur ("loup" ou "villageois").
        """
        self.board = Board(rows, cols, num_obstacles)
        self.wait_time = wait_time
        # Le joueur choisit son rôle et le NPC obtient le rôle complémentaire
        self.player = Player(1, "Joueur", role_choice)
        complementary_role = "villageois" if role_choice == "loup" else "loup"
        self.npc = Player(2, "NPC", complementary_role)

        # Placement simple des personnages
        # Par exemple, le joueur en haut à gauche et le NPC en bas à droite
        self.player.position = (0, 0)
        self.npc.position = (rows - 1, cols - 1)
        # Mettre à jour le plateau : attribuer VILLAGER ou WOLF selon le rôle
        self.board.update_cell(self.player.position, VILLAGER if role_choice == "villageois" else WOLF)
        self.board.update_cell(self.npc.position, VILLAGER if complementary_role == "villageois" else WOLF)
        self.game_over = False

    def move_player(self, move_vector):
        """
        Déplace le joueur selon le vecteur de déplacement fourni.
        move_vector: chaîne de 2 caractères (ex: "01" -> 0 lignes, 1 colonne).
        Les déplacements diagonaux sont interdits (si les deux chiffres ne sont pas 0, l'un doit être 0).
        Si le mouvement est invalide, le tour est perdu.
        Si le joueur se déplace sur la cellule du NPC, la condition de victoire/défaite est évaluée.
        """
        if move_vector == "00":
            print("Le joueur passe son tour.")
            return
        
        try:
            dr = int(move_vector[0])
            dc = int(move_vector[1])
        except Exception as e:
            raise ValueError("Format du vecteur invalide. Utilisez une chaîne à deux chiffres, ex: 01")

        # Vérifier que le déplacement est horizontal ou vertical seulement
        if dr != 0 and dc != 0:
            raise ValueError("Déplacement invalide : déplacements diagonaux interdits.")

        current_pos = self.player.position
        new_pos = (current_pos[0] + dr, current_pos[1] + dc)

        # Vérifier si la nouvelle position est dans les limites
        if not self.board.is_within_bounds(new_pos):
            raise ValueError("Déplacement hors du plateau.")

        # Vérifier si la nouvelle case est libre ou occupée par le NPC
        if not self.board.is_empty(new_pos):
            if new_pos == self.npc.position:
                # Condition de victoire/défaite selon le rôle du joueur
                if self.player.role == "loup":
                    print("Le joueur loup a éliminé le NPC villageois et gagne la partie !")
                else:
                    print("Le joueur villageois a rencontré le loup et perd la partie.")
                self.end_game()
                return new_pos
            else:
                raise ValueError("Déplacement impossible : la case est occupée.")

        # Le déplacement est valide : mettre à jour le plateau
        self.board.update_cell(current_pos, EMPTY)
        self.board.update_cell(new_pos, VILLAGER if self.player.role == "villageois" else WOLF)
        self.player.set_position(new_pos)
        return new_pos

    def play_turn(self):
        if self.game_over:
            print("La partie est terminée.")
            return
        self.board.display()
        move_vector = input("Entrez le vecteur de déplacement (ex: 01, ou 00 pour passer): ").strip()
        try:
            new_pos = self.move_player(move_vector)
            print("Le joueur se déplace à :", new_pos)
        except ValueError as ve:
            print("Erreur :", ve)
            print("Ce tour est perdu.")
        self.board.display()

    def end_game(self):
        self.game_over = True
        print("Fin du jeu.")

if __name__ == "__main__":
    print("Bienvenue dans le jeu 'Les Loups' (mode solo)")
    role = input("Choisissez votre rôle (loup ou villageois): ").strip().lower()
    if role not in ["loup", "villageois"]:
        print("Rôle invalide. Veuillez choisir 'loup' ou 'villageois'.")
        exit(1)

    # Initialisation d'une partie avec un plateau 5x5 et 3 obstacles
    game = Game(5, 5, 3, wait_time=30, role_choice=role)
    while not game.game_over:
        game.play_turn()
        if game.game_over:
            break
    print("Merci d'avoir joué !")
# Fin du code