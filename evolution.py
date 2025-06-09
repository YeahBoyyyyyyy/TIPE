import IATableDesTypes as IA
import numpy as np
import os
import donnees 
from Stockage_individus import load
from Stockage_individus import save
import pandas as pd
import matplotlib.pyplot as plt

GenCloud = load.get_generation_from_files()
POP_SIZE = 50
N_GENERATIONS = 200

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

generation = [IA.simplepokemon() for _ in range(POP_SIZE)]
historique = []

def selection_evolution(gen):

    population = gen
    evo = IA.EvolutionManager(mutation_base=0.004)

    # Suivi
    for g in range(N_GENERATIONS):
        print("--------------------------GENERATION " + str(g) + "--------------------------")
        IA.fight_generation(population)
        IA.tri_individus(population)
        
        fitness_max = population[0].fitness
        fitness_moy = sum(ind.fitness for ind in population) / len(population)

        print(f"Génération {g} - Fitness max : {fitness_max:.2f} | Moyenne : {fitness_moy:.2f} | Mutation : {evo.mutation_rate:.3f}")

        historique.append({
            "generation": g,
            "fitness_max": fitness_max,
            "fitness_moy": fitness_moy,
            "mutation_rate": evo.mutation_rate
    })
    
        evo.update(fitness_max)
        population = IA.new_generation(population, mutation_rate=evo.mutation_rate)

    os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Stockage_individus/Final_Gen")
    save.final_save_gen(population)
    os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE")

selection_evolution(generation)

gen = load.get_generation_from_files_final()

for i in range(len(gen)):
    print(IA.type_chart_evaluation(gen[i]))


df_historique = pd.DataFrame(historique)

plt.figure(figsize=(12, 6))
plt.plot(df_historique["generation"], df_historique["fitness_max"], label="Fitness max", color="blue")
plt.plot(df_historique["generation"], df_historique["fitness_moy"], label="Fitness moyenne", color="green")
plt.plot(df_historique["generation"], df_historique["mutation_rate"], label="Taux de mutation", color="orange", linestyle='--')

plt.title("Évolution de la fitness et du taux de mutation")
plt.xlabel("Génération")
plt.ylabel("Valeurs")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("courbe_evolution.png")
plt.show()
