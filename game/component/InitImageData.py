# 图片字典
imgurl_dict = {}

# 游戏背景图片
BACKGROUND_WELCOME_IMAGE = "background_welcome_image"
BACKGROUND_GAME_IMAGE = "background_game_image"

imgurl_dict[BACKGROUND_WELCOME_IMAGE] = 'img/gls1366_768.png'
imgurl_dict[BACKGROUND_GAME_IMAGE] = 'img/sky_background.png'

# 按钮
PLAY_BUTTON_IMG = "play_button_img"
PLAY_BUTTON_DARK_IMG = "play_button_dark_img"

imgurl_dict[PLAY_BUTTON_IMG] = 'img/play.png'
imgurl_dict[PLAY_BUTTON_DARK_IMG] = 'img/play_dark.png'


class ImageData:
    def __init__(self, pygameInstance):
        self.pygameInstance = pygameInstance
        print("图片数据加载中")
        self.card_image_data = self.init_card_image_data()
        self.basal_image_data = self.init_basal_image_data()
        print("图片数据加载完成")

    def init_card_image_data(self):
        color_en = ["spades", "hearts", "clubs", "diamonds"]
        list = {}
        for i in range(4):
            for j in range(12):
                if j + 2 == 10:
                    list["jack_of_" + color_en[i]] = self.pygameInstance.image.load(
                        "img/pokerimg/jack_of_" + color_en[i] + ".png").convert_alpha()
                elif j + 2 == 11:
                    list["queen_of_" + color_en[i]] = self.pygameInstance.image.load(
                        "img/pokerimg/queen_of_" + color_en[i] + ".png").convert_alpha()
                elif j + 2 == 12:
                    list["king_of_" + color_en[i]] = self.pygameInstance.image.load(
                        "img/pokerimg/king_of_" + color_en[i] + ".png").convert_alpha()
                elif j + 2 == 13:
                    list["ace_of_" + color_en[i]] = self.pygameInstance.image.load(
                        "img/pokerimg/ace_of_" + color_en[i] + ".png")
                else:
                    list[str(j + 2) + "_of_" + color_en[i]] = self.pygameInstance.image.load(
                        "img/pokerimg/" + str(j + 2) + "_of_" + color_en[i] + ".png").convert_alpha()
        return list

    def init_basal_image_data(self):
        basal_image_list = {}
        for key in imgurl_dict:
            basal_image_list[key] = self.pygameInstance.image.load(imgurl_dict[key]).convert()

        return basal_image_list
