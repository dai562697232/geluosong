import pygame
import os

# 游戏背景图片
BACKGROUND_WELCOME_IMAGE = "gls1366_768.png"
BACKGROUND_GAME_IMAGE = "sky_background.png"

# 按钮
PLAY_BUTTON_IMG = "play.png"
PLAY_BUTTON_DARK_IMG = "play_dark.png"

SORT_SWITCH_BUTTON = 'sort_switch.png'
SORT_SWITCH_OUTLINE_BUTTON = 'sort_switch_outline.png'

CANCEL_ALL_BUTTON = 'cancel_all.png'
CANCEL_ALL_OUTLINE_BUTTON = 'cancel_all_outline.png'

FINISH_PUT_BUTTON = 'finish_put.png'
FINISH_PUT_OUTLINE_BUTTON = 'finish_put_outline.png'

EXCHANGE_BUTTON = 'exchange.png'
EXCHANGE_OUTLINE_BUTTON = 'exchange_outline.png'


class ImageData:
    cards_image_data = {}
    basic_image_data = {}
    buttons_image_data = {}

    # def __init__(self):
    #     print("图片数据加载中")
    #     self.cards_image_data = self.init_cards_image_data()
    #     self.basic_image_data = self.init_basic_image_data()
    #     print("图片数据加载完成")

    @classmethod
    def get_cards_image_data(cls):
        color_en = ["spades", "hearts", "clubs", "diamonds"]
        if len(cls.cards_image_data) == 0:

            for i in range(4):
                for j in range(13):
                    if j + 2 == 11:
                        cls.cards_image_data["jack_of_" + color_en[i]] = pygame.image.load(
                            "img/pokerimg/jack_of_" + color_en[i] + ".png").convert_alpha()
                    elif j + 2 == 12:
                        cls.cards_image_data["queen_of_" + color_en[i]] = pygame.image.load(
                            "img/pokerimg/queen_of_" + color_en[i] + ".png").convert_alpha()
                    elif j + 2 == 13:
                        cls.cards_image_data["king_of_" + color_en[i]] = pygame.image.load(
                            "img/pokerimg/king_of_" + color_en[i] + ".png").convert_alpha()
                    elif j + 2 == 14:
                        cls.cards_image_data["ace_of_" + color_en[i]] = pygame.image.load(
                            "img/pokerimg/ace_of_" + color_en[i] + ".png")
                    else:
                        cls.cards_image_data[str(j + 2) + "_of_" + color_en[i]] = pygame.image.load(
                            "img/pokerimg/" + str(j + 2) + "_of_" + color_en[i] + ".png").convert_alpha()
        return cls.cards_image_data

    @classmethod
    def get_basic_image_data(cls):
        if len(cls.basic_image_data) == 0:
            dir = "img/basic/"
            file_names = os.listdir(dir)
            for name in file_names:
                cls.basic_image_data[name] = pygame.image.load(dir + name).convert_alpha()

            print("基础图片加载完毕...")
        return cls.basic_image_data

    @classmethod
    def get_buttons_image_data(cls):
        if len(cls.buttons_image_data) == 0:
            dir = "img/buttons/"
            button_names = os.listdir(dir)
            for button in button_names:
                cls.buttons_image_data[button] = pygame.image.load(dir + button).convert_alpha()
            print("按钮图片加载完毕...")

        return cls.buttons_image_data
