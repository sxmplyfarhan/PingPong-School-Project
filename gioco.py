# Gioco.py

import random
import pygame
from impostazioni import *
import stato_gioco as stato
from suoni import suono_rimbalzo, suono_punto

def resetta_palla():
    # --- Reimposta la posizione e la velocità della palla. ---
    stato.palla.center = (LARGHEZZA // 2, ALTEZZA // 2)
    stato.velocita_corrente = VELOCITA_PALLA * 0.7
    stato.velocita_palla_x = stato.velocita_corrente * random.choice((1, -1))
    stato.velocita_palla_y = stato.velocita_corrente * random.choice((1, -1))

def muovi_palla():
    # --- Muove la palla, gestisce collisioni e aggiorna punteggi. ---
    p = stato.palla
    p.x += stato.velocita_palla_x
    p.y += stato.velocita_palla_y

    # --- Collisione con bordi superiore/inferiore ---
    if p.top <= 0:
        p.top = 0
        stato.velocita_palla_y *= -1
        if suono_rimbalzo: suono_rimbalzo.play()
    elif p.bottom >= ALTEZZA:
        p.bottom = ALTEZZA
        stato.velocita_palla_y *= -1
        if suono_rimbalzo: suono_rimbalzo.play()

    # --- Collisione con padella sinistro ---
    if p.colliderect(stato.padella_sinistra):
        p.left = stato.padella_sinistra.right + 1
        stato.velocita_corrente = min(stato.velocita_corrente + 0.4, VELOCITA_PALLA * 1.8)
        stato.velocita_palla_x = abs(stato.velocita_corrente)
        stato.velocita_palla_y = random.choice([-stato.velocita_corrente, stato.velocita_corrente])
        if suono_rimbalzo: suono_rimbalzo.play()

    # --- Collisione con padella destro ---
    elif p.colliderect(stato.padella_destra):
        p.right = stato.padella_destra.left - 1
        stato.velocita_corrente = min(stato.velocita_corrente + 0.4, VELOCITA_PALLA * 1.8)
        stato.velocita_palla_x = -abs(stato.velocita_corrente)
        stato.velocita_palla_y = random.choice([-stato.velocita_corrente, stato.velocita_corrente])
        if suono_rimbalzo: suono_rimbalzo.play()

    # --- Punteggio (punto segnato) ---
    if p.left <= 0:
        stato.punteggio_destra += 1
        resetta_palla()
        if suono_punto: suono_punto.play()  
    elif p.right >= LARGHEZZA:
        stato.punteggio_sinistra += 1
        resetta_palla()
        if suono_punto: suono_punto.play()  
