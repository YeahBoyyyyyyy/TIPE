import pygame
from math import *

chemin = "Fonctionnement_neurone\\"
peur = 300
poids = 0.004

def calcdistance(pos1, pos2):
    x1,y1 = pos1
    x2,y2 = pos2
    return sqrt((x1-x2)**2+(y1-y2)**2)

def trop_proche(dist):
    sortie = dist*poids
    if sortie >= 1:
        return (True,1)
    else:
        return (False,0)


pygame.init()
pygame.mixer.init()
pygame.font.init()

pygame.mixer.music.load(chemin +"SCREAM.mp3")

pygame.mixer.music.play(loops=-1)
pygame.mixer.music.pause()

# Chargement de la fenêtre du titre et de l'icon
ecran = pygame.display.set_mode((1200, 640))
image = pygame.image.load(chemin +"icon.jpg").convert_alpha()
pygame.display.set_icon(image)
pygame.display.set_caption(chemin +"Diidy Party")

# Chargement des trois images importantes
background = pygame.image.load(chemin +"mario_background.jpg").convert()
mario = pygame.image.load(chemin +"Mayo.png").convert_alpha()
mario_screaming = pygame.image.load(chemin +"MAAAAAAMAAAAAAYO.PNG").convert_alpha()
boo = pygame.image.load(chemin +"Boo.png").convert_alpha()

# Chargement des positions des images
image_rect = boo.get_rect(topleft=(800, 200))  # Position initiale
mario_rect = mario.get_rect(center=(150,450))

# Variables de contrôle
dragging = False  # L'image est-elle en train d'être déplacée ?
offset_x = 0  # Décalage entre la souris et l'image
offset_y = 0

distance = int()

# Neurone
neurone = pygame.image.load(chemin +"neurone.png").convert_alpha()

# Police d'écriture pour le neurone
font = pygame.font.Font(None, 30)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Détecter un clic sur l'image
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if image_rect.collidepoint(event.pos):  # Si on clique sur l'image
                dragging = True
                offset_x = image_rect.x - event.pos[0]
                offset_y = image_rect.y - event.pos[1]

        # Relâcher l'image
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        # Déplacer l'image avec la souris
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                image_rect.x = event.pos[0] + offset_x
                image_rect.y = event.pos[1] + offset_y
    
    ecran.blit(background, (0,0))
    
    if trop_proche(distance)[0]:
        pygame.mixer.music.unpause()
        ecran.blit(mario_screaming, mario_rect)
    else:
        pygame.mixer.music.pause()
        ecran.blit(mario, mario_rect)

    distance = max(0, 600 - calcdistance(mario_rect.center, image_rect.center) * 0.70)

    pygame.mixer.music.set_volume(distance/600)

    neurone_entree = font.render(str(int(distance)), True, (0,0,0))
    neurone_poids = font.render(str(poids), True, (0,0,0))
    neurone_sortie = font.render(str(trop_proche(distance)[1]), True, (0,0,0))

  
    ecran.blit(boo, image_rect)
    ecran.blit(neurone, (25, 25))
    ecran.blit(neurone_entree, (57, 95))
    ecran.blit(neurone_poids, (180, 83))
    ecran.blit(neurone_sortie, (365, 95))

    # Mise à jour affichage
    pygame.display.flip()

pygame.mixer.music.stop()
pygame.quit()


