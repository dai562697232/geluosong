
import pygame
from pygame.locals import *
from sys import exit
from game.component.InitImageData import *
from game.component import Poker

pygame.init()
pygame.display.set_caption("割罗松")  # 设置标题

#################################################################
# -----------------------初始化数据-------------------------
# 屏幕宽高
screen_width = 1366
screen_height = 768

# 扑克宽高
card_width = 75
card_height = 110

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
image_data = ImageData(pygame)
card_image_data = image_data.card_image_data
basal_image_data = image_data.basal_image_data

# 设置背景图像
background1 = basal_image_data[BACKGROUND_WELCOME_IMAGE]
background2 = basal_image_data[BACKGROUND_GAME_IMAGE]
play_button_surf = basal_image_data[PLAY_BUTTON_IMG]
play_button_dark_surf = basal_image_data[PLAY_BUTTON_DARK_IMG]

mouse_cursor = pygame.transform.scale(card_image_data["ace_of_clubs"], (card_width, card_height))

clock = pygame.time.Clock



x, y = 195, 768 - card_height
offset_x = 0
offset_y = 0

# 设置 FPS
FPS = 120
FramePerSec = pygame.time.Clock()

mouse_moving = False
start = False
mouse_left_button_click = mouse_wheel_click = mouse_right_button_click = False
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if (start):
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

            screen.blit(background2, (0, 0))
            pygame.draw.rect(screen, (35, 104, 155), (first_put_area_x_start, put_area_height, 225, 110), 2)
            pygame.draw.rect(screen, (35, 104, 155), (second_put_area_x_start, put_area_height, 375, 110), 2)
            pygame.draw.rect(screen, (35, 104, 155), (third_put_area_x_start, put_area_height, 375, 110), 2)
            screen.blit(mouse_cursor, (x, y))
        else:
            screen.blit(background1, (0, 0))
            screen.blit(play_button_surf, (530, 330))
            mx, my = pygame.mouse.get_pos()
            if 530 <= mx <= 530 + 310 and 330 <= my <= 330 + 105:
                screen.blit(play_button_dark_surf, (530, 330))
                if event.type == MOUSEBUTTONDOWN:
                    start = True

        # 在新的位置上画图
        pygame.display.update()
        FramePerSec.tick(FPS)
