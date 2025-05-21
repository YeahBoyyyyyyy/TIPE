import IATableDesTypes as IA
import numpy as np
import os
import donnees 
from Stockage_individus import load
from Stockage_individus import save

Generation = load.get_generation_from_files()

def selection(gen):
    # Tri des individus par fitness
    IA.tri_individus(gen)

    # Croisement et mutation pour créer une nouvelle génération
    new_generation = IA.new_generation(gen)

    return new_generation

def evolution(gen, int):

    population = gen

    for i in range(int):
        print("--------------------------GENERATION " + str(i) + "--------------------------")
        IA.fight_generation(population)
        population = selection(population)
        
    os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Stockage_individus/Final_Gen")
    save.final_save_gen(population)
    os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE")

#evolution(Generation, 500)

"""
for j in range(2):
    IA.fight_generation(Generation)
    #for i in range(20):
     #   print(Generation[i]())

    IA.tri_individus(Generation)

    print(f"-------------------------------TRI GENERATION {j}-------------------------------")
    #for i in range(20):
     #   print(Generation[i]())

    Generation = IA.new_generation(Generation)

    print(f"-------------------------------NOUVELLE GENERATION {j}-------------------------------")

    for i in range(len(Generation)):
        print(Generation[i]())
    print("Nombre d'individus à sauvegarder :", len(Generation))


"""
os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Stockage_individus/Final_Gen")
gen = load.get_generation_from_files()

for i in range(len(gen)):
    print(gen[i].type)
    print(gen[i].name)
    print(IA.type_chart_evaluation(gen[i]))

pok = IA.simplepokemon()
print(IA.type_chart_evaluation(pok))
