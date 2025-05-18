import os
import pygame
import math
import random
import donnees
import IATableDesTypes as IA
from Stockage_individus import load as load
    
os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE/Stockage_individus")

pygame.init()
pygame.font.init()

''' Utilisation du stock de données pour teste

with open('stock20.txt', 'r') as fichier:
    matrix_from_file = [list(map(float, line.split())) for _,line in zip(range(18),fichier)]

'''

font = pygame.font.Font(None, 20)

screen = pygame.display.set_mode((900, 600))
os.chdir("C:/Users/natha/OneDrive/Desktop/Travail/TIPE")
image = pygame.image.load("assets/type chart icons.png").convert_alpha()

# type_chart(donnees.type_chart)
pokemon1 = load.import_pokemon("test1.txt")
pokemon2 = load.import_pokemon("test2.txt")

child = IA.crossover(pokemon1, pokemon2)

print(child.type_chart)
#for i in range(100000):
    

l,h = 45,21

rect_x, rect_y = 9+l, 5+h 
rect_width, rect_height = 750, 490

rect_pattern_width = 43
rect_pattern_height = 28

sub_types_images = [[],[],[]]
for k in range(3):
    for i in range(6):
        sub_types_images[k].append(image.subsurface(51*k, i*h, l,h))

image_rect = image.get_rect()
running = True

### Fonction affichant la table des types
def type_chart(chart):
        for i, row in zip(range(18),range(rect_y, rect_y + rect_height, rect_pattern_height)):
            for j, col in zip(range(18),range(rect_x, rect_x + rect_width, rect_pattern_width)):
                if chart[i][j] == 0:
                    pygame.draw.rect(screen, (0,0,0), (col, row, rect_pattern_width, rect_pattern_height))
                    screen.blit(multiplier_text[1], (col+10, row+5))
                elif chart[i][j] == 0.5:
                    pygame.draw.rect(screen, (211,45,45), (col, row, rect_pattern_width, rect_pattern_height))
                    screen.blit(multiplier_text[2], (col+10, row+5))
                elif chart[i][j] == 1:
                    pygame.draw.rect(screen, (140,140,140), (col, row, rect_pattern_width, rect_pattern_height))
                    screen.blit(multiplier_text[0], (col+10, row+5))
                else:
                    pygame.draw.rect(screen, (14,209,69), (col, row, rect_pattern_width, rect_pattern_height))
                    screen.blit(multiplier_text[3], (col+10, row+5))

### Fonction créant une mutation et l'affichant en même temps
def mutation(pokemon):
    IA.mutation_type_chart(pokemon)
    type_chart(pokemon.type_chart)

# Préparation de la fenêtre
screen.fill((128, 128, 128))
    
pygame.draw.rect(screen, (200,200,200), (0,0,850,560))
    
for j in range(3):
    for i in range(6):
        screen.blit(sub_types_images[j][i], (i*43+258*j+50,0))
        screen.blit(sub_types_images[j][i], (0,i*29+j*170+25))

multiplier_text = [font.render("x1", True, (0,0,0)), font.render("x0", True, (255,255,255)), 
                   font.render("x0.5", True, (0,0,0)), font.render("x2", True, (0,0,0))]

# Affichage de la table des types
type_chart(child.type_chart)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
                
    mutation(child)
    
    pygame.display.flip()
    

pygame.quit()








