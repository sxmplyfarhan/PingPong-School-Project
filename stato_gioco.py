# Stato_gioco.py

import pygame
import random
from impostazioni import *

# --- Punteggi ---
punteggio_sinistra = 0
punteggio_destra = 0

# --- Palla ---
palla = pygame.Rect(LARGHEZZA//2 - 15, ALTEZZA//2 - 15, 30, 30)
velocita_palla_x = VELOCITA_PALLA * random.choice((1,-1))
velocita_palla_y = VELOCITA_PALLA * random.choice((1,-1))
velocita_corrente = VELOCITA_PALLA

# --- Padella ---
padella_sinistra = pygame.Rect(20, ALTEZZA//2 - 70, 10, 140)
padella_destra = pygame.Rect(LARGHEZZA - 30, ALTEZZA//2 - 70, 10, 140)

# --- Colori ---
colore_sinistra = ARCOBALENO[0]
colore_destra = ARCOBALENO[1]
