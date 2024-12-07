from unittest.result import failfast
import pygame
import os

pygame.init()

HEIGHT, WIDHT = 720, 1280
FPS = 30
WIN = pygame.display.set_mode((WIDHT,HEIGHT))

#FONT
font = pygame.font.Font(None, 50)
pygame.display.set_caption("Anomaly")

#COLOUR
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
RED = (255,0,0)

#VARIABLE (PATEN)


def draw_window():
    WIN.fill(GREEN)

    #textTry = font.render("Test Text", True, BLUE)
    #WIN.blit(textTry,(500,100))

    pygame.draw.rect(WIN,RED,(player_x,player_y,50,50))

def main():

    #VARIABLES (YANG PERLU DIUPDATE)
    global player_x, player_y, vel
    player_x = 590
    player_y = 310
    vel = 20

    run_game = True
    clock = pygame.time.Clock()

    ### EVENT CHECKER
    while run_game:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #exit
                run_game = False


        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]: #LEFT
            player_x -= vel
        if keys[pygame.K_d]: #RIGHT
            player_x += vel
        if keys[pygame.K_w]: #UP
            player_y -= vel
        if keys[pygame.K_s]: #DOWN
            player_y += vel

        ### DRAW
        draw_window()

        #Update every loop
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__": #to make sure to run the main function when this programe is called
    main()

