import pygame
from pygame.locals import *
from sys import exit
from game.component.InitImageData import *
from game.component.Poker import *
from game.component import Dealer
from game.component import MyEvents

pygame.init()
pygame.display.set_caption("割罗松")  # 设置标题
#################################################################
# -----------------------初始化数据-------------------------
# 屏幕宽高
screen_width = 1366
screen_height = 768

# 扑克宽高
card_width = 110
card_height = 159

# 放置区域高度
put_area_height = screen_height / 2 + 40
# 第一道放置区域开始位置
first_put_area_x_start = 100
# 第二道放置区域开始位置
second_put_area_x_start = first_put_area_x_start + 300 + 20
# 第三道放置区域开始位置
third_put_area_x_start = first_put_area_x_start + 750 + 40

# 设置屏幕参数
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
# 加载图像数据
cards_image_data = ImageData.get_cards_image_data()
basal_image_data = ImageData.get_basic_image_data()
buttons_image_data = ImageData.get_buttons_image_data()

# 设置背景图像
background1 = basal_image_data[BACKGROUND_WELCOME_IMAGE]
background2 = basal_image_data[BACKGROUND_GAME_IMAGE]

# 设置按钮
play_button_surf = buttons_image_data[PLAY_BUTTON_IMG]
play_button_dark_surf = buttons_image_data[PLAY_BUTTON_DARK_IMG]

sort_switch_surf = buttons_image_data[SORT_SWITCH_BUTTON]
sort_switch_outline_surf = buttons_image_data[SORT_SWITCH_OUTLINE_BUTTON]
cancel_all_surf = buttons_image_data[CANCEL_ALL_BUTTON]
cancel_all_outline_surf = buttons_image_data[CANCEL_ALL_OUTLINE_BUTTON]
finish_put_button_surf = buttons_image_data[FINISH_PUT_BUTTON]
finish_put_outline_button_surf = buttons_image_data[FINISH_PUT_OUTLINE_BUTTON]

# 玩家底部卡牌间距
player1_area_card_spacing = 50
players = Dealer.deal()
player1 = players[0]
player1_card_area_x_start = 0
# player1_area_start_width = int(
#     screen_width / 2 - ((player1.__len__() - 1) * player1_area_card_spacing + card_width) / 2)

first_put_group = CardGroup([], True)
second_put_group = CardGroup([], True)
third_put_group = CardGroup([], True)

mouse_cursor = pygame.transform.scale(cards_image_data["ace_of_clubs"], (card_width, card_height))
mouse_cursor2 = pygame.transform.scale(cards_image_data["king_of_clubs"], (card_width, card_height))

clock = pygame.time.Clock

x, y = 195, 768 - card_height
offset_x = 0
offset_y = 0

# 设置 FPS
FPS = 120
FramePerSec = pygame.time.Clock()

mouse_moving = False
mouse_left_button_click = mouse_wheel_click = mouse_right_button_click = False
start = False

flag = 0

# area 集合区域  0 = player1  1 = first_put 2=second_put ..
CARD_MOVING_EVENTS = {"moving": False, "group": CardGroup([], True), "area": -1}
pre_selected = -1
hand_card_moving = False
first_put_card_moving = False

sort_by_value = True
while True:
    for event in pygame.event.get():

        # 退出游戏
        if event.type == QUIT:
            exit()

        # 获取鼠标坐标
        current_mouse_pos_x, current_mouse_pos_y = pygame.mouse.get_pos()
        current_mouse_button_pressed_L = pygame.mouse.get_pressed()[0]
        current_mouse_button_pressed_R = pygame.mouse.get_pressed()[2]

        # 开始游戏
        if start:

            # 渲染组件
            screen.blit(background2, (0, 0))
            pygame.draw.rect(screen, (35, 104, 155),
                             (first_put_area_x_start, put_area_height, 3 * SMALL_CARD_WIDTH, SMALL_CARD_HEIGHT), 2)
            pygame.draw.rect(screen, (35, 104, 155),
                             (second_put_area_x_start, put_area_height, 5 * SMALL_CARD_WIDTH, SMALL_CARD_HEIGHT), 2)
            pygame.draw.rect(screen, (35, 104, 155),
                             (third_put_area_x_start, put_area_height, 5 * SMALL_CARD_WIDTH, SMALL_CARD_HEIGHT), 2)

            screen.blit(pygame.transform.scale(finish_put_button_surf, (130, 51)), (1150, 605))
            screen.blit(pygame.transform.scale(sort_switch_surf, (130, 51)), (1150, 655))
            screen.blit(pygame.transform.scale(cancel_all_surf, (130, 51)), (1150, 705))

            # 获取手牌区域位置数据
            cards_len = len(player1.sprites())
            player1_card_area_x_start = int(
                screen_width / 2 - ((len(player1.sprites()) - 1) * player1_area_card_spacing + card_width) / 2)
            player1_card_area_x_end = player1_card_area_x_start + (
                    cards_len - 1) * player1_area_card_spacing + NORMAL_CARD_WIDTH
            player1_card_area_y_start = screen_height - NORMAL_CARD_HEIGHT - 10
            player1_card_area_y_end = screen_height - 10

            player1.draw_to(screen, (player1_card_area_x_start, screen_height - NORMAL_CARD_HEIGHT - 10),
                            space=player1_area_card_spacing, pre_selected=pre_selected)
            first_put_group.draw_to(surface=screen, xy=(first_put_area_x_start, put_area_height), space=0,
                                    pre_selected=pre_selected)

            #  检测是否在移动扑克
            # if CARD_MOVING_EVENTS["moving"]:
            #     cur_card = CARD_MOVING_EVENTS["group"].sprites()[pre_selected]
            #     cur_card.selected(screen, (
            #         current_mouse_pos_x - cur_card.card_width / 2, current_mouse_pos_y - cur_card.card_height / 2))
            #     card_list = player1.sprites()[pre_selected:pre_selected + 1]
            #
            #     if event.type == MOUSEBUTTONUP:
            #         if CARD_MOVING_EVENTS["area"] == 0:
            #             if first_put_area_x_start - SMALL_CARD_WIDTH / 2 < current_mouse_pos_x < first_put_area_x_start + (
            #                     3 + 1 / 2) * SMALL_CARD_WIDTH and \
            #                     put_area_height - SMALL_CARD_HEIGHT / 2 < current_mouse_pos_y < put_area_height + 3 / 2 * SMALL_CARD_HEIGHT:
            #                 if len(first_put_group) < 3:
            #                     player1.remove(cur_card)
            #                     first_put_group.add(cur_card)
            #                     first_put_group.sort_cards(True)
            #                 else:
            #                     cur_card.resize()
            #             else:
            #                 cur_card.resize()

            if hand_card_moving:
                cur_card = player1.sprites()[pre_selected]
                cur_card.selected(screen, (
                    current_mouse_pos_x - cur_card.card_width / 2, current_mouse_pos_y - cur_card.card_height / 2))
                card_list = player1.sprites()[pre_selected:pre_selected + 1]

                if event.type == MOUSEBUTTONUP:
                    # print(current_mouse_pos_x,current_mouse_pos_y)
                    if first_put_area_x_start - SMALL_CARD_WIDTH / 2 < current_mouse_pos_x < first_put_area_x_start + (
                            3 + 1 / 2) * SMALL_CARD_WIDTH and \
                            put_area_height - SMALL_CARD_HEIGHT / 2 < current_mouse_pos_y < put_area_height + 3 / 2 * SMALL_CARD_HEIGHT:
                        if len(first_put_group) < 3:
                            player1.remove(cur_card)
                            first_put_group.add(cur_card)
                            first_put_group.sort_cards(True)
                        else:
                            cur_card.resize()
                    else:
                        cur_card.resize()

            else:

                # 检测鼠标位置

                # 右下侧按钮区域
                if 1150 < current_mouse_pos_x < 1150 + 130 and 605 < current_mouse_pos_y < 605 + 51:
                    screen.blit(pygame.transform.scale(finish_put_outline_button_surf, (130, 51)), (1150, 605))
                if 1150 < current_mouse_pos_x < 1150 + 130 and 655 < current_mouse_pos_y < 655 + 51:
                    screen.blit(pygame.transform.scale(sort_switch_outline_surf, (130, 51)), (1150, 655))
                    if event.type == MOUSEBUTTONDOWN:
                        sort_by_value = not sort_by_value
                        player1.sort_cards(sort_by_value)
                if 1150 < current_mouse_pos_x < 1150 + 130 and 705 < current_mouse_pos_y < 705 + 51:
                    screen.blit(pygame.transform.scale(cancel_all_outline_surf, (130, 51)), (1150, 705))

                # 鼠标进入手牌区域 => 手牌预选状态
                selected = -1
                if player1_card_area_x_start < current_mouse_pos_x < player1_card_area_x_end and \
                        player1_card_area_y_start < current_mouse_pos_y < player1_card_area_y_end:
                    # print(current_mouse_pos_x - player1_area_start_width)
                    index = -1
                    for i in range(cards_len):
                        if i != cards_len - 1:
                            if i * player1_area_card_spacing < current_mouse_pos_x - player1_card_area_x_start < (
                                    i + 1) * player1_area_card_spacing:
                                index = i
                        else:
                            if i * player1_area_card_spacing < current_mouse_pos_x - player1_card_area_x_start < i * player1_area_card_spacing + \
                                    player1.sprites()[0].card_width:
                                index = i

                    if index != -1:
                        player1.sprites()[index].pre_select(screen, (
                            player1_card_area_x_start + index * player1_area_card_spacing,
                            screen_height - NORMAL_CARD_HEIGHT - 50))
                        pre_selected = index
                    # for c in player1.sprites():
                    #     print(c.get_rect())

                    if event.type == MOUSEBUTTONDOWN:
                        # CARD_MOVING_EVENTS["moving"] = True
                        # CARD_MOVING_EVENTS["group"] = player1
                        # CARD_MOVING_EVENTS["area"] = 0
                        hand_card_moving = True

                else:
                    pre_selected = -1

                # 鼠标进入第一道放置区域
                if first_put_area_x_start < current_mouse_pos_x < first_put_area_x_start + 3 * SMALL_CARD_WIDTH and \
                        put_area_height < current_mouse_pos_y < put_area_height + SMALL_CARD_HEIGHT:
                    cards_len = len(first_put_group.sprites())
                    if cards_len > 0:
                        if first_put_area_x_start < current_mouse_pos_x < first_put_area_x_start + cards_len * \
                                SMALL_CARD_WIDTH:
                            if current_mouse_button_pressed_L:
                                for i in range(cards_len):
                                    if i * SMALL_CARD_WIDTH < current_mouse_pos_x - first_put_area_x_start < (
                                            i + 1) * SMALL_CARD_WIDTH:
                                        pre_selected = i
                                        first_put_card_moving = True
                            if current_mouse_button_pressed_R:
                                for i in range(cards_len):
                                    if i * SMALL_CARD_WIDTH < current_mouse_pos_x - first_put_area_x_start < (
                                            i + 1) * SMALL_CARD_WIDTH:
                                        card = first_put_group.sprites()[i]
                                        card.resize()
                                        first_put_group.remove(card)
                                        player1.add(card)
                                        player1.sort_cards(sort_by_value)

            # 定义鼠标按键点击
            # 判断左键单击
            if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if x <= mouse_x <= x + card_width and y <= mouse_y <= y + card_height:
                    offset_x = x + card_width - mouse_x
                    offset_y = y + card_height - mouse_y
                    # print("鼠标点击")
                    mouse_moving = True
            # 判断左键收起
            if event.type == MOUSEBUTTONUP and not pygame.mouse.get_pressed()[0]:
                mouse_moving = False
                CARD_MOVING_EVENTS["moving"] = False
                hand_card_moving =False

            if mouse_moving:
                # print("moving", pygame.mouse.get_pos())
                # print("卡牌信息", mouse_cursor.get_width(), mouse_cursor.get_height())
                # print("偏移量", offset_x, offset_y)
                x, y = pygame.mouse.get_pos()
                x = x + offset_x - card_width
                y = y + offset_y - card_height
                if x < 0 or x > screen_width - card_width:
                    x = 0 if x < 0 else screen_width - card_width
                if y < 0 or y > screen_height - card_height:
                    y = 0 if y < 0 else screen_height - card_height
            else:
                if first_put_area_x_start - card_width <= x < first_put_area_x_start + 240 and \
                        put_area_height - card_height <= y <= put_area_height + card_height:
                    x = first_put_area_x_start
                    y = put_area_height
                else:
                    x, y = 195, 768 - card_height

                # x += 80
                # y += 110
            # 计算出新的坐标
            # x+= move_x
            # y+= move_y
            # print(offset_x,offset_y)


        # 登录界面
        else:
            screen.blit(background1, (0, 0))
            screen.blit(play_button_surf, (530, 330))
            if 530 <= current_mouse_pos_x <= 530 + 310 and 330 <= current_mouse_pos_y <= 330 + 105:
                screen.blit(play_button_dark_surf, (530, 330))
                if event.type == MOUSEBUTTONDOWN:
                    start = True
            # print(play_button_surf.get_rect())
        # 在新的位置上画图
        pygame.display.update()
        FramePerSec.tick(FPS)
