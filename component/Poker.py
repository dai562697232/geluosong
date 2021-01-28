from functools import cmp_to_key

from pygame.sprite import Sprite

from component.InitImageData import *

# 极小
X_SMALL_CARD_SIZE = -2
X_SMALL_CARD_WIDTH = 55
X_SMALL_CARD_HEIGHT = 79

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


def resize_cards_const(w_scale, h_scale):
    # 极小
    global X_SMALL_CARD_WIDTH
    global X_SMALL_CARD_HEIGHT
    global SMALL_CARD_WIDTH
    global SMALL_CARD_HEIGHT
    global NORMAL_CARD_WIDTH
    global NORMAL_CARD_HEIGHT
    X_SMALL_CARD_WIDTH = int(X_SMALL_CARD_WIDTH * w_scale)
    X_SMALL_CARD_HEIGHT = int(X_SMALL_CARD_HEIGHT * h_scale)

    # 小
    SMALL_CARD_WIDTH = int(SMALL_CARD_WIDTH * w_scale)
    SMALL_CARD_HEIGHT = int(SMALL_CARD_HEIGHT * h_scale)
    # 一般大小
    NORMAL_CARD_WIDTH = int(NORMAL_CARD_WIDTH * w_scale)
    NORMAL_CARD_HEIGHT = int(NORMAL_CARD_HEIGHT * h_scale)


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
        # 极小
        if size == -2:

            card_width = X_SMALL_CARD_WIDTH
            card_height = X_SMALL_CARD_HEIGHT
        elif size == -1:
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

    def resize(self, size=0):
        for s in self.sprites():
            s.resize(size)

    def sort_cards(self, by_value=True):
        self = self.__init__(self.sprites(), by_value)


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


types = "One pair, Two pair, Three of a kind, Straight, Flush,Full House, Four of a kind, Straight Flush,"


class CardType():
    def __init__(self, *cardGroup: CardGroup):
        self.group = cardGroup
        self.name = "noname"
        self.shorthand = "noshorthand"
        self.rank = -1

    def check_one_pair(self):
        # len = len(self.group.sprites())
        # num = 0
        # if len > 1:
        #     self.group.sort_cards(True)
        #     cards =self.group.sprites()
        #     for i in range(len):
        #         if i != len-1:
        #             if cards[i] == cards[i + 1]

        pass
    def check_two_pair(self):
        pass

    def check_three_of_a_kind(self):
        pass

    def check_straight(self):
        pass

    def check_flush(self):
        pass

    def check_full_house(self):
        pass

    def check_four_of_a_kind(self):
        pass

    def check_straight_flush(self):
        if len(self.group.sprites()) != 5:
            return False
