import sys
import os
sys.path.append("C:/Users/natha/OneDrive/Desktop/Travail/TIPE")
import IATableDesTypes as IA
import donnees
import numpy as np

os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Stockage_individus")


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
def save_gen(generation):
    n = len(generation)

    for i in range(n):
        fichier = open("stock" + str(i+1) + ".txt", "w")

        matrix = generation[i].type_chart

        for row in matrix:
            fichier.write(' '.join([str(a) for a in row]) + '\n')

        write_pokemon_description(fichier, generation[i])

        fichier.close()

def save_ind(individu, name = "stock.txt"):

    fichier = open(name, "w")

    matrix = individu.type_chart

    for row in matrix:
        fichier.write(' '.join([str(a) for a in row]) + '\n')

    write_pokemon_description(fichier, individu)

    fichier.close()


#generation = IA.Generation
#save_gen(generation)

save_ind(IA.test1, "test1.txt")
save_ind(IA.test2, "test2.txt")
save_ind(IA.test3, "test3.txt")
save_ind(IA.test4, "test4.txt")









