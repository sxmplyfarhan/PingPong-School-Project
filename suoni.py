#Suoni.py

import pygame

pygame.mixer.init()

# --- Suono rimbalzo (padella / muro) ---
try:
    suono_rimbalzo = pygame.mixer.Sound("palla_rimbalzo.wav")
except:
    suono_rimbalzo = None

# --- Suono punto segnato --- 
try:
    suono_punto = pygame.mixer.Sound("punto.wav")
except:
    suono_punto = None
