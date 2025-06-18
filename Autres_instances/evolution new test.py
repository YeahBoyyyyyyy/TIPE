import IATDTnew as IA
import numpy as np
import os
os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Autres_instances")
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import logging

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("evolution.log", mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

POP_SIZE = 60
N_GENERATIONS = 100
        
generation = [IA.simplepokemon() for _ in range(POP_SIZE)]
historique = []
# freq_map[i][j] = dict {0: count, 0.5: count, ...}
freq_map = [[defaultdict(int) for _ in range(18)] for _ in range(18)]

def selection_evolution(gen):

    population = gen

    population = IA.fight_generation_parallel(population)

    improve = 0
    nb_of_no_improve = 0
    chance_mutation = IA.MUTATION_CHANCE

    # Suivi
    for g in range(N_GENERATIONS):
        print(f"\n--- Génération {g}/{N_GENERATIONS} ---", flush=True)
        IA.tri_individus(population)

        top_k = 3  # top 3 individus
        for p in population[:top_k]:
            for i in range(18):
                for j in range(18):
                    val = p.type_chart[i][j]
                    freq_map[i][j][val] += 1

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

        if nb_of_no_improve > 9:
            chance_mutation = IA.MUTATION_CHANCE
        elif nb_of_no_improve > 8:
            chance_mutation = 0.06
        elif nb_of_no_improve > 5 :
            chance_mutation = 0.01
        else:
            chance_mutation = IA.MUTATION_CHANCE

        logger.info(f"Correspondance_max : {round(correspondance_max, 4)} | Correspondance : 1er : {round(correspondance_premier, 4)} | 2e : {round(correspondance_deuxieme, 4)} - Génération {g} -  Mutation : {chance_mutation} - NB of no improve : {nb_of_no_improve} - Improve : {round(improve, 4)}")

        historique.append({
            "generation": g,
            "correspondance_max": correspondance_max,
            "correspondance_premier": correspondance_premier,
            "mutation_rate": chance_mutation
    })
    
        population = IA.new_generation(population, freq_map, g, chance_mutation)

        # La génération recombat
        population = IA.fight_generation_parallel(population)
    return population

def main():
    pop = selection_evolution(generation)

    for i in range(len(pop)):
        print(IA.type_chart_evaluation(pop[i]))

    df_historique = pd.DataFrame(historique)

    plt.figure(figsize=(12, 6))
    plt.plot(df_historique["generation"], df_historique["correspondance_max"], label="Correspondance max", color="blue")
    plt.plot(df_historique["generation"], df_historique["correspondance_premier"], label="Correspondance Premier", color="green")
    plt.plot(df_historique["generation"], df_historique["mutation_rate"], label="Taux de mutation", color="orange", linestyle='--')

    plt.title("Évolution de la fitness et du taux de mutation")
    plt.xlabel("Génération")
    plt.ylabel("Valeurs")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("courbe_evolution.png")
    plt.show()


if __name__ == "__main__":
    main()