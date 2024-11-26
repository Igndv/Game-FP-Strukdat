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

GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)

def draw_window():
    WIN.fill(GREEN)

    textTry = font.render("Test Text", True, BLUE)
    WIN.blit(textTry,(500,100))

def main():
    run_game = True
    clock = pygame.time.Clock()

    ### EVENT CHECKER
    while run_game:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #exit
                run_game = False

        draw_window()
        #Update every loop
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__": #to make sure to run the main function when this programe is called
    main()

