import IATableDesTypes as IA
import numpy as np
import os
import donnees 
from Stockage_individus import load
from Stockage_individus import save

Generation = IA.get_generation_from_files()


for i in range(20):
    print(Generation[i]())

IA.tri_individus(Generation)

print("-------------------------------TRI-------------------------------")
for i in range(20):
    print(Generation[i]())









