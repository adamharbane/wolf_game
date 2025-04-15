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
        canvas_width = self.game.cols * self.cell_size
        canvas_height = self.game.rows * self.cell_size
        self.canvas = tk.Canvas(master, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack(padx=10, pady=10)
        
        # Champ de saisie pour le vecteur de déplacement
        self.move_entry = tk.Entry(master, font=("Arial", 16))
        self.move_entry.pack(pady=(0, 10))
        self.move_entry.insert(0, "01")  # Valeur par défaut
        
        # Bouton pour déclencher le déplacement
        self.move_button = tk.Button(master, text="Déplacer", font=("Arial", 16), command=self.move_player)
        self.move_button.pack(pady=(0, 10))
        
        # Label pour afficher des messages (erreur, victoire, etc.)
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
        # Afficher le numéro de tour en haut à gauche
        self.canvas.create_text(10, 10, anchor="nw", text=f"Tour: {self.game.turn}", font=("Arial", 14), fill="black")
    
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
            new_pos = self.game.move_player(self.player_position, move_vector, self.player_role)
            self.player_position = new_pos
            self.message_label.config(text=f"Déplacement réussi vers {new_pos}")
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
        # Mise à jour du plateau pour positionner le joueur
        self.game.board[player_pos[0]][player_pos[1]] = VILLAGER if player_role == "villager" else WOLF
        self.draw_board()

def main():
    # Demander le rôle et le nombre maximum de tours via la console
    role = input("Choisissez votre rôle (loup ou villageois): ").strip().lower()
    if role not in ["loup", "villager", "villageois"]:
        print("Rôle invalide. Veuillez choisir 'loup' ou 'villager'.")
        sys.exit(1)
    
    if role in ["villager", "villageois"]:
        player_role = "villager"
        npc_role = "wolf"
    else:
        player_role = "wolf"
        npc_role = "villager"
    
    try:
        max_turns = int(input("Entrez le nombre maximum de tours: ").strip())
    except ValueError:
        print("Nombre de tours invalide.")
        sys.exit(1)
    
    # Initialiser la partie avec un plateau de 5x5, 3 obstacles, et le nombre maximum de tours choisi
    game = Game(rows=5, cols=5, num_obstacles=3, max_turns=max_turns)
    
    # Positions initiales
    player_pos = (0, 0)
    npc_pos = (game.rows - 1, game.cols - 1)
    
    # Mise à jour du plateau pour le NPC (le NPC reste statique)
    game.board[npc_pos[0]][npc_pos[1]] = VILLAGER if npc_role == "villager" else WOLF
    
    print("Plateau initial:")
    game.display_board()
    
    # Lancer l'interface graphique Tkinter
    root = tk.Tk()
    gui = GameGUI(root, game, cell_size=80)
    gui.set_initial_positions(player_pos, npc_pos, player_role)
    root.mainloop()

if __name__ == "__main__":
    main()
    # Pour éviter les erreurs de fermeture de fenêtre

    try:
        main()
    except KeyboardInterrupt:
        print("\nArrêt du client.")
        sys.exit(0)
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        sys.exit(1)