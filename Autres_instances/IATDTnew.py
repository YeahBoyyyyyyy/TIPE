import os
os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Autres_instances")
import random
import donnees2
from multiprocessing import Pool, cpu_count


NUMBER_OF_ATTACKS = 12
NUMBER_OF_FIGHT = 9000
ZERO = 0
HALF = 1/2
DOUBLE = 2
MUTATION_CHANCE = 0.005

# Choisir un type au hasard parmi les 18 types du jeu
def randomType():
    return donnees2.POKEMON_TYPES[random.randint(0,17)]

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
    ID_offensive_type = donnees2.POKEMON_TYPES_ID[str(offensive_type)]
    ID_defensive_type = donnees2.POKEMON_TYPES_ID[str(defensive_type)]
    return donnees2.type_chart[ID_offensive_type][ID_defensive_type]

# Génération d'une table des types totalement aléatoire 
def generateTypeChart():
    values = [0, 0.5, 1, 2]
    weights = [0.020, 0.2025, 0.55, 0.20]

    matrix = [[random.choices(values, weights)[0] for _ in range(18)] for _ in range(18)]
    
    return matrix

def generateTypeChartCustomAccuracy(accuracy):

    values = [0, 0.5, 1, 2]
    weights = [0.020, 0.2025, 0.55, 0.20]

    matrix = [[0 for _ in range(18)] for _ in range(18)]

    for i in range(18):
        for j in range(18):
            if random.random() > accuracy:
                matrix[i][j] = random.choices(values, weights)[0]
            else:
                matrix[i][j] = donnees2.type_chart[i][j]  # Utiliser la table de types originale pour une précision donnée
        
    return matrix

def simplePokemonWeakness(pokemon, typechart):
    type = pokemon.type
    weakness = []
    for i in range(18):
        if typechart[i][donnees2.POKEMON_TYPES_ID[type]] == 2:
            weakness.append(donnees2.POKEMON_TYPES[i])
    return weakness

def simplePokemonResistance(pokemon, typechart):
    type = pokemon.type
    resistance = []
    for i in range(18):
        if typechart[i][donnees2.POKEMON_TYPES_ID[type]] == 0.5:
            resistance.append(donnees2.POKEMON_TYPES[i])
    return resistance

def simplePokemonNeutrality(pokemon, typechart):
    type = pokemon.type
    neutrality = []
    for i in range(18):
        if typechart[i][donnees2.POKEMON_TYPES_ID[type]] == 1:
            neutrality.append(donnees2.POKEMON_TYPES[i])
    return neutrality

def simplePokemonImmunities(pokemon, typechart):
    type = pokemon.type
    immunities = []
    for i in range(18):
        if typechart[i][donnees2.POKEMON_TYPES_ID[type]] == 0:
            immunities.append(donnees2.POKEMON_TYPES[i])
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

def type_chart_evaluation(pokemon):
    IA_type_chart = pokemon.type_chart
    evaluation = 0
    for i in range(18):
        for j in range(18):
            if IA_type_chart[i][j] == donnees2.type_chart[i][j]:
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
        pokemon1.number_of_damage_dealt += attack_used[0]*mono_type_attack_effectiveness(attack_used[1], pokemon2.type)*5

        if pokemon2.hp <= 0:
            pokemon1.number_of_victories += 5
            break

        # ---------------------- Tour du pokémon adverse ------------------------- #

        attack_used = selectAttackDefense(pokemon2, pokemon1)  # Choisir une attaque en fonction de la résistance du pokémon adverse
        damageSingleType(attack_used, pokemon1)

        ######## Gain de fitness et gain de damage taken
        pokemon1.number_of_damage_taken += attack_used[0]*mono_type_attack_effectiveness(attack_used[1], pokemon1.type)*5

        if pokemon1.hp <= 0:
            break

        compteur += 1

    pokemon1.hp = 200  # Reset HP for the next fight
    pokemon1.type = randomType() # Randomise le type pour pouvoir permettre d'utilliser d'autres attaques après
    pokemon1.attacks = [simpleAttack() for i in range(NUMBER_OF_ATTACKS)] # randomise les attaques pour faire varier les choix
    return pokemon1     

def smart_mutation(pokemon, freq_map, total_gens, mutation_rate=0.01, confidence_threshold=0.85):
    chart = pokemon.type_chart
    L = [0, 0.5, 1, 2]
    for i in range(18):
        for j in range(18):
            counts = freq_map[i][j]
            total = sum(counts.values())
            if total < 5:  # pas assez d'infos pour décider
                do_mutate = random.random() < mutation_rate
            else:
                # Score de confiance sur la valeur actuelle
                val = chart[i][j]
                freq = counts[val] / total
                do_mutate = freq < confidence_threshold and random.random() < mutation_rate * 2

            if do_mutate:
                chart[i][j] = random.choice([v for v in L if v != chart[i][j]])
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

def special_crossover(bestparent:simplepokemon, badparent:simplepokemon):
    child = simplepokemon()
    chart1 = bestparent.type_chart
    chart2 = badparent.type_chart
    for i in range(18):
        for j in range(18):
            r = random.random()
            if r < 0.75:
                child.type_chart[i][j] = chart1[i][j]
            else:
                child.type_chart[i][j] = chart2[i][j]
    return child

def fight_wrapper(args):
    individu, n_fights = args
    for _ in range(n_fights):
        individu.hp = 200
        try:
            fight(individu, simplepokemon())
        except:
            break
    return individu

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
        print(f"combat terminé pour le pokemon : {i}", end="\r", flush=True)

def fight_generation_parallel(generation, n_fights=NUMBER_OF_FIGHT):
    nb_processes = min(cpu_count(), len(generation))

    with Pool(processes=nb_processes) as pool:
        args = [(ind, n_fights) for ind in generation]
        result = pool.map(fight_wrapper, args)

    return result  # retourne la nouvelle génération modifiée

def tri_individus(gen):
    # normalisation de la génération
    normalize_generation(gen)
    # Trie la génération d'individus par fitness
    n = len(gen)
    for i in range(n):
        for j in range(n-i-1):
            if gen[j].fitness < gen[j+1].fitness:
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
            0.1 * norm_dealt +
            0.6 * (1 - norm_taken) +
            0.3 * norm_victories
        )

def new_generation(generation, freq_map, g, mutation_rate):
    gen = generation.copy()
    tri_individus(gen)  # Trie la génération selon le fitness (meilleurs en premier)
    new_gen = []

    # Élitisme : on garde les deux meilleurs individus sans modification
    best1 = gen[0]
    best2 = gen[1]
    new_gen.append(best1)
    new_gen.append(best2)
    gen = gen[2:]

    # Sélection par tournoi : on sélectionne les meilleurs parents pour croisement
    top_percent = int(len(gen) * 0.3) if len(gen) > 2 else len(gen)
    parents_pool = gen[:top_percent]
    gen = gen[top_percent:]  # On retire les meilleurs parents de la génération

    # Générer des enfants par croisement entre les meilleurs parents (favorise la diversité)
    while len(new_gen) < len(generation)*0.6:  # On vise à créer 90% de la génération
        parent1 = random.choice([best1, best2] + parents_pool[:len(parents_pool)//4])
        parent2 = random.choice(parents_pool)
        if parent1 == parent2:
            parent2 = simplepokemon()  # Diversité si même parent
        child = crossover(parent1, parent2)
        child = smart_mutation(child, freq_map, g, mutation_rate)                        # mutation_type_chart(child, mutation_rate)
        new_gen.append(child)

    while len(new_gen) < len(generation) * 0.7:  # On vise à créer 90% de la génération
        parent1 = random.choice([best1, best2] + parents_pool[:len(parents_pool)//4])
        parent2 = random.choice(gen) # On prend un parent aléatoire de la génération restante
        child = crossover(parent1, parent2)
        child = smart_mutation(child, freq_map, g, mutation_rate)                         # mutation_type_chart(child, mutation_rate)
        new_gen.append(child)

    # Compléter la génération avec des individus aléatoires si nécessaire
    while len(new_gen) < len(generation):
        parent1 = random.choice([best1, best2] + [parents_pool[0]])
        parent2 = simplepokemon()  
        child = special_crossover(parent1, parent2)
        new_gen.append(child)                      


    for i in range(len(new_gen)):
        new_gen[i].fitness = 0  # Réinitialiser la fitness des nouveaux individus

    # S'assurer que la taille de la génération reste constante
    return new_gen[:len(generation)]