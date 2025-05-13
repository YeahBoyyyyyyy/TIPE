import sys
import os
sys.path.append("C:/Users/natha/OneDrive/Desktop/Travail/TIPE")
import IATableDesTypes as IA
import donnees
import numpy as np

os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Stockage_individus")

matrix = IA.Dracaufeu.type_chart

def write_pokemon_description(file, pokemon):
    type = pokemon.type
    name = pokemon.name
    hp = pokemon.hp
    attacks = pokemon.attacks
    fitness = pokemon.fitness
    file.write(f"Nom: {name}\n")
    file.write(f"Type: {type}\n")
    file.write(f"HP: {hp}\n")
    file.write(f"Attaques: {attacks}\n")
    file.write(f"Fitness: {fitness}\n")

## Sauvegarde de l'individu dans un fichier texte
fichier = open('stock.txt', 'w')

for row in matrix:
    fichier.write(' '.join([str(a) for a in row]) + '\n')

write_pokemon_description(fichier, IA.Dracaufeu)

fichier.close()

with open('stock.txt', 'r') as fichier:
    matrix_from_file = [list(map(float, line.split())) for _, line in zip(range(18), fichier)]

#print(np.array(matrix_from_file))
# Le fichier est créé dans le répertoire courant, qui est défini par défaut comme "TIPE".
# Pour s'assurer que le fichier est créé dans "Stockage_individus", changez le répertoire courant.








