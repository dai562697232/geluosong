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
second_put_area_x_start = first_put_area_x_start + 4 * SMALL_CARD_WIDTH + 20
# 第三道放置区域开始位置
third_put_area_x_start = second_put_area_x_start + 6 * SMALL_CARD_WIDTH + 20

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

mouse_left_button_click = mouse_wheel_click = mouse_right_button_click = False
start = False

flag = 0

# area 集合区域  0 = player1  1 = first_put 2=second_put ..
CARD_MOVING_EVENTS = {"moving": False, "group": CardGroup([], True), "area": -1, "pre_moving": -1}
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


def handle_card_moving(group_index=-1):
    if group_index == -1:
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
                            cur_card.resize()

                else:
                    if not put_done:
                        cur_card.resize()
    else:
        print(pre_selected_list[group_index])
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
                            put_area_cards_moving = i
                            print(put_area_cards_moving)
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


while True:
    for event in pygame.event.get():

        # 退出游戏
        if event.type == QUIT:
            print("bye!")
            exit()

        # 获取鼠标信息
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
            screen.blit(pygame.transform.scale(buttons_image_data[EXCHANGE_BUTTON], (75, 67)),
                        (third_put_area_x_start - 85, put_area_height + (SMALL_CARD_HEIGHT - 67) / 2))

            # 获取手牌区域位置数据
            cards_len = len(player1.sprites())
            player1_card_area_x_start = int(
                screen_width / 2 - ((len(player1.sprites()) - 1) * player1_area_card_spacing + card_width) / 2)
            player1_card_area_x_end = player1_card_area_x_start + (
                    cards_len - 1) * player1_area_card_spacing + NORMAL_CARD_WIDTH
            player1_card_area_y_start = screen_height - NORMAL_CARD_HEIGHT - 10
            player1_card_area_y_end = screen_height - 10

            player1.draw_to(screen, (player1_card_area_x_start, screen_height - NORMAL_CARD_HEIGHT - 10),
                            space=player1_area_card_spacing, pre_selected=hand_pre_selected)
            first_put_group.draw_to(surface=screen, xy=(first_put_area_x_start, put_area_height), space=0,
                                    pre_selected=pre_selected_list[0])

            second_put_group.draw_to(screen, (second_put_area_x_start, put_area_height))
            third_put_group.draw_to(screen, (third_put_area_x_start, put_area_height))

            if hand_card_moving:
                handle_card_moving()

            elif put_area_cards_moving != -1:
                print("hello")
                handle_card_moving(put_area_cards_moving)


            else:

                # 检测鼠标位置

                # 右下侧按钮区域
                if 1150 < current_mouse_pos_x < 1150 + 130 and 605 < current_mouse_pos_y < 605 + 51:
                    screen.blit(pygame.transform.scale(finish_put_outline_button_surf, (130, 51)), (1150, 605))
                if 1150 < current_mouse_pos_x < 1150 + 130 and 655 < current_mouse_pos_y < 655 + 51:
                    screen.blit(pygame.transform.scale(sort_switch_outline_surf, (130, 51)), (1150, 655))
                    if mouse_l_click(event):
                        sort_by_value = not sort_by_value
                        player1.sort_cards(sort_by_value)
                if 1150 < current_mouse_pos_x < 1150 + 130 and 705 < current_mouse_pos_y < 705 + 51:
                    screen.blit(pygame.transform.scale(cancel_all_outline_surf, (130, 51)), (1150, 705))
                if third_put_area_x_start - 85 < current_mouse_pos_x < third_put_area_x_start - 85 + 67 and \
                        put_area_height + (SMALL_CARD_HEIGHT - 67) / 2 < current_mouse_pos_y < put_area_height + 67 + (
                        SMALL_CARD_HEIGHT - 67) / 2:
                    screen.blit(pygame.transform.scale(buttons_image_data[EXCHANGE_OUTLINE_BUTTON], (75, 67)),
                                (third_put_area_x_start - 85, put_area_height + (SMALL_CARD_HEIGHT - 67) / 2))
                    if mouse_l_click(event):
                        print("exchange")
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
                            if i * player1_area_card_spacing < current_mouse_pos_x - player1_card_area_x_start <= i * player1_area_card_spacing + \
                                    player1.sprites()[0].card_width:
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
                                screen_height - NORMAL_CARD_HEIGHT - 50))
                            hand_pre_selected = index
                else:
                    hand_pre_selected = -1

                # 鼠标进入放置区域
                on_mouse_to_put_area()

            # 定义鼠标按键点击
            # 判断左键单击

            print("hand_card_moving",hand_card_moving)
            if current_mouse_button_pressed_L:
                pass
            # 判断左键收起
            else:
                CARD_MOVING_EVENTS["moving"] = False
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
