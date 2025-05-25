import os
import IATableDesTypes as IA
from Stockage_individus import load as load
import tkinter as tk
from tkinter import Canvas, PhotoImage
from PIL import Image, ImageTk
import donnees

''' Programme avec pygame 
os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Stockage_individus")
pygame.init()
pygame.font.init()

# Utilisation du stock de données pour teste

with open('stock20.txt', 'r') as fichier:
    matrix_from_file = [list(map(float, line.split())) for _,line in zip(range(18),fichier)]


font = pygame.font.Font(None, 20)

screen = pygame.display.set_mode((900, 600))
os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE")
image = pygame.image.load("assets/type chart icons.png").convert_alpha()

# type_chart(donnees.type_chart)
pokemon1 = load.import_pokemon("test1.txt")
pokemon2 = load.import_pokemon("test2.txt")

child = IA.crossover(pokemon1, pokemon2)

print(child.type_chart)
#for i in range(100000):
    

l,h = 45,21

rect_x, rect_y = 9+l, 5+h 
rect_width, rect_height = 750, 490

rect_pattern_width = 43
rect_pattern_height = 28

sub_types_images = [[],[],[]]
for k in range(3):
    for i in range(6):
        sub_types_images[k].append(image.subsurface(51*k, i*h, l,h))

image_rect = image.get_rect()
running = True

### Fonction affichant la table des types
def type_chart(chart):
        for i, row in zip(range(18),range(rect_y, rect_y + rect_height, rect_pattern_height)):
            for j, col in zip(range(18),range(rect_x, rect_x + rect_width, rect_pattern_width)):
                if chart[i][j] == 0:
                    pygame.draw.rect(screen, (0,0,0), (col, row, rect_pattern_width, rect_pattern_height))
                    screen.blit(multiplier_text[1], (col+10, row+5))
                elif chart[i][j] == 0.5:
                    pygame.draw.rect(screen, (211,45,45), (col, row, rect_pattern_width, rect_pattern_height))
                    screen.blit(multiplier_text[2], (col+10, row+5))
                elif chart[i][j] == 1:
                    pygame.draw.rect(screen, (140,140,140), (col, row, rect_pattern_width, rect_pattern_height))
                    screen.blit(multiplier_text[0], (col+10, row+5))
                else:
                    pygame.draw.rect(screen, (14,209,69), (col, row, rect_pattern_width, rect_pattern_height))
                    screen.blit(multiplier_text[3], (col+10, row+5))

### Fonction créant une mutation et l'affichant en même temps
def mutation(pokemon):
    IA.mutation_type_chart(pokemon)
    type_chart(pokemon.type_chart)

# Préparation de la fenêtre
screen.fill((128, 128, 128))
    
pygame.draw.rect(screen, (200,200,200), (0,0,850,560))
    
for j in range(3):
    for i in range(6):
        screen.blit(sub_types_images[j][i], (i*43+258*j+50,0))
        screen.blit(sub_types_images[j][i], (0,i*29+j*170+25))

multiplier_text = [font.render("x1", True, (0,0,0)), font.render("x0", True, (255,255,255)), 
                   font.render("x0.5", True, (0,0,0)), font.render("x2", True, (0,0,0))]

# Affichage de la table des types
type_chart(child.type_chart)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
                
    mutation(child)
    
    pygame.display.flip()
    

pygame.quit()
'''

# Version Tkinter de l'affichage de la table des types

os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Stockage_individus")

# enregistrer dans une liste tous les fichiers .txt
fichiers = [f for f in os.listdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Stockage_individus") if f.endswith('.txt')]

# Paramètres d'affichage
l, h = 43, 19
rect_x, rect_y = 8 + l, 5 + h
rect_width, rect_height = 750, 490
rect_pattern_width = 43
rect_pattern_height = 26
default_gap = 4

# Préparation des textes multiplicateurs
multiplier_text = ["x1", "x0", "x0.5", "x2"]
multiplier_colors = ["#000000", "#FFFFFF", "#000000", "#000000"]
rect_colors = ["#8C8C8C", "#000000", "#D32D2D", "#0FD647"]

# Chargement de l'image des types

os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE")
types = ["normal", "fighting", "flying", "poison", "ground", "rock", "bug", "ghost", "steel",
          "fire", "water", "grass", "electric", "psychic", "ice", "dragon", "dark", "fairy"]
type_images = [Image.open("assets/" + types[i] + ".png").convert("RGBA") for i in range(18)]

def get_multiplier_index(value):
    if value == 1:
        return 0
    elif value == 0:
        return 1
    elif value == 0.5:
        return 2
    else:
        return 3

def type_table_window(canvas):
    # Affichage des icônes de types sur la première ligne et la première colonne
    for i in range(18):
        # Ligne du haut (types defensifs)
        img = ImageTk.PhotoImage(type_images[i].resize((l, h)))
        canvas.create_image(rect_x + i * rect_pattern_width, 5, anchor=tk.NW, image=img)
        # Conserver la référence pour éviter le garbage collection
        if not hasattr(canvas, 'type_imgs_row'):
            canvas.type_imgs_row = []
        canvas.type_imgs_row.append(img)

        # Colonne de gauche (types offensifs)
        img2 = ImageTk.PhotoImage(type_images[i].resize((l, h)))
        canvas.create_image(5, default_gap + rect_y + i * rect_pattern_height, anchor=tk.NW, image=img2)
        if not hasattr(canvas, 'type_imgs_col'):
            canvas.type_imgs_col = []
        canvas.type_imgs_col.append(img2)

def type_chart(chart,canvas):
    for i, row in zip(range(18), range(rect_y, rect_y + rect_height, rect_pattern_height)):
        for j, col in zip(range(18), range(rect_x, rect_x + rect_width, rect_pattern_width)):
            val = chart[i][j]
            idx = get_multiplier_index(val)
            canvas.create_rectangle(col, row, col + rect_pattern_width, row + rect_pattern_height, fill=rect_colors[idx], outline="#222")
            canvas.create_text(col + 21, row + 14, text=multiplier_text[idx], fill=multiplier_colors[idx], font=("Arial", 10, "bold"))

def manual_mutation():
    # Fenêtre pour demander l'indice du pokémon à muter
    popup = tk.Toplevel(window)
    popup.title("Choisir le pokémon à muter")
    popup.geometry("300x100")

    tk.Label(popup, text="Indice Pokémon à muter:").pack(pady=5)
    entry = tk.Entry(popup)
    entry.pack(pady=5)

    def do_mutation():
        try:
            idx = int(entry.get())
            if idx < 0 or idx >= len(fichiers):
                raise ValueError
            poke = load.import_pokemon(fichiers[idx])
            for _ in range(100):
                IA.mutation_type_chart(poke)
            btn = tk.Button(window, text=f"Muté {idx}", command=lambda: create_table_type_window_from_pokemon(poke))
            btn.grid(row=len(buttons)+3, column=6, padx=10, pady=5)
        except Exception:
            tk.Label(popup, text="Indice invalide", fg="red").pack()
        else:
            popup.destroy()

    tk.Button(popup, text="Muter", command=do_mutation).pack(pady=10)

def manual_crossover():
    # Fenêtre pour demander les indices des pokémons à croiser
    popup = tk.Toplevel(window)
    popup.title("Choisir les pokémons à croiser")
    popup.geometry("300x150")

    tk.Label(popup, text="Indice Pokémon 1:").pack(pady=5)
    entry1 = tk.Entry(popup)
    entry1.pack(pady=5)

    tk.Label(popup, text="Indice Pokémon 2:").pack(pady=5)
    entry2 = tk.Entry(popup)
    entry2.pack(pady=5)

    def do_crossover():
        try:
            idx1 = int(entry1.get())
            idx2 = int(entry2.get())
            if idx1 < 0 or idx1 >= len(fichiers) or idx2 < 0 or idx2 >= len(fichiers):
                raise ValueError
            poke1 = load.import_pokemon(fichiers[idx1])
            poke2 = load.import_pokemon(fichiers[idx2])
            baby = IA.crossover(poke1, poke2)
            btn = tk.Button(window, text=f"Enfant {idx1}-{idx2}", command=lambda: create_table_type_window_from_pokemon(baby))
            btn.grid(row=4, column=4, padx=10, pady=5)
        except Exception:
            tk.Label(popup, text="Indices invalides", fg="red").pack()
        else:
            popup.destroy()

    tk.Button(popup, text="Croiser", command=do_crossover).pack(pady=10)

pokemon_basic_type_chart = IA.simplepokemon()
pokemon_basic_type_chart.type_chart = donnees.type_chart

#### -------------------------------Fenêtre Tkinter------------------------------- ####

def create_table_type_window_from_file(name):
    pokemon = load.import_pokemon(name)
    extra_window = tk.Toplevel()
    extra_window.title(name)
    extra_window.geometry("900x500")
    canvas = Canvas(extra_window, width=900, height=600, bg="#9F9E9E")
    canvas.pack()
    type_table_window(canvas)
    type_chart(pokemon.type_chart, canvas)

def create_table_type_window_from_pokemon(pokemon):
    extra_window = tk.Toplevel()
    extra_window.title(pokemon.name)
    extra_window.geometry("900x500")
    canvas = Canvas(extra_window, width=900, height=600, bg="#9F9E9E")
    canvas.pack()
    type_table_window(canvas)
    type_chart(pokemon.type_chart, canvas)

def remove_button(button):
    button.grid_forget()


window = tk.Tk()
window.title("Affichage Table des Types")
window.geometry("700x700")

buttons = []
for i, fichier in enumerate(fichiers):
    button = tk.Button(window, text="pokémon n° " + str(i+1), command=lambda name=fichier: create_table_type_window_from_file(name))
    if i >= 10:
        button.grid(row=i-10, column=1, padx=10, pady=10)
    else:
        button.grid(row=i, column=0, padx=10, pady=10)
    buttons.append(button)

mutate_button = tk.Button(window, text="Muter", command=lambda: manual_mutation())
mutate_button.grid(row=0, column=5, padx=20, pady=10, sticky="ne")

crossover_button = tk.Button(window, text="Croiser", command=lambda: manual_crossover())
crossover_button.grid(row=2, column=5, padx=20, pady=10, sticky="ne")

test = tk.Button(window, text="Test", command = lambda: remove_button(crossover_button))
test.grid(row=1, column=5, padx=20, pady=10, sticky="ne")
# Comment enlever un bouton de l'affichage ?


window.mainloop()



