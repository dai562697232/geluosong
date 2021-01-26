from functools import cmp_to_key

from pygame.sprite import Sprite

from game.component.InitImageData import *

# 小
SMALL_CARD_SIZE = -1
SMALL_CARD_WIDTH = 75
SMALL_CARD_HEIGHT = 108
# 一般大小
NORMAL_CARD_SIZE = 0
NORMAL_CARD_WIDTH = 110
NORMAL_CARD_HEIGHT = 159

# 大
LARGE_CARD_SIZE = 1


class Card(pygame.sprite.Sprite):
    colors_shape = ["♠", "♥", "♣", "♦"]
    colors_en = ["spades", "hearts", "clubs", "diamonds"]

    def __init__(self, color, value, name, surface_key, size=0):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.value = value
        self.name = name
        self.surface_key = surface_key
        self.card_width = 0
        self.card_height = 0
        # self.surf = pygame.Surface([card_width, card_height])
        card_width, card_height = 0, 0
        self.resize(size)

    def pre_select(self, surface, xy):
        surface.blit(self.surface, (xy[0], xy[1]))

    def resize(self, size=0):
        if size == -1:
            card_width = SMALL_CARD_WIDTH
            card_height = SMALL_CARD_HEIGHT
        elif size == 1:
            pass
        else:
            card_width = NORMAL_CARD_WIDTH
            card_height = NORMAL_CARD_HEIGHT

        self.card_width = card_width
        self.card_height = card_height

    def selected(self, surface, xy):
        self.resize(-1)
        self.draw_to(surface, xy)

    def get_rect(self):
        return self.surface.get_rect()

    def draw_to(self, surface, xy):
        self.surface = pygame.transform.scale(ImageData.get_cards_image_data()[self.surface_key], (self.card_width,
                                                                                                   self.card_height))
        surface.blit(self.surface, (xy[0], xy[1]))


class CardGroup(pygame.sprite.Group):
    def __init__(self, cards=[], by_value=True):

        if by_value:
            cards.sort(key=cmp_to_key(comp_value_color))
        else:
            cards.sort(key=cmp_to_key(comp_color_value))
        pygame.sprite.Group.__init__(self, cards)



    def draw_to(self, surface, xy, space=0, pre_selected=-1):
        if len(self.sprites()) > 0:
            i = 0
            for key in self.sprites():
                if pre_selected != i:
                    if space == 0:
                        key.draw_to(surface, (xy[0] + i * key.card_width, xy[1]))
                    else:
                        key.draw_to(surface, (xy[0] + i * space, xy[1]))

                i += 1
    def sort_cards(self,by_value=True):
        self = self.__init__(self.sprites(),by_value)


# 排序算法
def comp_value_color(a, b):
    if a.value == b.value:
        return 1 if Card.colors_en.index(a.color) > Card.colors_en.index(b.color) else -1
    else:
        return 1 if a.value < b.value else -1


def comp_color_value(a, b):
    if Card.colors_en.index(a.color) == Card.colors_en.index(b.color):
        return 1 if a.value < b.value else -1
    else:
        return 1 if Card.colors_en.index(a.color) > Card.colors_en.index(b.color) else -1
