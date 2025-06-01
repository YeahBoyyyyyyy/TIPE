from IATableDesTypes import *
import json
import numpy as np

echantillon = 500
numb = 1500

fight_number = [i for i in range(numb)]
damage_dealts = []
perfect_damage_dealts = []
child_damage_dealts = []
damage_takens = []
perfect_damage_takens = []
child_damage_takens = []
nb_victories = []
perfect_nb_victories = []
child_nb_victories = []

for i in range(echantillon):
    pokemon = simplepokemon()
    ppokemon = simplepokemon()
    ppokemon.type_chart = donnees.type_chart
    child = crossover(pokemon,ppokemon)
    print(i)
    for k in range(750):
        fight(pokemon, simplepokemon())
        fight(ppokemon,simplepokemon())
        fight(child, simplepokemon())
    damage_dealts.append(pokemon.number_of_damage_dealt)
    perfect_damage_dealts.append(ppokemon.number_of_damage_dealt)
    child_damage_dealts.append(child.number_of_damage_dealt)
    damage_takens.append(pokemon.number_of_damage_taken)
    perfect_damage_takens.append(ppokemon.number_of_damage_taken)
    child_damage_takens.append(child.number_of_damage_taken)
    nb_victories.append(pokemon.number_of_victories)
    perfect_nb_victories.append(ppokemon.number_of_victories)
    child_nb_victories.append(child.number_of_victories)

# Affichage des résultats en fonction du nombre de combats
import matplotlib.pyplot as plt

results = {
    "fight_number": fight_number,

    "damage_dealts": damage_dealts,
    "perfect_damage_dealts": perfect_damage_dealts,
    "child_damage_dealts" : child_damage_dealts,

    "damage_takens": damage_takens,
    "perfect_damage_takens": perfect_damage_takens,
    "child_damage_takens": child_damage_takens,

    "nb_victories": nb_victories,
    "perfect_nb_victories": perfect_nb_victories,
    "child_nb_victories": child_nb_victories
}

with open("results.json", "w") as f:
    json.dump(results, f, indent=4)
    

plt.figure(figsize=(10, 6))

plt.subplot(3, 1, 1)
plt.plot(fight_number, damage_dealts, color='blue', label="Pokémon IA")
plt.plot(fight_number, perfect_damage_dealts, color='deepskyblue', linestyle='dashdot', label="Pokémon parfait")
plt.plot(fight_number,child_damage_dealts, color='cyan', linestyle='--', label="Enfant")
plt.ylabel("Dégâts infligés")
plt.title("Dégâts infligés en fonction du nombre de combats")
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(fight_number, damage_takens, color='red', label="Pokémon IA")
plt.plot(fight_number, perfect_damage_takens, color='salmon', linestyle='dashdot', label="Pokémon parfait")
plt.plot(fight_number,child_damage_takens, color='darkorange', linestyle='--', label="Enfant")
plt.ylabel("Dégâts subis")
plt.title("Dégâts subis en fonction du nombre de combats")
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(fight_number, nb_victories, color='green', label="Pokémon IA")
plt.plot(fight_number, perfect_nb_victories, color='limegreen', linestyle='dashdot', label="Pokémon parfait")
plt.plot(fight_number,child_nb_victories, color='aquamarine', linestyle='--', label="Enfant")
plt.xlabel("Nombre de combats effectués")
plt.ylabel("Nombre de victoires")
plt.title("Nombre de victoires en fonction du nombre de combats")
plt.legend()
plt.grid(True)
plt.show()

'''
plt.figure(figsize=(10, 6))

plt.subplot(3, 1, 1)
plt.plot(fight_number, damage_dealts, color='blue', label="Pokémon IA")
plt.plot(fight_number, perfect_damage_dealts, color='deepskyblue', linestyle='dashdot', label="Pokémon parfait")
plt.plot(fight_number,child_damage_dealts, color='cyan', linestyle='--', label="Enfant")
plt.ylabel("Dégâts infligés")
plt.title("Dégâts infligés en fonction du nombre de combats")
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(fight_number, damage_takens, color='red', label="Pokémon IA")
plt.plot(fight_number, perfect_damage_takens, color='salmon', linestyle='dashdot', label="Pokémon parfait")
plt.plot(fight_number,child_damage_takens, color='darkorange', linestyle='--', label="Enfant")
plt.ylabel("Dégâts subis")
plt.title("Dégâts subis en fonction du nombre de combats")
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(fight_number, nb_victories, color='green', label="Pokémon IA")
plt.plot(fight_number, perfect_nb_victories, color='limegreen', linestyle='dashdot', label="Pokémon parfait")
plt.plot(fight_number,child_nb_victories, color='aquamarine', linestyle='--', label="Enfant")
plt.xlabel("Nombre de combats effectués")
plt.ylabel("Nombre de victoires")
plt.title("Nombre de victoires en fonction du nombre de combats")
plt.legend()
plt.grid(True)
plt.show()
'''
