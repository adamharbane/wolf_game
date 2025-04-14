import tkinter as tk
from tkinter import messagebox
from game_engine import Game, EMPTY, VILLAGER, WOLF, OBSTACLE
import sys

class GameGUI:
    def __init__(self, master, game, cell_size=80):
        self.master = master
        self.game = game
        self.cell_size = cell_size
        
        master.title("Les Loups - Mode Solo")
        
        # Dimensions du Canvas basées sur le plateau
        canvas_width = self.game.rows * self.cell_size
        canvas_height = self.game.cols * self.cell_size
        self.canvas = tk.Canvas(master, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack(padx=10, pady=10)
        
        # Champ de saisie pour le vecteur de déplacement
        self.move_entry = tk.Entry(master, font=("Arial", 16))
        self.move_entry.pack(pady=(0, 10))
        self.move_entry.insert(0, "01")  # Valeur par défaut
        
        # Bouton pour tenter le déplacement
        self.move_button = tk.Button(master, text="Déplacer", font=("Arial", 16), command=self.move_player)
        self.move_button.pack(pady=(0, 10))
        
        # Label pour afficher des messages (ex: erreur, victoire, etc.)
        self.message_label = tk.Label(master, text="", font=("Arial", 14))
        self.message_label.pack(pady=(0, 10))
        
        self.draw_board()

    def draw_board(self):
        """Dessine le plateau sur le Canvas."""
        self.canvas.delete("all")
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                cell_value = self.game.board[r][c]
                color = self.get_color(cell_value)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
    
    def get_color(self, cell_value):
        """Retourne une couleur en fonction du contenu de la cellule."""
        if cell_value == EMPTY:
            return "white"
        elif cell_value == VILLAGER:
            return "blue"
        elif cell_value == WOLF:
            return "red"
        elif cell_value == OBSTACLE:
            return "black"
        else:
            return "gray"
    
    def move_player(self):
        """Tente le déplacement du joueur en utilisant le vecteur saisi."""
        move_vector = self.move_entry.get().strip()
        try:
            # Ici, on appelle move_player() du Game en passant la position actuelle du joueur, le vecteur et le rôle.
            new_pos = self.game.move_player(self.player_position, move_vector, self.player_role)
            self.player_position = new_pos
            self.message_label.config(text=f"Déplacement réussi : {new_pos}")
        except Exception as e:
            messagebox.showerror("Erreur de déplacement", str(e))
            self.message_label.config(text="Déplacement invalide, tour perdu.")
        self.draw_board()
        if self.game.game_over:
            self.move_button.config(state="disabled")
            self.message_label.config(text="Partie terminée.")

    def set_initial_positions(self, player_pos, npc_pos, player_role):
        """Configure les positions initiales et le rôle du joueur dans l'interface."""
        self.player_position = player_pos
        self.player_role = player_role
        # Mettre à jour le plateau avec les positions initiales
        self.game.board[player_pos[0]][player_pos[1]] = VILLAGER if player_role == "villager" else WOLF
        # On suppose que le NPC occupe déjà sa position dans le Game (par exemple, le coin opposé)
        # Actualisation de l'affichage
        self.draw_board()

def main():
    # Demander le rôle du joueur via la console
    role = input("Choisissez votre rôle (loup ou villageois): ").strip().lower()
    if role not in ["loup", "villager", "villageois"]:
        print("Rôle invalide. Veuillez choisir 'loup' ou 'villageois'.")
        sys.exit(1)
    
    # Adapter le rôle pour correspondre aux constantes utilisées
    if role in ["villager", "villageois"]:
        player_role = "villager"
        npc_role = "wolf"
    else:
        player_role = "wolf"
        npc_role = "villager"
        
    # Initialisation de la partie avec un plateau de 5x5, 3 obstacles.
    # Remarque : dans game_engine.py, la classe Game initiale définit self.rows et self.cols d'après les arguments rows et cols,
    # et crée le plateau dans self.board. Vous pouvez aussi modifier Game pour exposer ces attributs directement.
    game = Game(rows=5, cols=5, num_obstacles=3)
    
    # Définir les positions initiales:
    # Par exemple, le joueur en haut à gauche et le NPC en bas à droite
    player_pos = (0, 0)
    npc_pos = (game.rows - 1, game.cols - 1)
    
    # Mettre à jour le plateau : placer le NPC (la logique d'initialisation du NPC devrait être gérée dans le game, à améliorer plus tard)
    game.board[npc_pos[0]][npc_pos[1]] = VILLAGER if npc_role == "villager" else WOLF
    
    # Afficher le plateau initial dans la console pour vérification
    print("Plateau initial :")
    game.display_board()
    
    # Lancer l'interface graphique Tkinter
    root = tk.Tk()
    gui = GameGUI(root, game, cell_size=80)
    gui.set_initial_positions(player_pos, npc_pos, player_role)
    root.mainloop()

if __name__ == "__main__":
    main()
