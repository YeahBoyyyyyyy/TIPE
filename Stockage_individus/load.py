import sys
import os
sys.path.append("C:/Users/natha/OneDrive/Desktop/Travail/TIPE")
import IATableDesTypes as IA
import donnees
import numpy as np
import save

os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Stockage_individus")

def import_type_chart_1(name):
    with open(name, 'r') as fichier:
        matrix_from_file = [list(map(float, line.split())) for _,line in zip(range(18),fichier)]
    return matrix_from_file

def import_type_chart_2(fichier):
    matrix_from_file = [list(map(float, line.split())) for _,line in zip(range(18),fichier)]
    return matrix_from_file

def import_pokemon_description(name):
    pokemon = IA.simplepokemon()
    with open(name, 'r') as fichier:
        lines = fichier.readlines()
        for line in lines:
            if line.startswith("Nom:"):
                name = line.split(":")[1].strip()
                pokemon.name = name
            
            elif line.startswith("Type:"):
                type = line.split(":")[1].strip()
                pokemon.type = type
            
            elif line.startswith("HP:"):
                hp = int(line.split(":")[1].strip())
                pokemon.hp = hp
            
            elif line.startswith("Attaques:"):
                raw_attacks = line.split(":")[1].strip()
                attack_list = raw_attacks.split(',')

                cleaned_attacks = []

                for item in attack_list:
                    cleaned = item.replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("'", "").strip()
                    cleaned_attacks.append(cleaned)

                attacks = [(int(cleaned_attacks[2*i]), cleaned_attacks[2*i+1]) for i in range(len(cleaned_attacks)//2)]       
                pokemon.attacks = attacks
            
            elif line.startswith("Fitness:"):
                fitness = float(line.split(":")[1].strip())
                pokemon.fitness = fitness
                
    return pokemon

eval_gen = [IA.type_chart_evaluation(import_pokemon_description("stock" + str(i+1) + ".txt")) for i in range(20)]

print(eval_gen)