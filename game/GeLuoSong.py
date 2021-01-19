background_image_index = 'img/gls1366_768.png'
background_image_filename = 'img/sky_background.png'
mouse_image_filename = 'img/back.png'
play_img_url = 'img/play.png'
play_dark_img_url = 'img/play_dark.png'
import pygame
from pygame.locals import *
from sys import exit
from game.component import LoadImgData

pygame.init()
pygame.display.set_caption("割罗松")  # 设置标题

# 设置屏幕参数
screen_width = 1366
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
# 加载图像数据
list = LoadImgData.load_card_data(pygame)
# 设置背景图像
background1 = pygame.image.load(background_image_index).convert()
background2 = pygame.image.load(background_image_filename).convert()
play_img = pygame.transform.scale(pygame.image.load(play_img_url).convert(), (310, 105))
play_dark_img = pygame.transform.scale(pygame.image.load(play_dark_img_url).convert(), (310, 105))

# mouse_cursor = pygame.image.load(list["ace_of_clubs"]).convert_alpha()
# mouse_cursor = pygame.image.load(mouse_image_filename).convert_alpha()
mouse_cursor = pygame.transform.scale(list["ace_of_clubs"], (75, 110))

x, y = 0, 0
offset_x = 0
offset_y = 0

FPS = 60
FramePerSec = pygame.time.Clock()

mouse_moving = False
dyd_x = 100
d_y = screen_height / 2 + 40
mark = 0
start = False
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        print(event)
        if (start):
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if x <= mouse_x <= x + 80 and y <= mouse_y <= y + 110:
                    offset_x = x + 80 - mouse_x
                    offset_y = y + 110 - mouse_y
                    # print("鼠标点击")
                    mouse_moving = True
            if event.type == MOUSEBUTTONUP:
                mouse_moving = False

            if mouse_moving:
                # print("moving", pygame.mouse.get_pos())
                # print("卡牌信息", mouse_cursor.get_width(), mouse_cursor.get_height())
                # print("偏移量", offset_x, offset_y)
                x, y = pygame.mouse.get_pos()
                x = x + offset_x - 75
                y = y + offset_y - 110
                if x < 0 or x > screen_width - 75:
                    x = 0 if x < 0 else screen_width - 75
                if y < 0 or y > screen_height - 110:
                    y = 0 if y < 0 else screen_height - 110
            else:
                if 0 <= x < dyd_x + 240 and d_y - 110 < y < d_y + 110:
                    x = dyd_x
                    y = d_y

                # x += 80
                # y += 110
            # 计算出新的坐标
            # x+= move_x
            # y+= move_y
            # print(offset_x,offset_y)

            screen.blit(background2, (0, 0))
            pygame.draw.rect(screen, (35, 104, 155), (dyd_x, d_y, 225, 110), 2)
            pygame.draw.rect(screen, (35, 104, 155), (dyd_x + 300 + 20, d_y, 375, 110), 2)
            pygame.draw.rect(screen, (35, 104, 155), (dyd_x + 750 + 40, d_y, 375, 110), 2)
            screen.blit(mouse_cursor, (x, y))
        else:
            screen.blit(background1, (0, 0))
            screen.blit(play_img, (530, 330))
            mx, my = pygame.mouse.get_pos()
            if 530 <= mx <= 530 + 310 and 330 <= my <= 330 + 105:
                screen.blit(play_dark_img, (530, 330))
                if event.type == MOUSEBUTTONDOWN:
                    start = True

        # 在新的位置上画图
        pygame.display.update()
        FramePerSec.tick(FPS)
