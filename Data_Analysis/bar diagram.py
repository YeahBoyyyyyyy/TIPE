import json
import numpy as np
import matplotlib.pyplot as plt
("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Stockage_individus/Data_Analysis")
numb = 500
jason = dict()

with open('Data_Analysis/datas.json') as json_data:
    jason = json.load(json_data)


damage_dealts = jason["damage_dealts"]
perfect_damage_dealts = jason["perfect_damage_dealts"]
child_damage_dealts = jason["child_damage_dealts"]
damage_takens = jason["damage_takens"]
perfect_damage_takens = jason["perfect_damage_takens"]
child_damage_takens = jason["child_damage_takens"]
nb_victories = jason["nb_victories"]
perfect_nb_victories = jason["perfect_nb_victories"]
child_nb_victories = jason["child_nb_victories"]

print(np.mean(damage_dealts))
print(np.mean(perfect_damage_dealts))

pokemons = ["random", "child", "perfect"]
damage_dealts_count = [np.mean(damage_dealts), np.mean(child_damage_dealts), np.mean(perfect_damage_dealts)]
damage_takens_count = [np.mean(damage_takens), np.mean(child_damage_takens), np.mean(perfect_damage_takens)]
nb_victories_count = [np.mean(nb_victories), np.mean(child_nb_victories), np.mean(perfect_nb_victories)]


fig, axs = plt.subplots(1, 3, figsize=(17, 4))

bar_colors1 = ['green', 'limegreen', 'aquamarine']
bar_colors2 = ['blue', 'cyan', 'deepskyblue']
bar_colors3 = ['red', 'darkorange', 'salmon']

axs[0].set_title("Nb victoire pour chaque pokemon")
axs[1].set_title("Dommages infligés pour chaque pokemon")
axs[2].set_title("Dommages reçus pour chaque pokemon")

axs[0].set_ylabel("nombre de victoires")
axs[1].set_ylabel("Dommages infligés")
axs[2].set_ylabel("Dommages reçus")

axs[0].bar(pokemons, nb_victories_count, color = bar_colors1)
axs[1].bar(pokemons, damage_dealts_count, color = bar_colors2)
axs[2].bar(pokemons, damage_takens_count, color = bar_colors3)

plt.show()

"""
bar_width = 0.25
index = np.arange(numb)

plt.figure(figsize=(12, 10))

    # Dégâts infligés
plt.subplot(3, 1, 1)
plt.bar(index, damage_dealts, bar_width, label="Pokémon IA", color='blue')
plt.bar(index + bar_width, perfect_damage_dealts, bar_width, label="Pokémon parfait", color='deepskyblue')
plt.bar(index + 2 * bar_width, child_damage_dealts, bar_width, label="Enfant", color='cyan')
plt.ylabel("Dégâts infligés")
plt.title("Dégâts infligés en fonction du nombre de combats")
plt.legend()
plt.grid(True, axis='y')
plt.xticks([])

    # Dégâts subis
plt.subplot(3, 1, 2)
plt.bar(index, damage_takens, bar_width, label="Pokémon IA", color='red')
plt.bar(index + bar_width, perfect_damage_takens, bar_width, label="Pokémon parfait", color='salmon')
plt.bar(index + 2 * bar_width, child_damage_takens, bar_width, label="Enfant", color='darkorange')
plt.ylabel("Dégâts subis")
plt.title("Dégâts subis en fonction du nombre de combats")
plt.legend()
plt.grid(True, axis='y')
plt.xticks([])

    # Nombre de victoires
plt.subplot(3, 1, 3)
plt.bar(index, nb_victories, bar_width, label="Pokémon IA", color='green')
plt.bar(index + bar_width, perfect_nb_victories, bar_width, label="Pokémon parfait", color='limegreen')
plt.bar(index + 2 * bar_width, child_nb_victories, bar_width, label="Enfant", color='aquamarine')
plt.xlabel("Nombre de combats effectués")
plt.ylabel("Nombre de victoires")
plt.title("Nombre de victoires en fonction du nombre de combats")
plt.legend()
plt.grid(True, axis='y')
plt.xticks([])

plt.tight_layout()
plt.show()
"""

