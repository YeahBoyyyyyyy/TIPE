import numpy as np
import matplotlib.pyplot as plt
from enum import IntEnum
import random
import donnees

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

def damageSingleType(attack_used, pokemon_damaged):
    pokemon_damaged.hp = pokemon_damaged.hp - attack_used[0]*mono_type_attack_effectiveness(attack_used[1], pokemon_damaged.type)
    return pokemon_damaged

def mono_type_attack_effectiveness(offensive_type, defensive_type):
    ID_offensive_type = donnees.POKEMON_TYPES_ID[str(offensive_type)]
    ID_defensive_type = donnees.POKEMON_TYPES_ID[str(defensive_type)]
    return donnees.type_chart[ID_offensive_type][ID_defensive_type]

def stab_attack(attack_used, pokemon):
    r = 1
    if attack_used[1] == pokemon.type:
        r = 1.5
    return r
# Création d'un pokémon très simple avec juste des points de vie (de base 200), 
# un type (au hasard de base) et des attaques (au hasard de base)
class simplepokemon():
    def __init__(self, name = "Null", hp = 200, type = randomType(), attacks = [simpleAttack() for i in range(NUMBER_OF_ATTACKS)]):
        self.name = name
        self.hp = hp
        self.type = type
        self.attacks = attacks
    def __call__(self):
        return self.name, self.hp, self.type, self.attacks

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

# Génération d'une table des types totalement aléatoire 
def generateTypeChart():
    values = [0, 0.5, 1, 2]
    weights = [0.05, 0.20, 0.55, 0.20]

    matrix = [[random.choices(values, weights)[0] for _ in range(18)] for _ in range(18)]
    
    return matrix

Pikachu = simplepokemon("Pikachu",200, "Electric", [(50, "Electric"), (50, "Steel"), (50, "Normal"), (50, "Ground")])

print(Pikachu())
damageSingleType(Pikachu.attacks[3],Pikachu)
print(Pikachu())

# les inputs seraient : 
# - les types du pokémon en face 
# - Les attaques du pokémon joué : type et puissance
# - Pas encore le type du pokémon joué (on ne considère pas le STAB encore)

#Pour l'IA sur la table des types, il faudrait générer une génération de pokémon (avec une capacité ?),



















# Pour la création du choix des capacités par l'IA il faudrait
# prendre en entrée tous les types du jeu mais les connexions qui seraient créées s'activerait seulement 
# lorsque le pokémon en face est du type présent sur la connexion


