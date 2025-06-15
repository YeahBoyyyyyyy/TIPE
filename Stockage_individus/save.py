import sys
import os
sys.path.append("C:/Users/natha/OneDrive/Desktop/Travail/TIPE")
import IATableDesTypes as IA
import numpy as np

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
    os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Stockage_individus/Cloud")
    n = len(generation)

    for i in range(n):
        fichier = open("stock" + str(i+1) + ".txt", "w")

        matrix = generation[i].type_chart

        for row in matrix:
            fichier.write(' '.join([str(a) for a in row]) + '\n')

        write_pokemon_description(fichier, generation[i])

        fichier.close()
    os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE")

def save_ind(individu, name = "stock.txt"):
    os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Stockage_individus")

    fichier = open(name, "w")

    matrix = individu.type_chart

    for row in matrix:
        fichier.write(' '.join([str(a) for a in row]) + '\n')

    write_pokemon_description(fichier, individu)

    fichier.close()
    os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE")

## Sauvegarde de la génération après évolution et selection. Ils sont donc supposé être "parfait" et "optimaux"
def final_save_gen(gen):
    os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Stockage_individus/Final_Gen")
    
    n = len(gen)

    for i in range(n):
        fichier = open("stock" + str(i+1) + ".txt", "w")

        matrix = gen[i].type_chart

        for row in matrix:
            fichier.write(' '.join([str(a) for a in row]) + '\n')

        write_pokemon_description(fichier, gen[i])
        print(f"Création du fichier : stock{i+1}.txt")

        fichier.close()

    os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE")

"""
save_ind(IA.test1, "x2.txt")
save_ind(IA.test2, "x0,5.txt")
save_ind(IA.test3, "x1.txt")
save_ind(IA.test4, "x0.txt")
"""








