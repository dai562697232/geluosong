# import pygame
#
#
def on_mouse_moving():
    cur_mouse_x, cur_mouse_y = pygame.mouse.get_pos()

    cards_len = len(player1.sprites())
    player1_card_area_x_start = player1_area_start_width
    player1_card_area_x_end = player1_area_start_width + cards_len * player1_area_card_spacing + player1.sprites()[
        0].card_width
    player1_card_area_y_start = screen_height - player1.sprites()[0].card_width - 10
    player1_card_area_y_end = screen_height - 10
    if player1_card_area_x_end < cur_mouse_x < player1_card_area_x_start and \
            player1_card_area_y_start < cur_mouse_y < player1_card_area_y_end:
        print("hello")
