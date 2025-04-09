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

def damage(attack_used, pokemon_damaged):
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

# Génération d'une table des types totalement aléatoire 
def generateTypeChart():
    values = [0, 0.5, 1, 2]
    weights = [0.05, 0.20, 0.55, 0.20]

    matrix = [[random.choices(values, weights)[0] for _ in range(18)] for _ in range(18)]
    
    return matrix

Pikachu = simplepokemon("Pikachu",200, "Electric", [(50, "Electric"), (50, "Steel"), (50, "Normal"), (50, "Ground")])

print(Pikachu())
damage(Pikachu.attacks[3],Pikachu)
print(Pikachu())

# les inputs seraient : 
# - les types du pokémon en face 
# - Les attaques du pokémon joué : type et puissance
# - Pas encore le type du pokémon joué (on ne considère pas le STAB encore)

#Pour l'IA sur la table des types, il faudrait générer une génération de pokémon (avec une capacité ?),



















# Pour la création du choix des capacités par l'IA il faudrait
# prendre en entrée tous les types du jeu mais les connexions qui seraient créées s'activerait seulement 
# lorsque le pokémon en face est du type présent sur la connexion


