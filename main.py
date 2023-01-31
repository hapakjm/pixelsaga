import pygame
import sys
import resources as res
import barneyGame
import tiktaktoeGame
import snakeGame

pygame.init()
pygame.display.set_caption('G2 Games')
G2GICON = pygame.image.load(res.resource_path("G2icon.jpg"))
pygame.display.set_icon(G2GICON)

RUNNING_BARNEY_GIF = res.import_barney_game_gif((300, 150))
SNAKE_GIF = res.import_snake_game_gif((300, 150))
TIKTAKTOE_GIF = res.import_tiktaktoe_game_gif((300, 150))


def display_boxes_main(screen):
    res.display_rectangle(screen,
                          color=res.AQUA,
                          position=(res.SCREEN_WIDTH // 2,
                                    res.SCREEN_HEIGHT // 2 + 25),
                          dimension=(800, 450))


def display_texts_main(screen):
    res.display_text(screen,
                     text="G2 Games",
                     size=100,
                     color=res.GREEN,
                     position=(400, 25))
    res.display_text(screen,
                     text="Running Barney",
                     size=75,
                     color=res.WHITE,
                     position=(200, 150))
    res.display_text(screen,
                     text="Snake",
                     size=75,
                     color=res.WHITE,
                     position=(200, 300))
    res.display_text(screen,
                     text="Tik-Tak-Toe",
                     size=75,
                     color=res.WHITE,
                     position=(200, 450))


def display_barney_gif_main(screen):
    global barney_timer
    barney_timer = res.display_image(screen,
                                     images=RUNNING_BARNEY_GIF,
                                     rect=(650, 100, 300, 150),
                                     counter=barney_timer,
                                     speed=8)


def display_snake_gif_main(screen):
    global snake_timer
    snake_timer = res.display_image(screen,
                                    images=SNAKE_GIF,
                                    rect=(650, 250, 300, 150),
                                    counter=snake_timer,
                                    speed=8)


def display_tiktaktoe_gif_main(screen):
    global tiktakktoe_timer
    tiktakktoe_timer = res.display_image(screen,
                                         images=TIKTAKTOE_GIF,
                                         rect=(650, 400, 300, 150),
                                         counter=tiktakktoe_timer,
                                         speed=8)


def display_box_borders_main(screen):
    pygame.draw.rect(screen, res.YELLOW, (150, 100, 500, 150), 2)
    pygame.draw.rect(screen, res.YELLOW, (150, 250, 500, 150), 2)
    pygame.draw.rect(screen, res.YELLOW, (150, 400, 500, 150), 2)
    pygame.draw.rect(screen, res.YELLOW, (650, 100, 300, 150), 2)
    pygame.draw.rect(screen, res.YELLOW, (650, 250, 300, 150), 2)
    pygame.draw.rect(screen, res.YELLOW, (650, 400, 300, 150), 2)


def check_mouse_position_box1_main(mouse_x, mouse_y):
    if (mouse_x >= 175 and mouse_x <= 950) and (mouse_y >= 100 and mouse_y <= 250):
        return True


def check_mouse_position_box2_main(mouse_x, mouse_y):
    if (mouse_x >= 175 and mouse_x <= 950) and (mouse_y >= 250 and mouse_y <= 400):
        return True


def check_mouse_position_box3_main(mouse_x, mouse_y):
    if (mouse_x >= 175 and mouse_x <= 950) and (mouse_y >= 400 and mouse_y <= 550):
        return True


def check_mouse_position_boxes_main(mouse_x, mouse_y):
    if check_mouse_position_box1_main(mouse_x, mouse_y):
        return 1
    if check_mouse_position_box2_main(mouse_x, mouse_y):
        return 2
    if check_mouse_position_box3_main(mouse_x, mouse_y):
        return 3


def mouse_hover_main(screen, mouse_x, mouse_y):
    temp = check_mouse_position_boxes_main(mouse_x, mouse_y)
    if temp == 1:
        res.display_rectangle(screen,
                              color=res.BLACK,
                              position=(400, 175),
                              dimension=(500, 150))
    elif temp == 2:
        res.display_rectangle(screen,
                              color=res.BLACK,
                              position=(400, 325),
                              dimension=(500, 150))
    elif temp == 3:
        res.display_rectangle(screen,
                              color=res.BLACK,
                              position=(400, 475),
                              dimension=(500, 150))


def box_clicked_main(screen, clicked_l, mouse_x, mouse_y):
    if clicked_l:
        box = check_mouse_position_boxes_main(mouse_x, mouse_y)
        if box == 1:
            box_l_click_event_main(screen, 175)
            barneyGame.menu().main()
        elif box == 2:
            box_l_click_event_main(screen, 325)
            snakeGame.menu().main()
        elif box == 3:
            box_l_click_event_main(screen, 475)
            tiktaktoeGame.menu().main()


def box_l_click_event_main(screen, y_pos):
    res.display_rectangle(screen,
                          color=res.MAGENTA,
                          position=(400, y_pos),
                          dimension=(500, 150))


def main():
    global barney_timer, snake_timer, tiktakktoe_timer
    pygame.display.set_icon(res.G2GICON)
    SCREEN = pygame.display.set_mode((res.SCREEN_WIDTH, res.SCREEN_HEIGHT))
    res.BG_MUSIC.load(res.resource_path("Theme.wav"))
    res.BG_MUSIC.play(-1)
    run = True
    clock = pygame.time.Clock()
    barney_timer = 0
    snake_timer = 0
    tiktakktoe_timer = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            clicked_l = res.check_mouse_l_click(event)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        SCREEN.fill(res.BLUE)
        display_boxes_main(SCREEN)
        mouse_hover_main(SCREEN, mouse_x, mouse_y)
        box_clicked_main(SCREEN, clicked_l, mouse_x, mouse_y)
        display_texts_main(SCREEN)
        display_barney_gif_main(SCREEN)
        display_snake_gif_main(SCREEN)
        display_tiktaktoe_gif_main(SCREEN)
        display_box_borders_main(SCREEN)

        clock.tick(60)
        pygame.display.update()


if __name__ == '__main__':
    main()
