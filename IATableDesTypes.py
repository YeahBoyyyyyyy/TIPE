import numpy as np
from enum import IntEnum
import random
import donnees
import os
from Stockage_individus import load
import json

class bcolors:
    OKWHITE = '\033[97m'
    OKBLACK = '\033[30m'
    OKRED = '\033[91m'
    OKORANGE = '\033[38;5;208m'
    OKYELLOW = '\033[93m'
    OKPINK = '\033[95m'
    OKPURPLE = '\033[95m'
    OKMAGENTA = '\033[35m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNBOLD = '\033[22m'
    UNDERLINE = '\033[4m'

NUMBER_OF_ATTACKS = 10
NUMBER_OF_FIGHT = 3000
ZERO = 0
HALF = 1/2
DOUBLE = 2
MUTATION_CHANCE = 0.005

# Choisir un type au hasard parmi les 18 types du jeu
def randomType():
    return donnees.POKEMON_TYPES[random.randint(0,17)]

# Genère une attaque simple de 50 de puissance, d'un certain type et sans effets spéciaux 
def simpleAttack():
    return (50, randomType())

# Création d'un pokémon très simple avec juste des points de vie (de base 200), 
# un type (au hasard de base) et des attaques (au hasard de base)
class simplepokemon():
    def __init__(self, name="Null", hp=200, type=None, attacks=None, fitness=0):
        if type is None:
            type = randomType()
        if attacks is None:
            attacks = [simpleAttack() for i in range(NUMBER_OF_ATTACKS)]
        
        self.name = name
        self.hp = hp
        self.type = type
        self.attacks = attacks
        self.fitness = fitness
        self.type_chart = generateTypeChart()
        self.number_of_damage_taken = 0
        self.number_of_damage_dealt = 0
        self.number_of_victories = 0
    def __call__(self):
        return self.name, self.hp, self.type, self.attacks, self.fitness, self.number_of_damage_dealt, self.number_of_damage_taken, self.number_of_victories
    def __str__(self): 
        return f"{self.name} (HP: {self.hp}, Type: {self.type}), Fitness: {self.fitness}, Damage Dealt: {self.number_of_damage_dealt}, Damage Taken: {self.number_of_damage_taken}, Victories: {self.number_of_victories})"
 

def damageSingleType(attack_used, pokemon_damaged):
    pokemon_damaged.hp = pokemon_damaged.hp - attack_used[0]*mono_type_attack_effectiveness(attack_used[1], pokemon_damaged.type)
    return pokemon_damaged

def mono_type_attack_effectiveness(offensive_type, defensive_type):
    ID_offensive_type = donnees.POKEMON_TYPES_ID[str(offensive_type)]
    ID_defensive_type = donnees.POKEMON_TYPES_ID[str(defensive_type)]
    return donnees.type_chart[ID_offensive_type][ID_defensive_type]

# Génération d'une table des types totalement aléatoire 
def generateTypeChart():
    values = [0, 0.5, 1, 2]
    weights = [0.020, 0.2025, 0.55, 0.20]

    matrix = [[random.choices(values, weights)[0] for _ in range(18)] for _ in range(18)]
    
    return matrix

# les inputs seraient : 
# - les types du pokémon en face 
# - Les attaques du pokémon joué : type et puissance
# - Pas encore le type du pokémon joué (on ne considère pas le STAB encore)

#Pour l'IA sur la table des types, il faudrait générer une génération de pokémon (avec une capacité ?),

## Foncion pour faire combattre un pokémon contre un autre pokémon

def simplePokemonWeakness(pokemon, typechart):
    type = pokemon.type
    weakness = []
    for i in range(18):
        if typechart[i][donnees.POKEMON_TYPES_ID[type]] == 2:
            weakness.append(donnees.POKEMON_TYPES[i])
    return weakness

def simplePokemonResistance(pokemon, typechart):
    type = pokemon.type
    resistance = []
    for i in range(18):
        if typechart[i][donnees.POKEMON_TYPES_ID[type]] == 0.5:
            resistance.append(donnees.POKEMON_TYPES[i])
    return resistance

def simplePokemonNeutrality(pokemon, typechart):
    type = pokemon.type
    neutrality = []
    for i in range(18):
        if typechart[i][donnees.POKEMON_TYPES_ID[type]] == 1:
            neutrality.append(donnees.POKEMON_TYPES[i])
    return neutrality

def simplePokemonImmunities(pokemon, typechart):
    type = pokemon.type
    immunities = []
    for i in range(18):
        if typechart[i][donnees.POKEMON_TYPES_ID[type]] == 0:
            immunities.append(donnees.POKEMON_TYPES[i])
    return immunities

def selectAttack(pokemon, opponent):
    # Choisir une attaque en fonction de la faiblesse du pokémon adverse
    weaknesses = simplePokemonWeakness(opponent, pokemon.type_chart)
    neutrality = simplePokemonNeutrality(opponent, pokemon.type_chart)
    for attack in pokemon.attacks:
        if attack[1] in weaknesses:
            return attack
        elif attack[1] in neutrality:
            return attack
    # Si aucune attaque ne correspond à la faiblesse, choisir une attaque aléatoire
    return pokemon.attacks[random.randint(0, NUMBER_OF_ATTACKS-1)]

def selectAttackDefense(pokemon, opponent):
    # Choisir une attaque en fonction de la faiblesse du pokémon adverse
    immunities = simplePokemonImmunities(opponent, opponent.type_chart)
    resistance = simplePokemonResistance(opponent, opponent.type_chart)
    for attack in pokemon.attacks:
        if attack[1] in immunities:
            return attack
        elif attack[1] in resistance:
            return attack
    # Si aucune attaque ne correspond à la faiblesse, choisir une attaque aléatoire
    return pokemon.attacks[random.randint(0, NUMBER_OF_ATTACKS-1)]

def fitnessGainAttack(pokemon, attack_used, opponent):
    effectivness = mono_type_attack_effectiveness(attack_used[1], opponent.type)
    if effectivness == 2:
        pokemon.fitness += 150
    elif effectivness == 0.5:
        pokemon.fitness -= 50
    elif effectivness == 0:
        pokemon.fitness -= 100

def fitnessGainDefense(pokemon, attack_used):
    effectivness = mono_type_attack_effectiveness(attack_used[1], pokemon.type)
    if effectivness == 2:
        pokemon.fitness -= 150
    elif effectivness == 0.5:
        pokemon.fitness += 50
    elif effectivness == 0:
        pokemon.fitness += 100

def type_chart_evaluation(pokemon):
    IA_type_chart = pokemon.type_chart
    evaluation = 0
    for i in range(18):
        for j in range(18):
            if IA_type_chart[i][j] == donnees.type_chart[i][j]:
                evaluation += 1
    return (evaluation/324)

def fight(pokemon1, pokemon2):
    # print(pokemon2())

    compteur = 0

    while pokemon1.hp > 0 and pokemon2.hp > 0 and compteur <= 15:
        
        # ---------------------- Tour du pokémon IA ------------------------- #

        attack_used = selectAttack(pokemon1, pokemon2)  # Choisir une attaque en fonction de la faiblesse du pokémon adverse
        damageSingleType(attack_used, pokemon2)
        
        ######## Gain de fitness et gain de damage dealt
        pokemon1.number_of_damage_dealt += attack_used[0]*mono_type_attack_effectiveness(attack_used[1], pokemon2.type)
        # fitnessGainAttack(pokemon1, attack_used, pokemon2)

        
        # ------------- Print the description of the attack used with colored pokemon names to the text ------------- #
        # print(f"{bcolors.OKBLUE}{pokemon1.name}{bcolors.ENDC} used {attack_used[1]} attack on {bcolors.OKGREEN}{pokemon2.name}." + bcolors.ENDC)

        if pokemon2.hp <= 0:
            # print(f"{bcolors.OKBLACK}{pokemon2.name} fainted!" + bcolors.ENDC)
            # pokemon1.fitness += 20  # Gain fitness for knocking out the opponent
            pokemon1.number_of_victories += 1
            break


        # ---------------------- Tour du pokémon adverse ------------------------- #

        attack_used = selectAttackDefense(pokemon2, pokemon1)  # Choisir une attaque en fonction de la résistance du pokémon adverse
        damageSingleType(attack_used, pokemon1)

        ######## Gain de fitness et gain de damage taken
        pokemon1.number_of_damage_taken += attack_used[0]*mono_type_attack_effectiveness(attack_used[1], pokemon1.type)
        # fitnessGainDefense(pokemon1, attack_used)
        
        # ------------- Print the description of the attack used with colors to the text ------------- #
        # print(f"{bcolors.OKGREEN}{pokemon2.name}{bcolors.ENDC} used {attack_used[1]} attack on {bcolors.OKBLUE}{pokemon1.name}." + bcolors.ENDC)

        if pokemon1.hp <= 0:
            # print(f"{bcolors.OKGREEN}{pokemon1.name} fainted!" + bcolors.ENDC)
            # pokemon1.fitness -= 100  # Loss of fitness for being knocked out
            break

        compteur += 1

    pokemon1.hp = 200  # Reset HP for the next fight
    pokemon1.type = randomType() # Randomise le type pour pouvoir permettre d'utilliser d'autres attaques après
    pokemon1.attacks = [simpleAttack() for i in range(NUMBER_OF_ATTACKS)] # randomise les attaques pour faire varier les choix
    return pokemon1     

    # Générer une liste de 20 pokémons différents

class EvolutionManager:
    def __init__(self, mutation_base=0.01, max_no_improve=5, mutation_step=0.002):
        self.best_fitness = None
        self.no_improve_count = 0
        self.mutation_rate = mutation_base
        self.max_no_improve = max_no_improve
        self.mutation_step = mutation_step
        self.min_mutation = 0.002
        self.max_mutation = 0.3

    def update(self, current_best_fitness):
        if self.best_fitness is None or current_best_fitness > self.best_fitness:
            self.best_fitness = current_best_fitness
            self.no_improve_count = 0
            self.mutation_rate -= 0.001
        else:
            self.no_improve_count += 1
            if self.no_improve_count >= self.max_no_improve:
                self.mutation_rate = min(self.mutation_rate + self.mutation_step, self.max_mutation)
                self.no_improve_count = 0

# Parcours la table des types du pokemon et génère des mutations
def static_mutation_type_chart(pokemon):
    chart = pokemon.type_chart
    L = [0, 0.5, 1, 2]
    for i in range(18):
        for j in range(18):
            if random.random() <= MUTATION_CHANCE:
                r = random.randint(1,4)
                chart[i][j] = L[r-1]
    pokemon.type_chart = chart
    return pokemon

def mutation_type_chart(pokemon, mutation_rate=0.005):
    chart = pokemon.type_chart
    L = [0, 0.5, 1, 2]
    mutated = 0
    for i in range(18):
        for j in range(18):
            if mutated > 15 : break
            if random.random() <= mutation_rate:
                chart[i][j] = random.choice(L)
                mutated += 1

    pokemon.type_chart = chart
    return pokemon

def crossover(bestparent:simplepokemon, badparent:simplepokemon):
    child = simplepokemon()
    chart1 = bestparent.type_chart
    chart2 = badparent.type_chart
    for i in range(18):
        for j in range(18):
            r = random.random()
            if r < 0.60:
                child.type_chart[i][j] = chart1[i][j]
            else:
                child.type_chart[i][j] = chart2[i][j]
    return child

# Fait combattre une chaque individus d'une génération contre NB_OF_FIGHT pokémons simples 
def fight_generation(gen):
    for i in range(len(gen)):
        for j in range(NUMBER_OF_FIGHT):
            gen[i].hp = 200
            try:
                fight(gen[i], simplepokemon())
            except Exception as e:
                print(f"Erreur pendant le combat {j} du pokemon {i}: {e}")
                break

def tri_individus(gen):
    # normalisation de la génération
    normalize_generation(gen)
    # Trie la génération d'individus par fitness
    n = len(gen)
    for i in range(n):
        for j in range(n-i-1):
            if gen[j].fitness < gen[j+1].fitness:
                gen[j], gen[j+1] = gen[j+1], gen[j]

def tri_individus_en_fonction_de_la_type_chart_directement(gen):
    n = len(gen)
    for i in range(n):
        for j in range(n-i-1):
            if type_chart_evaluation(gen[j]) < type_chart_evaluation(gen[j+1]):
                gen[j], gen[j+1] = gen[j+1], gen[j]

def normalize_generation(generation):
    # Récupérer les valeurs brutes
    damage_dealts = [ind.number_of_damage_dealt for ind in generation]
    damage_takens = [ind.number_of_damage_taken for ind in generation]
    nb_victories = [ind.number_of_victories for ind in generation]

    # Éviter la division par zéro
    def min_max(val, min_val, max_val):
        if max_val - min_val == 0:
            return 0.0
        return (val - min_val) / (max_val - min_val)

    # Calcul des min/max
    min_dealt, max_dealt = min(damage_dealts), max(damage_dealts)
    min_taken, max_taken = min(damage_takens), max(damage_takens)
    min_victories, max_victories = min(nb_victories), max(nb_victories)

    # Construction de la fitness normalisée avec les mêmes poids
    for ind in generation:
        norm_dealt = min_max(ind.number_of_damage_dealt, min_dealt, max_dealt)
        norm_taken = min_max(ind.number_of_damage_taken, min_taken, max_taken)
        norm_victories = min_max(ind.number_of_victories, min_victories, max_victories)

        # Attention : on inverse damage_taken car moins = mieux
        ind.fitness = (
            0.20 * norm_dealt +
            0.5 * (1 - norm_taken) +
            0.30 * norm_victories
        )





def new_generation(generation, mutation_rate=MUTATION_CHANCE):
    gen = generation.copy()
    tri_individus(gen)  # Trie la génération selon le fitness (meilleurs en premier)
    new_gen = []

    # Élitisme : on garde les deux meilleurs individus sans modification
    best1 = gen[0]
    best2 = gen[1]
    best1.fitness = 0
    best2.fitness = 0
    new_gen.append(best1)
    new_gen.append(best2)
    gen = gen[2:]

    # Sélection par tournoi : on sélectionne les meilleurs parents pour croisement
    top_percent = int(len(gen) * 0.3) if len(gen) > 3 else len(gen)
    parents_pool = gen[:top_percent]

    # Générer des enfants par croisement entre les meilleurs parents (favorise la diversité)
    while len(new_gen) < len(generation):
        parent1 = random.choice([best1, best2] + parents_pool)
        parent2 = random.choice(parents_pool)
        if parent1 == parent2:
            parent2 = simplepokemon()  # Diversité si même parent
        child = crossover(parent1, parent2)
        child = mutation_type_chart(child, mutation_rate)
        new_gen.append(child)

    # S'assurer que la taille de la génération reste constante
    return new_gen[:len(generation)]

pupute_gang = [simplepokemon() for _ in range(50)]

fight_generation(pupute_gang)

tri_individus(pupute_gang)

for i in range(len(pupute_gang)):
   print(f"fitness : {pupute_gang[i].fitness}")
   print(f"correspondance : {type_chart_evaluation(pupute_gang[i])}")
   print("-------------------------------------")

"""
def normalize_damage_dealts(value, moyenne, SD):
    if SD == 0:
        return 0
    return (value - moyenne) / SD

def normalize_damage_takens(value, moyenne, SD):
    if SD == 0:
        return 0
    return (value - moyenne) / SD

def normalize_nb_victories(value, moyenne, SD):
    if SD == 0:
        return 0
    return (value - moyenne) / SD

def normalize_generation(generation):
    # Normalise les dégâts infligés, subis et le nombre de victoires
    damage_dealts = [individu.number_of_damage_dealt for individu in generation]
    damage_takens = [individu.number_of_damage_taken for individu in generation]
    nb_victories = [individu.number_of_victories for individu in generation]

    moyenne_damage_dealts = np.mean(damage_dealts)
    SD_damage_dealts = np.std(damage_dealts)

    moyenne_damage_takens = np.mean(damage_takens)
    SD_damage_takens = np.std(damage_takens)

    moyenne_nb_victories = np.mean(nb_victories)
    SD_nb_victories = np.std(nb_victories)

    # Normalisation des dégâts infligés, subis et du nombre de victoires pour former le fitness avec un poids de 0.6 pour les 
    # dégâts subits, 0,25 pour les victoires et 0.15 pour les dégâts infligés
    for individu in generation:
        # Pour les dégâts subis (damage_taken), moins il y en a, mieux c'est, donc on oppose la normalisation
        individu.fitness = (
            0.15 * normalize_damage_dealts(individu.number_of_damage_dealt, moyenne_damage_dealts, SD_damage_dealts) +
            0.6 * -normalize_damage_takens(individu.number_of_damage_taken, moyenne_damage_takens, SD_damage_takens) +
            0.25 * normalize_nb_victories(individu.number_of_victories, moyenne_nb_victories, SD_nb_victories)
        )
"""
# Pour la création du choix des capacités par l'IA il faudrait
# prendre en entrée tous les types du jeu mais les connexions qui seraient créées s'activerait seulement 
# lorsque le pokémon en face est du type présent sur la connexion
