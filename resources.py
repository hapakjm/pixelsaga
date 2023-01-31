import os
import sys
import pygame


os.system("cls")


SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
AQUA = (0, 150, 255)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    base_path += "\\G2Games\\Assets\\"
    return os.path.join(base_path, relative_path)


def import_images(directory, image_type, number_of_images, dimension=False):
    if number_of_images > 1:
        thislist = []
        for num in range(0, number_of_images):
            thislist_dir = f" ({num+1}).{image_type}"
            thislist.append(pygame.image.load(
                resource_path(directory) + thislist_dir))
            if dimension != False:
                thislist[num] = pygame.transform.scale(
                    thislist[num], dimension)
        return thislist
    else:
        image = pygame.image.load(resource_path(directory + "." + image_type))
        if dimension != False:
            image = pygame.transform.scale(image, dimension)
        return image


pygame.mixer.init()
BG_MUSIC = pygame.mixer.music
BG_MUSIC.load(resource_path("Theme.wav"))
G2GICON = pygame.image.load(resource_path("G2icon.jpg"))
pygame.display.set_icon(G2GICON)


def import_barney_game_gif(dimension=False):
    return import_images(directory="Menu\\Barney\\RunningBarney",
                         image_type="gif",
                         number_of_images=36,
                         dimension=dimension)


def import_snake_game_gif(dimension=False):
    return import_images(directory="Menu\\Snake\\Snake",
                         image_type="gif",
                         number_of_images=228,
                         dimension=dimension)


def import_tiktaktoe_game_gif(dimension=False):
    return import_images(directory="Menu\\TikTakToe\\TikTakToe",
                         image_type="gif",
                         number_of_images=45,
                         dimension=dimension)


def import_barney_bg_img(dimension=False):
    return import_images(directory="Barney\\Others\\Track",
                         image_type="png",
                         number_of_images=1,
                         dimension=dimension)


def import_start_barney_img(dimension=False):
    return import_images(directory="Barney\\Barney\\BarneyStart",
                         image_type="png",
                         number_of_images=1,
                         dimension=dimension)


def import_running_barney_gif(dimension=False):
    return import_images(directory="Barney\\Barney\\BarneyRun",
                         image_type="png",
                         number_of_images=2,
                         dimension=dimension)


def import_ducking_barney_gif(dimension=False):
    return import_images(directory="Barney\\Barney\\BarneyDuck",
                         image_type="png",
                         number_of_images=2,
                         dimension=dimension)


def import_jumping_barney_img(dimension=False):
    return import_images(directory="Barney\\Barney\\BarneyJump",
                         image_type="png",
                         number_of_images=1,
                         dimension=dimension)


def import_dead_barney_img(dimension=False):
    return import_images(directory="Barney\\Barney\\BarneyDead",
                         image_type="png",
                         number_of_images=1,
                         dimension=dimension)


def import_pacman_gif(dimension=False):
    return import_images(directory="Barney\\Pacman\\Pacman",
                         image_type="png",
                         number_of_images=3,
                         dimension=dimension)


def import_shuriken_gif(dimension=False):
    return import_images(directory="Barney\\Shuriken\\Shuriken",
                         image_type="png",
                         number_of_images=2,
                         dimension=dimension)


def import_start_green_gif(dimension=False):
    return import_images(directory="TikTakToe\\StartGameG\\StartGameG",
                         image_type="gif",
                         number_of_images=12,
                         dimension=dimension)


def import_start_yellow_gif(dimension=False):
    return import_images(directory="TikTakToe\\StartGameY\\StartGameY",
                         image_type="gif",
                         number_of_images=12,
                         dimension=dimension)


def import_x_mark_img(dimension=False):
    return import_images(directory="TikTakToe\\Xmark",
                         image_type="png",
                         number_of_images=1,
                         dimension=dimension)


def import_o_mark_img(dimension=False):
    return import_images(directory="TikTakToe\\Omark",
                         image_type="png",
                         number_of_images=1,
                         dimension=dimension)


def import_coming_soon_img(dimension=False):
    return import_images(directory="Snake\\ComingSoon",
                         image_type="jpg",
                         number_of_images=1,
                         dimension=dimension)


def import_check_img(dimension=False):
    return import_images(directory="Snake\\Check",
                         image_type="png",
                         number_of_images=1,
                         dimension=dimension)


def display_image(screen, images, rect, counter=False, speed=False):
    if speed is False or counter is False:
        screen.blit(images, rect)
    else:
        if speed >= 10:
            speed = 9
        elif speed < 1:
            speed = 0
        image_speed = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        temp = counter // image_speed[speed]
        screen.blit(images[temp], rect)
        counter += 1
        if counter >= (len(images)) * image_speed[speed]:
            counter = 0
        return counter


def display_text(screen, text, size, color, position, font=False):
    if font is False:
        font = 'system'
    font = pygame.font.SysFont(font, size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.x = position[0]
    text_rect.y = position[1]
    screen.blit(text, text_rect)
    return text_rect


def display_text_centered(screen, text, size, color, position, font=False):
    if font is False:
        font = 'system'
    font = pygame.font.SysFont(font, size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.center = position
    screen.blit(text, text_rect)
    return text_rect


def display_rectangle(screen, color, position, dimension):
    rectangle = pygame.Surface(dimension)
    rectangle_rect = rectangle.get_rect()
    rectangle_rect.center = position
    rectangle.fill(color)
    screen.blit(rectangle, rectangle_rect)


def back_button(screen, color, mouse_x, mouse_y, clicked_l, destination):
    position = display_text(screen,
                            text="Back",
                            size=50,
                            color=color,
                            position=(25, 15))
    if ((mouse_x >= position[0]-10 and mouse_x <= position[0]+position[2]+10)
            and (mouse_y >= position[1]-10 and mouse_y <= position[1]+position[3]+10)
            and clicked_l):
        destination()


def main_menu_button(screen, color, mouse_x, mouse_y, clicked_l, destination):
    position = display_text(screen,
                            text="Main Menu",
                            size=50,
                            color=color,
                            position=(900, 15))
    if ((mouse_x >= position[0]-10 and mouse_x <= position[0]+position[2]+10)
            and (mouse_y >= position[1]-10 and mouse_y <= position[1]+position[3]+10)
            and clicked_l):
        destination()


def check_mouse_l_click(event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        return True
    else:
        return False


def check_mouse_r_click(event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
        return True
    else:
        return False
