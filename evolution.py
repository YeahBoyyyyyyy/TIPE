import IATableDesTypes as IA
import numpy as np
import os
from Stockage_individus import load
from Stockage_individus import save
import pandas as pd
import matplotlib.pyplot as plt

GenCloud = load.get_generation_from_files()
POP_SIZE = 100
N_GENERATIONS = 200

def selection(gen):
    # Tri des individus par fitness
    IA.tri_individus(gen)

    # Croisement et mutation pour créer une nouvelle génération
    new_generation = IA.new_generation(gen)

    return new_generation

def evolution(gen, int):

    population = gen

    for k in range(int):
        print("--------------------------GENERATION " + str(k) + "--------------------------")
        IA.fight_generation(population, k)
        population = selection(population)
        
    os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Stockage_individus/Final_Gen")
    save.final_save_gen(population)
    os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE")

generation = [IA.simplepokemon() for _ in range(POP_SIZE)]
historique = []

def selection_evolution(gen):

    population = gen

    IA.fight_generation(population)

    improve = 0
    nb_of_no_improve = 0
    chance_mutation = IA.MUTATION_CHANCE

    # Suivi
    for g in range(N_GENERATIONS):
        print("--------------------------GENERATION " + str(g) + "--------------------------")
        IA.tri_individus(population)

        fitness_max = population[0].fitness

        c = [IA.type_chart_evaluation(population[i]) for i in range(len(population))]
        correspondance_max = max(c)

        correspondance_premier = IA.type_chart_evaluation(population[0])
        correspondance_deuxieme = IA.type_chart_evaluation(population[1])

        new_improve = np.mean([correspondance_deuxieme, correspondance_premier])

        if g == 0:
            pass
        else:
            if new_improve <= improve:
                nb_of_no_improve += 1
            else:
                improve = new_improve
                nb_of_no_improve = 0

        if nb_of_no_improve > 6:
            chance_mutation = IA.MUTATION_CHANCE
        elif nb_of_no_improve > 4:
            chance_mutation = 0.04
        elif nb_of_no_improve > 3:
            chance_mutation = 0.02
        else:
            chance_mutation = IA.MUTATION_CHANCE

        

        print(f"Correspondance_max : {round(correspondance_max, 4)} | Correspondance : 1er : {round(correspondance_premier, 4)} | 2e : {round(correspondance_deuxieme, 4)} - Génération {g} -  Mutation : {chance_mutation} - NB of no improve : {nb_of_no_improve} - Improve : {round(improve, 4)}")

        historique.append({
            "generation": g,
            "correspondance_max": correspondance_max,
            "correspondance_premier": correspondance_premier,
            "mutation_rate": chance_mutation
    })
    
        population = IA.new_generation(population, chance_mutation)

        # La génération recombat
        IA.fight_generation(population)

    os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Stockage_individus/Final_Gen")
    save.final_save_gen(population)
    os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE")

selection_evolution(generation)

# Pour éviter que les individus stagent trop il faudrait augmenter le taux de mutation si la fitness stagne pendant 
# environ 5 générations, on le change beaucoup pour la génération suivante afin de récréer de la disparité parmi les individus

gen = load.get_generation_from_files_final()

for i in range(len(gen)):
    print(IA.type_chart_evaluation(gen[i]))


df_historique = pd.DataFrame(historique)

plt.figure(figsize=(12, 6))
plt.plot(df_historique["generation"], df_historique["correspondance_max"], label="Correspondance max", color="blue")
plt.plot(df_historique["generation"], df_historique["correspondance_premier"], label="Correspondance Permier", color="green")
plt.plot(df_historique["generation"], df_historique["mutation_rate"], label="Taux de mutation", color="orange", linestyle='--')

plt.title("Évolution de la fitness et du taux de mutation")
plt.xlabel("Génération")
plt.ylabel("Valeurs")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("courbe_evolution.png")
plt.show()
