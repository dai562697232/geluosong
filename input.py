


import pygame
from pygame.locals import *

pygame.init()
size = width, height = 640, 480
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Gaben's Future Adventure")

player = pygame.image.load("images/player.png")
player_rect = player.get_rect()

white = (255, 255, 255)
black = (0, 0, 0)


class World(object):
    def __init__(self):
        pass


move_map = {pygame.K_w: (0, -1),
            pygame.K_s: (0, 1),
            pygame.K_a: (-1, 0),
            pygame.K_d: (1, 0)}


def main():
    running = True

    while running:
        screen.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print
                "Exiting game."

        pressed = pygame.key.get_pressed()
        move = [move_map[key] for key in move_map if pressed[key]]
        final = map(sum, zip(*move))
        if final:
            player_rect.move_ip(*final)

        screen.blit(player, player_rect)
        pygame.display.flip()
        print
        player_rect.x
        print
        player_rect.y


main()
