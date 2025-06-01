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
ZERO = 0
HALF = 1/2
DOUBLE = 2
MUTATION_CHANCE = 0.001

# Choisi un type au hasard parmis les 18 types du jeu
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

# Parcours la table des types du pokemon et génère des mutations
def mutation_type_chart(pokemon):
    chart = pokemon.type_chart
    L = [0, 0.5, 1, 2]
    for i in range(18):
        for j in range(18):
            if random.random() <= MUTATION_CHANCE:
                r = random.randint(1,4)
                chart[i][j] = L[r-1]
    pokemon.type_chart = chart
    return pokemon

def crossover(bestparent:simplepokemon, badparent:simplepokemon):
    child = simplepokemon()
    chart1 = bestparent.type_chart
    chart2 = badparent.type_chart
    for i in range(18):
        for j in range(18):
            r = random.random()
            if r < 0.66:
                child.type_chart[i][j] = chart1[i][j]
            else:
                child.type_chart[i][j] = chart2[i][j]
    return child

# Fait combattre une chaque individus d'une génération contre 100 pokémons simples 
def fight_generation(gen):
    for i in range(len(gen)):
        for j in range(500):
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


def new_generation(gen):
    # Crée une nouvelle génération à partir de la génération actuelle
    new_gen = []
    gen[0].fitness = 0
    gen[1].fitness = 0
    # On garde les deux meilleurs individus de la génération actuelle
    new_gen.append(gen[0])
    new_gen.append(gen[1])
    gen.pop(0)
    gen.pop(0)
    # On croise les 3/5 meilleurs et un random avec le meilleur, et les 2/5-1 avec le deuxieme 
    for i in range(int(len(gen) * 0.6)):
        parent1 = new_gen[0]
        parent2 = gen[0]
        child = crossover(parent1, parent2)
        child = mutation_type_chart(child)
        new_gen.append(child)
        gen.remove(parent2)
    for i in range(int(len(gen))):
        parent1 = new_gen[1]
        parent2 = gen[0]
        child = crossover(parent1, parent2)
        child = mutation_type_chart(child)
        new_gen.append(child)
        gen.remove(parent2)
    return new_gen

# Peut etre separer la table en chunks
# victoire / degat infligés / degats subis (les traités séparément et mieux définir ce qu'est le cas "1.0")

# Création d'un nouveau fitness en fonction des dégâts subits, infligés et du nombre de victoire


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


'''
# ----------------------------------------------------- #
amogus = simplepokemon()
pupute = simplepokemon()
pupute.type_chart = donnees.type_chart

def combats(pokemon,n):
    for i in range(n):
        fight(pokemon, simplepokemon())

number = 1000

combats(amogus, number)
combats(pupute, number)

new_fitness(amogus, number)
new_fitness(pupute, number)

print(f"{bcolors.OKBLUE}AMOGUS : {bcolors.ENDC}" + str(amogus) + f" {bcolors.OKYELLOW}{str(type_chart_evaluation(amogus))}{bcolors.ENDC} --- {bcolors.OKGREEN}{str(amogus.fitness)}{bcolors.ENDC}")
print(f"{bcolors.OKBLUE}PUPUTE : {bcolors.ENDC}" + str(pupute) + f" {bcolors.OKYELLOW}{str(type_chart_evaluation(pupute))}{bcolors.ENDC} --- {bcolors.OKGREEN}{str(pupute.fitness)}{bcolors.ENDC}")
# ----------------------------------------------------- #'''
"""
groscaca = simplepokemon()
groscaca.type_chart = donnees.type_chart 

for i in range(20):
    combats(groscaca)
"""
# Pour la création du choix des capacités par l'IA il faudrait
# prendre en entrée tous les types du jeu mais les connexions qui seraient créées s'activerait seulement 
# lorsque le pokémon en face est du type présent sur la connexion

class complexAttack():
    def __init__(self, name="Null", power=50, attack_type="Normal", category="Physical", effects=None):
        """
        Initialize a complex attack.
        :param name: Name of the attack.
        :param power: Base power of the attack.
        :param attack_type: Type of the attack (e.g., "Fire", "Water").
        :param category: Category of the attack ("Physical" or "Special").
        :param effects: Dictionary of additional effects (e.g., {"flinch": 0.1, "burn": 0.2}).
        """
        self.name = name
        self.power = power
        self.attack_type = attack_type
        self.category = category
        self.effects = effects if effects else {}

    def apply_effects(self, target):
        """
        Apply effects of the attack to the target.
        :param target: The target Pokémon.
        """
        for effect, probability in self.effects.items():
            if random.random() < probability:
                if effect == "flinch":
                    target.flinched = True
                elif effect == "burn":
                    target.status = "Burned"
                elif effect == "paralyze":
                    target.status = "Paralyzed"
                elif effect == "heal":
                    target.hp = min(target.hp + self.power // 2, 200)  # Heal up to half the power, max HP is 200
                # Add more effects as needed

    def __call__(self):
        return self.name, self.power, self.attack_type, self.category, self.effects

def stab_attack(attack_used, pokemon):
    r = 1
    if attack_used[1] == pokemon.type:
        r = 1.5
    return r

class complexpokemon():
    def __init__(self, name="Null", hp=200, type=randomType(), attacks=[simpleAttack() for i in range(NUMBER_OF_ATTACKS)], abilities=[], level=1, experience=0, stats=None, status=None, nature=None, held_item=None):
        """
        Initialize a complex Pokémon with various attributes.
        :param name: Name of the Pokémon.
        :param hp: Hit points of the Pokémon.
        :param type: Type of the Pokémon.
        :param attacks: List of attacks the Pokémon can use.
        :param abilities: List of abilities the Pokémon has.
        :param level: Level of the Pokémon.
        :param experience: Experience points of the Pokémon.
        :param stats: Dictionary of stats (e.g., {"attack": 50, "defense": 40, "speed": 60}).
        :param status: Current status condition (e.g., "Burned", "Paralyzed").
        :param nature: Nature of the Pokémon (e.g., "Adamant", "Timid").
        :param held_item: Item the Pokémon is holding.
        """
        self.name = name
        self.hp = hp
        self.type = type
        self.attacks = attacks
        self.abilities = abilities
        self.level = level
        self.experience = experience
        self.stats = stats if stats else {"attack": 50, "defense": 50, "speed": 50, "special_attack": 50, "special_defense": 50}
        self.status = status
        self.nature = nature
        self.held_item = held_item

    def __call__(self):
        return {
            "name": self.name,
            "hp": self.hp,
            "type": self.type,
            "attacks": self.attacks,
            "abilities": self.abilities,
            "level": self.level,
            "experience": self.experience,
            "stats": self.stats,
            "status": self.status,
            "nature": self.nature,
            "held_item": self.held_item,
        }