from functools import cmp_to_key

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


types = "single,One pair, Two pair, Three of a kind, Straight, Flush,Full House, Four of a kind, Straight Flush,"


class CardType():
    def __init__(self, cardGroup):
        self.card_list = cardGroup.sprites()
        self.group = cardGroup
        self.name = "noname"
        self.shorthand = "noshorthand"
        self.rank = -1

    def check_pair(self):
        arr = []
        pair_num = []
        three_num = []
        fore_num = []

        for i in range(len(self.card_list)):
            if arr.count(self.card_list[i].value) == 0:
                arr.append(self.card_list[i].value)
            else:
                if pair_num.count(self.card_list[i].value) == 0:
                    pair_num.append(self.card_list[i].value)
                else:
                    if three_num.count(self.card_list[i].value) == 0:
                        three_num.append(self.card_list[i].value)
                    else:
                        fore_num.append(self.card_list[i].value)

        return len(pair_num), len(three_num), len(fore_num)

    def check_one_pair(self):
        arr = []
        one_pair_arr = []
        two_pair_arr = []
        for i in range(len(self.card_list)):
            if arr.count(self.card_list[i].value) == 0:
                arr.append(self.card_list[i].value)
            else:
                if one_pair_arr.count(self.card_list[i].value) == 0:
                    one_pair_arr.append(self.card_list[i].value)
                else:
                    two_pair_arr.append(self.card_list[i].value)

    def check_two_pair(self):
        pass

    def check_three_of_a_kind(self):
        pass

    @classmethod
    def check_straight(cls, cards=[]):
        time = 0
        for i in range(len(cards)):
            if i < len(cards) - 1:
                if cards[i].value - 1 == cards[i + 1].value:
                    time += 1
                else:
                    time = 0
        return True if time > 4 else False

    @classmethod
    def check_flush(cls, cards=[]):
        if len(cards) == 0:
            return False
        flag = False
        for i in range(len(cards)):
            if i < len(cards) - 1:
                if cards[i].color - 1 == cards[i + 1].color:
                    flag = True
                else:
                    flag = False

        return flag

    def check_full_house(self):
        pass

    def check_four_of_a_kind(self):
        pass

    def check_straight_flush(self):
        return self.check_flush() and self.check_straight()

    def get_optimal_combination_test(self):
        global d1, d2, d3
        d1 = []
        d2 = []
        d3 = []
        card_flush_count = {"spades": {"num": 0, "items": []}, "hearts": {"num": 0, "items": []},
                            "clubs": {"num": 0, "items": []}, "diamonds": {"num": 0, "items": []}}

        # 按花色筛选
        for i in range(len(self.card_list)):
            # 筛选同花
            for key in card_flush_count:
                if key == self.card_list[i].color:
                    card_flush_count[key]["num"] += 1
                    card_flush_count[key]["items"].append(self.card_list[i])

        for key in card_flush_count:
            if card_flush_count[key]["num"] > 4:
                # 检查是否为同花顺
                if self.check_straight(card_flush_count[key]["items"]):
                    d3 = card_flush_count[key]["items"]

                else:
                    pass

        if len(d3) == 5:

            # 保留同花顺 其余牌都给第二道
            for key in card_flush_count:
                d2 += card_flush_count[key]

            pairs = self.check_pair(d2)
            # 没有对子
            if pairs[0] < 1:
                pass
            else:
                # m没有葫芦
                if pairs[1] < 1:
                    pass
                else:
                    # 没有炸弹
                    if pairs[2] < 1:
                        pass
        else:
            pass

        # if colors_num[key]["num"] >= 5:
        #     flush_time = 0
        #     for j in range(len(colors_num[key]["items"])):
        #         if j < len(colors_num[key]["items"]) - 1:
        #             if colors_num[key]["items"][j].value - 1 == colors_num[key]["items"][j].value:
        #                 flush_time += 1
        #             else:
        #                 flush_time = 0
        #
        #     has_straight_flush = True if flush_time > 4 else False

    def get_optimal_combination(self):
        # 思路
        # 检查顺序  同花顺->炸弹->葫芦->同花->

        card_list = self.group.sprites()
        card_len = len(card_list)

        # 检查同花
        colors_num = {"spades": {"num": 0, "items": []}, "hearts": {"num": 0, "items": []},
                      "clubs": {"num": 0, "items": []}, "diamonds": {"num": 0, "items": []}}
        has_flush = False
        has_straight_flush = False

        value_arr = []
        for i in range(card_len):

            # 检查同花
            for key in colors_num:
                if key == card_list[i].color:
                    colors_num[key]["num"] += 1
                    colors_num[key]["items"].append(card_list[i])
                    if colors_num[key]["num"] >= 5:
                        has_flush = True
                        flush_time = 0
                        for j in range(len(colors_num[key]["items"])):
                            if j < len(colors_num[key]["items"]) - 1:
                                if colors_num[key]["items"][j].value - 1 == colors_num[key]["items"][j].value:
                                    flush_time += 1
                                else:
                                    flush_time = 0

                        has_straight_flush = True if flush_time > 4 else False
            if value_arr.count(card_list[i].value) == 0:
                value_arr.append(card_list[i].value)

        #   检查顺子
        global straight_time;
        straight_time = 0
        for i in range(len(value_arr)):
            if i < len(value_arr) - 1:
                if value_arr[i] - 1 == value_arr[i + 1]:
                    # if card_list[i].value - 1 == card_list[i + 1].value:

                    straight_time += 1
                else:
                    straight_time = 0
                print(straight_time)
        print("out:", straight_time)
        has_straight = True if straight_time > 4 else False
        print("是否有同花", has_flush)
        print("是否有同花顺", has_straight_flush)
        print("是否有顺子", has_straight)
