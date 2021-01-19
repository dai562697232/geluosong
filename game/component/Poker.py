import pygame
class Card(pygame.sprite.Sprite):
    colors = ["♠", "♥", "♣", "♦"]
    colors_en = ["spades", "hearts", "clubs", "diamonds"]

    def __init__(self, color, value, name, surface_name):
        super.__init__()
        self.color = color
        self.value = value
        self.name = name
        self.surface = surface_name


def initCards(list):
    for surface_name in list:
        pass