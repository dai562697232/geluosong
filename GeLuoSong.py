import pygame
from pygame.locals import *
from sys import exit
from component.Poker import *
from component import Dealer

pygame.init()
pygame.display.set_caption("割罗松")  # 设置标题
#################################################################
# -----------------------初始化数据-------------------------
# 屏幕宽高
screen_width = 1366
screen_height = 768

# 扑克宽高
# card_width = 110
# card_height = 159
# # 极小
# X_SMALL_CARD_SIZE = -2
# X_SMALL_CARD_WIDTH = 55
# X_SMALL_CARD_HEIGHT = 79
#
# # 小
# SMALL_CARD_SIZE = -1
# SMALL_CARD_WIDTH = 75
# SMALL_CARD_HEIGHT = 108
# # 一般大小
# NORMAL_CARD_SIZE = 0
# NORMAL_CARD_WIDTH = 110
# NORMAL_CARD_HEIGHT = 159

# 放置区域高度
put_area_height = screen_height / 2 + 40
# 第一道放置区域开始位置
first_put_area_x_start = (screen_width - 15 * SMALL_CARD_WIDTH - 40) / 2
# 第二道放置区域开始位置
second_put_area_x_start = first_put_area_x_start + 4 * SMALL_CARD_WIDTH + 20
# 第三道放置区域开始位置
third_put_area_x_start = second_put_area_x_start + 6 * SMALL_CARD_WIDTH + 20

# 设置屏幕参数
screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE, 32)
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
exchange_button_width = 75
exchange_button_height = 67
exchange_button_start_width = third_put_area_x_start - SMALL_CARD_WIDTH - 10
exchange_button_start_height = put_area_height + (SMALL_CARD_HEIGHT - exchange_button_height) / 2

# 右下角功能键区域
lr_function_buttons_width = 130
lr_function_buttons_height = 51
lr_function_buttons_start_width = 1150
lr_function_buttons_start_height = 605
lr_function_buttons_start_space = 50
lr_function_buttons_surf_list = [buttons_image_data[FINISH_PUT_BUTTON], buttons_image_data[SORT_SWITCH_BUTTON],
                                 buttons_image_data[CANCEL_ALL_BUTTON]]
lr_function_outline_buttons_surf_list = [buttons_image_data[FINISH_PUT_OUTLINE_BUTTON],
                                         buttons_image_data[SORT_SWITCH_OUTLINE_BUTTON],
                                         buttons_image_data[CANCEL_ALL_OUTLINE_BUTTON]]

# 玩家底部卡牌间距
player1_area_card_spacing = 50
players = Dealer.deal()
player1 = players[0]
player1_card_area_x_start = 0
pre_selected_out_height = 50
# player1_area_start_width = int(
#     screen_width / 2 - ((player1.__len__() - 1) * player1_area_card_spacing + card_width) / 2)

player2 = players[1]
player3 = players[2]
player4 = players[3]

first_put_group = CardGroup([], True)
second_put_group = CardGroup([], True)
third_put_group = CardGroup([], True)

clock = pygame.time.Clock

# 设置 FPS
FPS = 90
FramePerSec = pygame.time.Clock()

mouse_left_button_click = mouse_wheel_click = mouse_right_button_click = False
start = False

flag = 0

# area 集合区域  0 = player1  1 = first_put 2=second_put ..
hand_pre_selected = -1
first_put_pre_selected = -1
hand_card_moving = False
first_put_card_moving = False

sort_by_value = True


# 左键单击
def mouse_l_click(event):
    return event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and not pygame.mouse.get_pressed()[2]


# 右键单击
def mouse_r_click(event):
    return event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2] and not pygame.mouse.get_pressed()[0]


groups = [first_put_group, second_put_group, third_put_group]
put_area_start_width_list = [first_put_area_x_start, second_put_area_x_start, third_put_area_x_start]
max_number = [3, 5, 5]
pre_selected_list = [-1, -1, -1]
put_area_cards_moving = -1

finish_put = False

full_screen = False


def handle_card_moving(group_index=-1):
    global put_area_cards_moving
    if group_index == -1:
        if len(player1.sprites()) > 0:
            cur_card = player1.sprites()[hand_pre_selected]
            cur_card.selected(screen, (
                current_mouse_pos_x - cur_card.card_width / 2, current_mouse_pos_y - cur_card.card_height / 2))
            if current_mouse_button_pressed_L:
                pass
            else:
                put_done = False
                for i in range(len(put_area_start_width_list)):
                    if put_area_start_width_list[i] - SMALL_CARD_WIDTH / 2 < current_mouse_pos_x < \
                            put_area_start_width_list[i] + (max_number[i] + 1 / 2) * SMALL_CARD_WIDTH and \
                            put_area_height - SMALL_CARD_HEIGHT / 2 < current_mouse_pos_y < put_area_height + 3 / 2 * SMALL_CARD_HEIGHT:
                        if len(groups[i]) < max_number[i]:
                            player1.remove(cur_card)
                            cur_card.resize(-1)
                            groups[i].add(cur_card)
                            groups[i].sort_cards(True)
                            put_done = True
                        else:
                            if not put_done:
                                cur_card.resize(0)

                    else:
                        if not put_done:
                            cur_card.resize()


    else:
        if pre_selected_list[group_index] != -1:
            cur_card = groups[group_index].sprites()[pre_selected_list[group_index]]
            cur_card.selected(screen, (
                current_mouse_pos_x - cur_card.card_width / 2, current_mouse_pos_y - cur_card.card_height / 2))
            if current_mouse_button_pressed_L:
                pass
            else:
                for i in range(len(put_area_start_width_list)):
                    if i == group_index:
                        pass
                    else:
                        if put_area_start_width_list[i] - SMALL_CARD_WIDTH / 2 < current_mouse_pos_x < \
                                put_area_start_width_list[i] + (max_number[i] + 1 / 2) * SMALL_CARD_WIDTH and \
                                put_area_height - SMALL_CARD_HEIGHT / 2 < current_mouse_pos_y < put_area_height + 3 / 2 * SMALL_CARD_HEIGHT:
                            if len(groups[i]) < max_number[i]:
                                groups[group_index].remove(cur_card)
                                cur_card.resize(-1)
                                groups[i].add(cur_card)
                                groups[i].sort_cards(True)
                                pre_selected_list[group_index] = -1
                                put_area_cards_moving = -1
                        else:
                            print("else")
                            pre_selected_list[group_index] = -1
                            put_area_cards_moving = -1


def hand_card_quick_put(index):
    key_list = [K_1, K_2, K_3]
    for i in range(len(key_list)):
        if event.type == KEYDOWN and pygame.key.get_pressed()[key_list[i]] == 1 and len(
                groups[i].sprites()) < max_number[i]:
            card = player1.sprites()[index]
            player1.remove(card)
            card.resize(-1)
            groups[i].add(card)
            groups[i].sort_cards(True)
            index = -1

    return index


def on_mouse_to_put_area():
    for i in range(len(put_area_start_width_list)):
        if put_area_start_width_list[i] < current_mouse_pos_x < put_area_start_width_list[i] + max_number[
            i] * SMALL_CARD_WIDTH \
                and put_area_height < current_mouse_pos_y < put_area_height + SMALL_CARD_HEIGHT:
            if len(groups[i]) > 0:
                if mouse_l_click(event):
                    for j in range(len(groups[i])):
                        if j * SMALL_CARD_WIDTH < current_mouse_pos_x - put_area_start_width_list[i] < (
                                j + 1) * SMALL_CARD_WIDTH:
                            global put_area_cards_moving
                            put_area_cards_moving = i
                            pre_selected_list[i] = j

            if mouse_r_click(event):
                for j in range(len(groups[i])):
                    if j * SMALL_CARD_WIDTH < current_mouse_pos_x - put_area_start_width_list[i] < (
                            j + 1) * SMALL_CARD_WIDTH:
                        card = groups[i].sprites()[j]
                        card.resize()
                        groups[i].remove(card)
                        player1.add(card)
                        player1.sort_cards(sort_by_value)


def on_mouse_to_lr_function_area():
    global finish_put
    global sort_by_value
    for i in range(len(lr_function_buttons_surf_list)):
        if lr_function_buttons_start_width < current_mouse_pos_x < lr_function_buttons_width + \
                lr_function_buttons_start_width and lr_function_buttons_start_height + \
                i * lr_function_buttons_start_space < current_mouse_pos_y < lr_function_buttons_start_height + \
                i * lr_function_buttons_start_space + lr_function_buttons_height:
            if i == 0 and len(player1.sprites()) > 0:
                pass
            else:
                screen.blit(pygame.transform.smoothscale(lr_function_outline_buttons_surf_list[i],
                                                         (lr_function_buttons_width, lr_function_buttons_height)), (
                                lr_function_buttons_start_width,
                                lr_function_buttons_start_height + i * lr_function_buttons_start_space))
            if mouse_l_click(event):
                if i == 0 and len(player1.sprites()) == 0:
                    finish_put = True
                    print(finish_put)

                if i == 1 and len(player1.sprites()) > 0:
                    sort_by_value = not sort_by_value
                    player1.sort_cards(sort_by_value)

                if i == 2 and len(player1.sprites()) != 13:
                    for i in range(len(groups)):
                        if len(groups[i].sprites()) > 0:
                            list = groups[i].sprites()
                            groups[i].remove(list)
                            player1.add(list)
                            player1.sort_cards(sort_by_value)
                            player1.resize()


def on_exchange():
    if exchange_button_start_width < current_mouse_pos_x < exchange_button_start_width + exchange_button_width and \
            exchange_button_start_height < current_mouse_pos_y < exchange_button_start_height + exchange_button_height:

        screen.blit(pygame.transform.smoothscale(buttons_image_data[EXCHANGE_OUTLINE_BUTTON],
                                                 (exchange_button_width, exchange_button_height)),
                    (exchange_button_start_width, exchange_button_start_height))
        if mouse_l_click(event):
            if len(second_put_group.sprites()) > 0 or len(third_put_group.sprites()) > 0:
                list2 = second_put_group.sprites()
                list3 = third_put_group.sprites()
                second_put_group.remove(list2)
                second_put_group.add(list3)
                third_put_group.remove(list3)
                third_put_group.add(list2)
                second_put_group.resize(-1)
                third_put_group.resize(-1)


while True:
    for event in pygame.event.get():

        # 退出游戏
        if event.type == QUIT:
            print("bye!")
            exit()
        if event.type == VIDEORESIZE:
            # 更新比例
            cur_screen_width, cur_screen_height = pygame.display.get_window_size()
            width_scale = cur_screen_width / screen_width
            height_scale = cur_screen_height / screen_height

            # 屏幕宽高
            screen_width = int(screen_width * width_scale)
            screen_height = int(screen_height * height_scale)
            # 放置区域高度
            put_area_height = int(put_area_height * height_scale)
            # 第一道放置区域开始位置
            first_put_area_x_start = int(first_put_area_x_start * width_scale)
            # 第二道放置区域开始位置
            second_put_area_x_start = int(second_put_area_x_start * width_scale)
            # 第三道放置区域开始位置
            third_put_area_x_start = int(third_put_area_x_start * width_scale)

            put_area_start_width_list = [first_put_area_x_start, second_put_area_x_start, third_put_area_x_start]

            # 设置按钮
            exchange_button_width = int(exchange_button_width * width_scale)
            exchange_button_height = int(exchange_button_height * height_scale)
            exchange_button_start_width = int(exchange_button_start_width * width_scale)
            exchange_button_start_height = int(exchange_button_start_height * height_scale)
            # 右下角功能键区域
            lr_function_buttons_width = int(lr_function_buttons_width * width_scale)
            lr_function_buttons_height = int(lr_function_buttons_height * height_scale)
            lr_function_buttons_start_width = int(lr_function_buttons_start_width * width_scale)
            lr_function_buttons_start_height = int(lr_function_buttons_start_height * height_scale)
            lr_function_buttons_start_space = int(lr_function_buttons_start_space * height_scale)

            # 玩家底部卡牌间距
            player1_area_card_spacing = int(player1_area_card_spacing * width_scale)
            player1_card_area_x_start = int(player1_card_area_x_start * width_scale)
            pre_selected_out_height = int(pre_selected_out_height * height_scale)

            X_SMALL_CARD_WIDTH = int(X_SMALL_CARD_WIDTH * width_scale)
            X_SMALL_CARD_HEIGHT = int(X_SMALL_CARD_HEIGHT * height_scale)

            # 小
            SMALL_CARD_WIDTH = int(SMALL_CARD_WIDTH * width_scale)
            SMALL_CARD_HEIGHT = int(SMALL_CARD_HEIGHT * height_scale)
            # 一般大小
            NORMAL_CARD_WIDTH = int(NORMAL_CARD_WIDTH * width_scale)
            NORMAL_CARD_HEIGHT = int(NORMAL_CARD_HEIGHT * height_scale)
            resize_cards_const(width_scale, height_scale)
            print(first_put_area_x_start)
            for i in range(len(groups)):
                groups[i].resize(-1)
            player1.resize()
        # 获取鼠标信息
        current_mouse_pos_x, current_mouse_pos_y = pygame.mouse.get_pos()
        current_mouse_button_pressed_L = pygame.mouse.get_pressed()[0]
        current_mouse_button_pressed_R = pygame.mouse.get_pressed()[2]
        # 开始游戏
        if start:

            # if not full_screen:
            #     pygame.display.toggle_fullscreen()
            #     full_screen = True
            # 渲染组件
            screen.blit(pygame.transform.smoothscale(background2, (screen_width, screen_height)), (0, 0))
            pygame.draw.rect(screen, (35, 104, 155),
                             (first_put_area_x_start, put_area_height, 3 * SMALL_CARD_WIDTH, SMALL_CARD_HEIGHT), 2)
            pygame.draw.rect(screen, (35, 104, 155),
                             (second_put_area_x_start, put_area_height, 5 * SMALL_CARD_WIDTH, SMALL_CARD_HEIGHT), 2)
            pygame.draw.rect(screen, (35, 104, 155),
                             (third_put_area_x_start, put_area_height, 5 * SMALL_CARD_WIDTH, SMALL_CARD_HEIGHT), 2)

            # 渲染右下角功能区
            for i in range(len(lr_function_buttons_surf_list)):
                if i == 0:
                    if len(player1.sprites()) > 0:
                        pass
                    else:
                        screen.blit(pygame.transform.smoothscale(lr_function_buttons_surf_list[i],
                                                                 (lr_function_buttons_width,
                                                                  lr_function_buttons_height)), (
                                        lr_function_buttons_start_width,
                                        lr_function_buttons_start_height + i * lr_function_buttons_start_space))

                else:
                    screen.blit(pygame.transform.smoothscale(lr_function_buttons_surf_list[i],
                                                             (lr_function_buttons_width, lr_function_buttons_height)), (
                                    lr_function_buttons_start_width,
                                    lr_function_buttons_start_height + i * lr_function_buttons_start_space))

            screen.blit(pygame.transform.smoothscale(buttons_image_data[MENU_BUTTON_OUTLINE], (160, 47)),
                        (screen_width - 160-10, 10))

            screen.blit(pygame.transform.smoothscale(buttons_image_data[EXCHANGE_BUTTON],
                                                     (exchange_button_width, exchange_button_height)),
                        (exchange_button_start_width, exchange_button_start_height))

            # 获取手牌区域位置数据
            cards_len = len(player1.sprites())
            player1_card_area_x_start = int(
                screen_width / 2 - ((len(player1.sprites()) - 1) * player1_area_card_spacing + NORMAL_CARD_WIDTH) / 2)
            player1_card_area_x_end = player1_card_area_x_start + (
                    cards_len - 1) * player1_area_card_spacing + NORMAL_CARD_WIDTH
            player1_card_area_y_start = screen_height - NORMAL_CARD_HEIGHT - 10
            player1_card_area_y_end = screen_height - 10

            player1.draw_to(screen, (player1_card_area_x_start, screen_height - NORMAL_CARD_HEIGHT - 10),
                            space=player1_area_card_spacing, pre_selected=hand_pre_selected)
            player2.resize(-2)
            player2.draw_to(screen, (0, 0))

            # 渲染放置区域
            for i in range(len(groups)):
                groups[i].draw_to(screen, (put_area_start_width_list[i], put_area_height), 0, pre_selected_list[i])

            if hand_card_moving and len(player1.sprites()) > 0:
                handle_card_moving()

            elif put_area_cards_moving != -1:
                handle_card_moving(put_area_cards_moving)


            else:

                # 检测鼠标位置

                # 右下侧按钮区域
                on_mouse_to_lr_function_area()

                # 第二道第三道交换按钮
                on_exchange()
                # 鼠标进入手牌区域 => 手牌预选状态
                selected = -1
                if player1_card_area_x_start < current_mouse_pos_x < player1_card_area_x_end and \
                        player1_card_area_y_start < current_mouse_pos_y < player1_card_area_y_end:
                    # print(current_mouse_pos_x - player1_area_start_width)

                    index = -1

                    for i in range(cards_len):
                        if i != cards_len - 1:
                            if i * player1_area_card_spacing < current_mouse_pos_x - player1_card_area_x_start <= (
                                    i + 1) * player1_area_card_spacing:
                                index = i
                        else:
                            if i * player1_area_card_spacing < current_mouse_pos_x - player1_card_area_x_start <= i \
                                    * player1_area_card_spacing + player1.sprites()[0].card_width:
                                index = i

                    index = hand_card_quick_put(index)
                    if mouse_l_click(event):
                        hand_card_moving = True
                    if index == -1:
                        pass
                    else:
                        if len(player1.sprites()) > 0:
                            player1.sprites()[index].pre_select(screen, (
                                player1_card_area_x_start + index * player1_area_card_spacing,
                                screen_height - NORMAL_CARD_HEIGHT - pre_selected_out_height))
                            hand_pre_selected = index
                else:
                    hand_pre_selected = -1

                # 鼠标进入放置区域
                on_mouse_to_put_area()

            # 定义鼠标按键点击
            # 判断左键单击

            if current_mouse_button_pressed_L:
                pass
            # 判断左键收起
            else:
                hand_card_moving = False
                first_put_card_moving = False
                pre_selected_list[0] = -1


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
