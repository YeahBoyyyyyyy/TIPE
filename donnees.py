import numpy as np
from enum import IntEnum
import random 
from time import *

ZERO = 0
HALF = 1/2
DOUBLE = 2

POKEMON_TYPES = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel",
              "Fire", "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark", "Fairy", "Null"]

POKEMON_TYPES_ID = {"Normal":0, "Fighting":1, "Flying":2, "Poison":3, "Ground":4, "Rock":5, "Bug":6, 
                    "Ghost":7, "Steel":8, "Fire":9, "Water":10, "Grass":11, "Electric":12, "Psychic":13, 
                    "Ice":14, "Dragon":15, "Dark":16, "Fairy":17, "Null":18}

type_chart = [
    # Normal  Fight  Fly  Pois  Grou  Rock  Bug   Ghos  Stee  Fire  Wate  Gras  Elec  Psyc  Ice   Drag  Dark  Fair
    [  1.0,   1.0,  1.0,  1.0,  1.0,  0.5,  1.0,  0.0,  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0],  # Normal
    [  2.0,   1.0,  0.5,  0.5,  1.0,  2.0,  0.5,  0.0,  2.0,  1.0,  1.0,  1.0,  1.0,  0.5,  2.0,  1.0,  2.0,  0.5],  # Fighting
    [  1.0,   2.0,  1.0,  1.0,  1.0,  0.5,  2.0,  1.0,  0.5,  1.0,  1.0,  2.0,  0.5,  1.0,  1.0,  1.0,  1.0,  1.0],  # Flying
    [  1.0,   1.0,  1.0,  0.5,  0.5,  0.5,  1.0,  0.5,  0.0,  1.0,  1.0,  2.0,  1.0,  1.0,  1.0,  1.0,  1.0,  2.0],  # Poison
    [  1.0,   1.0,  0.0,  2.0,  1.0,  2.0,  0.5,  1.0,  2.0,  2.0,  1.0,  0.5,  2.0,  1.0,  1.0,  1.0,  1.0,  1.0],  # Ground
    [  1.0,   0.5,  2.0,  1.0,  0.5,  1.0,  2.0,  1.0,  0.5,  2.0,  1.0,  1.0,  1.0,  1.0,  2.0,  1.0,  1.0,  1.0],  # Rock
    [  1.0,   0.5,  0.5,  0.5,  1.0,  1.0,  1.0,  0.5,  0.5,  0.5,  1.0,  2.0,  1.0,  2.0,  1.0,  1.0,  2.0,  0.5],  # Bug
    [  0.0,   1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  2.0,  1.0,  1.0,  1.0,  1.0,  1.0,  2.0,  1.0,  1.0,  0.5,  1.0],  # Ghost
    [  1.0,   1.0,  1.0,  1.0,  1.0,  2.0,  1.0,  1.0,  0.5,  0.5,  0.5,  1.0,  0.5,  1.0,  2.0,  1.0,  1.0,  2.0],  # Steel
    [  1.0,   1.0,  1.0,  1.0,  1.0,  0.5,  2.0,  1.0,  2.0,  0.5,  0.5,  2.0,  1.0,  1.0,  2.0,  0.5,  1.0,  1.0],  # Fire
    [  1.0,   1.0,  1.0,  1.0,  2.0,  2.0,  1.0,  1.0,  1.0,  2.0,  0.5,  0.5,  1.0,  1.0,  1.0,  0.5,  1.0,  1.0],  # Water
    [  1.0,   1.0,  0.5,  0.5,  2.0,  2.0,  0.5,  1.0,  0.5,  0.5,  2.0,  0.5,  1.0,  1.0,  1.0,  0.5,  1.0,  1.0],  # Grass
    [  1.0,   1.0,  2.0,  1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  1.0,  2.0,  0.5,  0.5,  1.0,  1.0,  0.5,  1.0,  1.0],  # Electric
    [  1.0,   2.0,  1.0,  2.0,  1.0,  1.0,  1.0,  1.0,  0.5,  1.0,  1.0,  1.0,  1.0,  0.5,  1.0,  1.0,  0.0,  1.0],  # Psychic
    [  1.0,   1.0,  2.0,  1.0,  2.0,  1.0,  1.0,  1.0,  0.5,  0.5,  0.5,  2.0,  1.0,  1.0,  0.5,  2.0,  1.0,  1.0],  # Ice
    [  1.0,   1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  2.0,  1.0,  0.0],  # Dragon
    [  1.0,   0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  2.0,  1.0,  1.0,  1.0,  1.0,  1.0,  2.0,  1.0,  1.0,  0.5,  0.5],  # Dark
    [  1.0,   2.0,  1.0,  0.5,  1.0,  1.0,  1.0,  1.0,  0.5,  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  2.0,  2.0,  1.0]   # Fairy
]

NUMBER_OF_ATTACKS = 4
def randomType():
    return POKEMON_TYPES[random.randint(0,17)]
def simpleAttack():
    return (50, randomType())
def generateTypeChart():
    values = [0, 0.5, 1, 2]
    weights = [0.05, 0.20, 0.55, 0.20]

    matrix = [[random.choices(values, weights)[0] for _ in range(18)] for _ in range(18)]
    
    return matrix
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
    def __deepcopy__(self):
        return simplepokemon(self.name, self.hp, self.type, self.attacks.copy(), self.fitness)
    
first_gen_pokemon = [
    simplepokemon(name, 200, type, [simpleAttack() for _ in range(NUMBER_OF_ATTACKS)])
    for name, type in [
        ("Bulbizarre", "Grass"),
        ("Herbizarre", "Grass"),
        ("Florizarre", "Grass"),
        ("Salamèche", "Fire"),
        ("Reptincel", "Fire"),
        ("Dracaufeu", "Fire"),
        ("Carapuce", "Water"),
        ("Carabaffe", "Water"),
        ("Tortank", "Water"),
        ("Chenipan", "Bug"),
        ("Chrysacier", "Bug"),
        ("Papilusion", "Bug"),
        ("Aspicot", "Bug"),
        ("Coconfort", "Bug"),
        ("Dardargnan", "Bug"),
        ("Roucool", "Flying"),
        ("Roucoups", "Flying"),
        ("Roucarnage", "Flying"),
        ("Rattata", "Normal"),
        ("Rattatac", "Normal"),
        ("Piafabec", "Flying"),
        ("Rapasdepic", "Flying"),
        ("Abo", "Poison"),
        ("Arbok", "Poison"),
        ("Pikachu", "Electric"),
        ("Raichu", "Electric"),
        ("Sabelette", "Ground"),
        ("Sablaireau", "Ground"),
        ("Nidoran♀", "Poison"),
        ("Nidorina", "Poison"),
        ("Nidoqueen", "Poison"),
        ("Nidoran♂", "Poison"),
        ("Nidorino", "Poison"),
        ("Nidoking", "Poison"),
        ("Mélofée", "Fairy"),
        ("Mélodelfe", "Fairy"),
        ("Goupix", "Fire"),
        ("Feunard", "Fire"),
        ("Rondoudou", "Fairy"),
        ("Grodoudou", "Fairy"),
        ("Nosferapti", "Poison"),
        ("Nosferalto", "Poison"),
        ("Mystherbe", "Grass"),
        ("Ortide", "Grass"),
        ("Rafflesia", "Grass"),
        ("Paras", "Bug"),
        ("Parasect", "Bug"),
        ("Mimitoss", "Bug"),
        ("Aéromite", "Bug"),
        ("Taupiqueur", "Ground"),
        ("Triopikeur", "Ground"),
        ("Miaouss", "Normal"),
        ("Persian", "Normal"),
        ("Psykokwak", "Water"),
        ("Akwakwak", "Water"),
        ("Férosinge", "Fighting"),
        ("Colossinge", "Fighting"),
        ("Caninos", "Fire"),
        ("Arcanin", "Fire"),
        ("Ptitard", "Water"),
        ("Têtarte", "Water"),
        ("Tartard", "Water"),
        ("Abra", "Psychic"),
        ("Kadabra", "Psychic"),
        ("Alakazam", "Psychic"),
        ("Machoc", "Fighting"),
        ("Machopeur", "Fighting"),
        ("Mackogneur", "Fighting"),
        ("Chétiflor", "Grass"),
        ("Boustiflor", "Grass"),
        ("Empiflor", "Grass"),
        ("Tentacool", "Water"),
        ("Tentacruel", "Water"),
        ("Racaillou", "Rock"),
        ("Gravalanch", "Rock"),
        ("Grolem", "Rock"),
        ("Ponyta", "Fire"),
        ("Galopa", "Fire"),
        ("Ramoloss", "Water"),
        ("Flagadoss", "Water"),
        ("Magnéti", "Electric"),
        ("Magnéton", "Electric"),
        ("Canarticho", "Flying"),
        ("Doduo", "Flying"),
        ("Dodrio", "Flying"),
        ("Otaria", "Water"),
        ("Lamantine", "Water"),
        ("Tadmorv", "Poison"),
        ("Grotadmorv", "Poison"),
        ("Kokiyas", "Water"),
        ("Crustabri", "Water"),
        ("Fantominus", "Ghost"),
        ("Spectrum", "Ghost"),
        ("Ectoplasma", "Ghost"),
        ("Onix", "Rock"),
        ("Soporifik", "Psychic"),
        ("Hypnomade", "Psychic"),
        ("Krabby", "Water"),
        ("Krabboss", "Water"),
        ("Voltorbe", "Electric"),
        ("Électrode", "Electric"),
        ("Noeunoeuf", "Grass"),
        ("Noadkoko", "Grass"),
        ("Osselait", "Ground"),
        ("Ossatueur", "Ground"),
        ("Kicklee", "Fighting"),
        ("Tygnon", "Fighting"),
        ("Excelangue", "Normal"),
        ("Smogo", "Poison"),
        ("Smogogo", "Poison"),
        ("Rhinocorne", "Ground"),
        ("Rhinoféros", "Ground"),
        ("Leveinard", "Normal"),
        ("Saquedeneu", "Grass"),
        ("Kangourex", "Normal"),
        ("Hypotrempe", "Water"),
        ("Hypocéan", "Water"),
        ("Poissirène", "Water"),
        ("Poissoroy", "Water"),
        ("Stari", "Water"),
        ("Staross", "Water"),
        ("M. Mime", "Psychic"),
        ("Insécateur", "Bug"),
        ("Lippoutou", "Ice"),
        ("Élektek", "Electric"),
        ("Magmar", "Fire"),
        ("Scarabrute", "Bug"),
        ("Tauros", "Normal"),
        ("Magicarpe", "Water"),
        ("Léviator", "Water"),
        ("Lokhlass", "Water"),
        ("Métamorph", "Normal"),
        ("Évoli", "Normal"),
        ("Aquali", "Water"),
        ("Voltali", "Electric"),
        ("Pyroli", "Fire"),
        ("Porygon", "Normal"),
        ("Amonita", "Rock"),
        ("Amonistar", "Rock"),
        ("Kabuto", "Rock"),
        ("Kabutops", "Rock"),
        ("Ptéra", "Rock"),
        ("Ronflex", "Normal"),
        ("Artikodin", "Ice"),
        ("Électhor", "Electric"),
        ("Sulfura", "Fire"),
        ("Minidraco", "Dragon"),
        ("Draco", "Dragon"),
        ("Dracolosse", "Dragon"),
        ("Mewtwo", "Psychic"),
        ("Mew", "Psychic"),
    ]
]