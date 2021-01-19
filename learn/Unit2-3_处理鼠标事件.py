background_image_filename = 'img/skya.png'
mouse_image_filename = 'img/back.png'

import pygame
from pygame.locals import *
from sys import exit

pygame.init()
pygame.display.set_caption("割罗松")
screen_width = 1366
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
background = pygame.image.load(background_image_filename).convert()
mouse_cursor = pygame.image.load(mouse_image_filename).convert_alpha()
mouse_cursor = pygame.transform.scale(mouse_cursor, (80, 110))

x, y = 0, 0
move_x, move_y = 0, 0
offset_x = 0
offset_y = 0


FPS = 60
FramePerSec = pygame.time.Clock()

mouse_moving = False

dyd_x = 73
d_y = screen_height / 2 + 40
mark = 0
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

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
            x = x + offset_x - 80
            y = y + offset_y - 110
            if x < 0 or x > screen_width-80:
                x = 0 if x < 0 else screen_width-80
            if y < 0 or y > screen_height-110:
                y = 0 if y < 0 else screen_height-110
        else:
            if 0<=x<dyd_x+240 and d_y-110<y<d_y+110:

                 x=dyd_x
                 y=d_y


            # x += 80
            # y += 110
        # 计算出新的坐标
        # x+= move_x
        # y+= move_y
        # print(offset_x,offset_y)
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (35, 104, 155), (dyd_x, d_y, 240, 110), 2)
        pygame.draw.rect(screen, (35, 104, 155), (dyd_x + 320+20,d_y, 400, 110), 2)
        pygame.draw.rect(screen, (35, 104, 155), (dyd_x + 800+20, d_y, 400, 110), 2)
        screen.blit(mouse_cursor, (x, y))
        # 在新的位置上画图
        pygame.display.update()
        FramePerSec.tick(FPS)
