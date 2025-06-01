import IATableDesTypes as IA
import os 
os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Data_Analysis")
import json
import numpy as np
from sklearn.preprocessing import RobustScaler, MinMaxScaler
import pandas as pd


with open("datas.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)


damage_dealts = data["damage_dealts"]
perfect_damage_dealts = data["perfect_damage_dealts"]
child_damage_dealts = data["child_damage_dealts"]
damage_takens = data["damage_takens"]
perfect_damage_takens = data["perfect_damage_takens"]
child_damage_takens = data["child_damage_takens"]
nb_victories = data["nb_victories"]
perfect_nb_victories = data["perfect_nb_victories"]
child_nb_victories = data["child_nb_victories"]
""
moyenne_damage_dealts = np.mean(damage_dealts + perfect_damage_dealts)
moyenne_damage_takens = np.mean(damage_takens + perfect_damage_takens)
moyenne_nb_victories = np.mean(nb_victories + perfect_nb_victories)

    # Normalisation des données pour l'analyse de la fitness des Pokémon
# Méthode Min-Max Scaling pour damage dealt

standard_deviation = np.std(damage_dealts + perfect_damage_dealts)





"""

X = pd.DataFrame({
    "damage_dealts": df["damage_dealts"],
    "damage_takens": df["damage_takens"],
    "nb_victories": df["nb_victories"]
})

# Normalisation
scaler_robust = RobustScaler()
scaler_minmax = MinMaxScaler()

X[["damage_dealts", "damage_takens"]] = scaler_robust.fit_transform(X[["damage_dealts", "damage_takens"]])
X[["nb_victories"]] = scaler_minmax.fit_transform(X[["nb_victories"]])

# Pondération
w1, w2, w3 = 0.3, 0.6, 0.1
X["fitness"] = (
    w1 * X["damage_dealts"] +
    w2 * (1 - X["damage_takens"]) +  # On inverse si moins = mieux
    w3 * X["nb_victories"]
)

# Sélection du meilleur individu
best_index = X["fitness"].idxmax()
best_individual = X.loc[best_index]
print(best_individual)
"""