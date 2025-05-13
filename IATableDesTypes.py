import numpy as np
import matplotlib.pyplot as plt
from enum import IntEnum
import random
import donnees

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

NUMBER_OF_ATTACKS = 4
ZERO = 0
HALF = 1/2
DOUBLE = 2

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
    def __call__(self):
        return self.name, self.hp, self.type, self.attacks, self.fitness
    def __str__(self): 
        return f"{self.name} (HP: {self.hp}, Type: {self.type}, Attacks: {self.attacks})"
 

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
    weights = [0.025, 0.2025, 0.55, 0.20]

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
    resistance = simplePokemonResistance(opponent, pokemon.type_chart)
    for attack in pokemon.attacks:
        if attack[1] in weaknesses:
            return attack
        elif attack[1] in neutrality:
            return attack
    # Si aucune attaque ne correspond à la faiblesse, choisir une attaque aléatoire
    return pokemon.attacks[random.randint(0, NUMBER_OF_ATTACKS-1)]

def fitnessGain(pokemon, attack_used, opponent):
    effectivness = mono_type_attack_effectiveness(attack_used[1], opponent.type)
    if effectivness == 2:
        pokemon.fitness += attack_used[0] * effectivness
    elif effectivness == 0.5:
        pokemon.fitness -= 30
    elif effectivness == 0:
        pokemon.fitness -= 50
    elif effectivness == 1:
        pokemon.fitness += 5

def fight(pokemon1, pokemon2):
    # print(pokemon2())

    while pokemon1.hp > 0 and pokemon2.hp > 0:

        # ---------------------- Tour du pokémon IA ------------------------- #

        attack_used = selectAttack(pokemon1, pokemon2)  # Choisir une attaque en fonction de la faiblesse du pokémon adverse
        damageSingleType(attack_used, pokemon2)
        
        ######## Gain de fitness 
        fitnessGain(pokemon1, attack_used, pokemon2)
        
        # ------------- Print the description of the attack used with colored pokemon names to the text ------------- #
        # print(f"{bcolors.OKBLUE}{pokemon1.name}{bcolors.ENDC} used {attack_used[1]} attack on {bcolors.OKGREEN}{pokemon2.name}." + bcolors.ENDC)

        if pokemon2.hp <= 0:
            # print(f"{bcolors.OKBLACK}{pokemon2.name} fainted!" + bcolors.ENDC)
            pokemon1.fitness += 20  # Gain fitness for knocking out the opponent
            break


        # ---------------------- Tour du pokémon adverse ------------------------- #

        attack_used = pokemon2.attacks[random.randint(0, NUMBER_OF_ATTACKS-1)]
        damageSingleType(attack_used, pokemon1)
        
        # ------------- Print the description of the attack used with colors to the text ------------- #
        # print(f"{bcolors.OKGREEN}{pokemon2.name}{bcolors.ENDC} used {attack_used[1]} attack on {bcolors.OKBLUE}{pokemon1.name}." + bcolors.ENDC)

        if pokemon1.hp <= 0:
            # print(f"{bcolors.OKGREEN}{pokemon1.name} fainted!" + bcolors.ENDC)
            pokemon1.fitness -= 50  # Loss of fitness for being knocked out
            break
    
    pokemon1.hp = 200  # Reset HP for the next fight

    return pokemon1     

    # Générer une liste de 20 pokémons différents

def type_chart_evaluation(pokemon):
    IA_type_chart = pokemon.type_chart
    evaluation = 0
    for i in range(18):
        for j in range(18):
            if IA_type_chart[i][j] == donnees.type_chart[i][j]:
                evaluation += 1
    return evaluation



Generation = [simplepokemon(name= "Individu : "+str(i+1)) for i in range(20)]

for i in range(20):
    for j in range(100):
        fight(Generation[i], simplepokemon())
    















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