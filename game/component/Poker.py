import pygame

SMALL_CARD = -1
NORMAL_CARD = 0
LARGE_CARD = 1


class Card(pygame.sprite.Sprite):
    colors = ["♠", "♥", "♣", "♦"]
    colors_en = ["spades", "hearts", "clubs", "diamonds"]

    def __init__(self, color, value, name, surface_name, size=0):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.value = value
        self.name = name
        self.surface = surface_name
        card_width, card_height = 0, 0
        if size == -1:
            pass
        elif size == 1:
            pass
        else:
            card_width = 75
            card_height = 110

        self.surf = pygame.Surface([card_width, card_height])
        self.rect = self.surf.get_rect()


# def initCards(list):
#     for surface_name in list:
#         pass

ace = Card("spades", 14, "♠A", "scrface")
