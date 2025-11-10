# Principale.py

import pygame, sys
from impostazioni import *
import stato_gioco as stato
from gioco import muovi_palla, resetta_palla
from menu_colore import scegli_colore

pygame.init()
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA), pygame.RESIZABLE)
pygame.display.set_caption("Ping Pong - Due Giocatori")
superficie_virtuale = pygame.Surface((LARGHEZZA, ALTEZZA))
font_titolo = pygame.font.Font(None, 50)
font_punteggio = pygame.font.Font(None, 36)
clock = pygame.time.Clock()


     # --- Menu Pausa ---
def pausa():
    overlay = pygame.Surface((LARGHEZZA, ALTEZZA), pygame.SRCALPHA)
    overlay.fill((0,0,0,180))
    superficie_virtuale.blit(overlay, (0,0))
    testo = font_titolo.render("PAUSA", True, BIANCO)
    superficie_virtuale.blit(testo, (LARGHEZZA//2 - testo.get_width()//2, ALTEZZA//2-50))
    schermo.blit(pygame.transform.scale(superficie_virtuale, schermo.get_size()), (0,0))
    pygame.display.flip()
    paused=True
    while paused:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE: paused=False

def resetta_gioco():
    # --- Resetta punteggi, palla e posizione padella. ---
    stato.punteggio_sinistra = 0
    stato.punteggio_destra = 0
    resetta_palla()
    stato.padella_sinistra.y = ALTEZZA // 2 - stato.padella_sinistra.height // 2
    stato.padella_destra.y = ALTEZZA // 2 - stato.padella_destra.height // 2

def principale():
    global schermo

    while True:  

        # --- Scelta colori ---
        colore_sinistra = scegli_colore(schermo, superficie_virtuale, font_titolo, font_punteggio, "Giocatore 1")
        if colore_sinistra is None: continue  # reset
        colore_destra = scegli_colore(schermo, superficie_virtuale, font_titolo, font_punteggio, "Giocatore 2")
        if colore_destra is None: continue  # reset

        stato.colore_sinistra = colore_sinistra
        stato.colore_destra = colore_destra

        # --- Reset partita ---
        resetta_gioco()

        partita_attiva = True
        while partita_attiva:
            for evento in pygame.event.get():
                if evento.type==pygame.QUIT: pygame.quit(); sys.exit()
                if evento.type==pygame.KEYDOWN:
                    if evento.key==pygame.K_ESCAPE:
                        pausa()
                    if evento.key==pygame.K_r:  
                        resetta_gioco()
                        partita_attiva = False
                        break
                if evento.type==pygame.VIDEORESIZE:
                    schermo=pygame.display.set_mode((evento.w, evento.h), pygame.RESIZABLE)

            # --- Controlli padella ---
            tasti=pygame.key.get_pressed()
            if tasti[pygame.K_UP] and stato.padella_sinistra.top>0: stato.padella_sinistra.y-=VELOCITA_PADELLA
            if tasti[pygame.K_DOWN] and stato.padella_sinistra.bottom<ALTEZZA: stato.padella_sinistra.y+=VELOCITA_PADELLA
            if tasti[pygame.K_LEFT] and stato.padella_destra.top>0: stato.padella_destra.y-=VELOCITA_PADELLA
            if tasti[pygame.K_RIGHT] and stato.padella_destra.bottom<ALTEZZA: stato.padella_destra.y+=VELOCITA_PADELLA

            # --- Logica palla ---
            muovi_palla()

            # --- Controllo vincitore ---
            if stato.punteggio_sinistra >= PUNTEGGIO_VITTORIA or stato.punteggio_destra >= PUNTEGGIO_VITTORIA:
                superficie_virtuale.fill(NERO)
                vincitore = "Giocatore 1" if stato.punteggio_sinistra >= PUNTEGGIO_VITTORIA else "Giocatore 2"
                testo_vittoria = font_titolo.render(f"{vincitore} VINCE!", True, VINTO)
                superficie_virtuale.blit(testo_vittoria, (LARGHEZZA//2 - testo_vittoria.get_width()//2, ALTEZZA//2 - 50))
                schermo.blit(pygame.transform.scale(superficie_virtuale, schermo.get_size()), (0,0))
                pygame.display.flip()
                pygame.time.wait(2000)
                resetta_gioco()
                break  

            # --- Disegno ---
            superficie_virtuale.fill(NERO)
            pygame.draw.rect(superficie_virtuale, stato.colore_sinistra, stato.padella_sinistra)
            pygame.draw.rect(superficie_virtuale, stato.colore_destra, stato.padella_destra)
            pygame.draw.ellipse(superficie_virtuale, BIANCO, stato.palla)
            pygame.draw.aaline(superficie_virtuale, BIANCO, (LARGHEZZA//2,0),(LARGHEZZA//2,ALTEZZA))

            # --- Etichette giocatori ---
            etichetta_sx = font_punteggio.render("Giocatore 1", True, BIANCO)
            etichetta_dx = font_punteggio.render("Giocatore 2", True, BIANCO)
            superficie_virtuale.blit(etichetta_sx, (10,10))
            superficie_virtuale.blit(etichetta_dx, (LARGHEZZA - etichetta_dx.get_width() - 10, 10))

            # --- Centro punteggio con grandezza variabile ---
            if stato.punteggio_sinistra > stato.punteggio_destra:
                colore_sx, colore_dx = VINTO, PERSO
                grandezza_sx, grandezza_dx = int(ALTEZZA*0.12), int(ALTEZZA*0.08)
            elif stato.punteggio_destra > stato.punteggio_sinistra:
                colore_sx, colore_dx = PERSO, VINTO
                grandezza_sx, grandezza_dx = int(ALTEZZA*0.08), int(ALTEZZA*0.12)
            else:
                colore_sx = colore_dx = BIANCO
                grandezza_sx = grandezza_dx = int(ALTEZZA*0.1)

            font_sx = pygame.font.Font(None, grandezza_sx)
            font_dx = pygame.font.Font(None, grandezza_dx)
            score_sx = font_sx.render(str(stato.punteggio_sinistra), True, colore_sx)
            score_dx = font_dx.render(str(stato.punteggio_destra), True, colore_dx)
            superficie_virtuale.blit(score_sx, (LARGHEZZA//2 - 50 - score_sx.get_width()//2, 10))
            superficie_virtuale.blit(score_dx, (LARGHEZZA//2 + 50 - score_dx.get_width()//2, 10))

            schermo.blit(pygame.transform.scale(superficie_virtuale, schermo.get_size()), (0,0))
            pygame.display.flip()
            clock.tick(60)

if __name__=="__main__":
    principale()
