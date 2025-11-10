# Menu _Colori.py

import pygame, sys, time
from impostazioni import *

def scegli_colore(schermo, superficie, font_titolo, font_punteggio, giocatore="Giocatore 1"):
    indice = 0
    inizio = time.time()
    while True:
        superficie.fill(NERO)
        titolo = font_titolo.render(f"Scegli colore: {giocatore}", True, BIANCO)
        superficie.blit(titolo, (LARGHEZZA//2 - titolo.get_width()//2, ALTEZZA*0.08))

        # --- Quadrati colori ---
        dimensione = ALTEZZA*0.12
        spaziatura = (LARGHEZZA - dimensione*len(ARCOBALENO)) / (len(ARCOBALENO)+1)
        for i, colore in enumerate(ARCOBALENO):
            x = spaziatura + i*(dimensione+spaziatura)
            y = ALTEZZA*0.4
            rett = pygame.Rect(x,y,dimensione,dimensione)
            pygame.draw.rect(superficie, colore, rett)
            if i==indice: pygame.draw.rect(superficie, BIANCO, rett, 4)

        restante = max(0, TEMPO_SCELTA_COLORE - int(time.time()-inizio))
        info = font_punteggio.render(f"{restante}s rimanenti", True, BIANCO)
        superficie.blit(info, (LARGHEZZA//2 - info.get_width()//2, ALTEZZA*0.75))

        schermo.blit(pygame.transform.scale(superficie, schermo.get_size()), (0,0))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                # --- menu di pausa ---
                if evento.key == pygame.K_ESCAPE:
                    paused = True
                    overlay = pygame.Surface((LARGHEZZA, ALTEZZA), pygame.SRCALPHA)
                    overlay.fill((0,0,0,180))
                    superficie.blit(overlay, (0,0))
                    testo = font_titolo.render("PAUSA", True, BIANCO)
                    superficie.blit(testo, (LARGHEZZA//2 - testo.get_width()//2, ALTEZZA//2-50))
                    schermo.blit(pygame.transform.scale(superficie, schermo.get_size()), (0,0))
                    pygame.display.flip()
                    while paused:
                        for e in pygame.event.get():
                            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE:
                                paused=False

                # --- resetta il gioco ---
                if evento.key == pygame.K_r:
                    return None  

                # --- Naviga tra i colori ---
                if giocatore=="Giocatore 1":
                    if evento.key==pygame.K_UP: indice=(indice-1)%len(ARCOBALENO)
                    if evento.key==pygame.K_DOWN: indice=(indice+1)%len(ARCOBALENO)
                else:
                    if evento.key==pygame.K_LEFT: indice=(indice-1)%len(ARCOBALENO)
                    if evento.key==pygame.K_RIGHT: indice=(indice+1)%len(ARCOBALENO)

        if time.time()-inizio >= TEMPO_SCELTA_COLORE:
            return ARCOBALENO[indice]
