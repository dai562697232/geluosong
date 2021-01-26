from game.component.Poker import *
import random


# 添加全部牌
def create_cards():
    colors_shape = Card.colors_shape
    colors_en = Card.colors_en
    all_cards = []
    for i in range(4):
        for j in range(13):
            if j + 2 == 11:
                all_cards.append(Card(colors_en[i], 11, colors_shape[i] + "J", "jack_of_" + colors_en[i]))
            elif j + 2 == 12:
                all_cards.append(Card(colors_en[i], 12, colors_shape[i] + "Q", "queen_of_" + colors_en[i]))
            elif j + 2 == 13:
                all_cards.append(Card(colors_en[i], 13, colors_shape[i] + "K", "king_of_" + colors_en[i]))
            elif j + 2 == 14:
                all_cards.append(Card(colors_en[i], 14, colors_shape[i] + "A", "ace_of_" + colors_en[i]))
            else:
                all_cards.append(
                    Card(colors_en[i], j + 2, colors_shape[i] + str(j + 2), str(j + 2) + "_of_" + colors_en[i]))

    return all_cards


def deal():
    all_cards = create_cards()
    random.shuffle(all_cards)
    players = []
    for i in range(4):
        players.append(CardGroup(all_cards[i * 13:(i + 1) * 13]))
    return players



# 洗牌

