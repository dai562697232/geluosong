def load_card_data(pygameInstance):
    print("图像数据加载中···")
    color_en = ["spades", "hearts", "clubs", "diamonds"]
    list = {}
    for i in range(4):
        for j in range(12):
            if j + 2 == 10:
                list["jack_of_" + color_en[i]] = pygameInstance.image.load(
                    "img/pokerimg/jack_of_" + color_en[i] + ".png").convert_alpha()
            elif j + 2 == 11:
                list["queen_of_" + color_en[i]] = pygameInstance.image.load(
                    "img/pokerimg/queen_of_" + color_en[i] + ".png").convert_alpha()
            elif j + 2 == 12:
                list["king_of_" + color_en[i]] = pygameInstance.image.load(
                    "img/pokerimg/king_of_" + color_en[i] + ".png").convert_alpha()
            elif j + 2 == 13:
                list["ace_of_" + color_en[i]] = pygameInstance.image.load(
                    "img/pokerimg/ace_of_" + color_en[i] + ".png")
            else:
                list[str(j + 2) + "_of_" + color_en[i]] = pygameInstance.image.load(
                    "img/pokerimg/" + str(j + 2) + "_of_" + color_en[i] + ".png").convert_alpha()
    return list
