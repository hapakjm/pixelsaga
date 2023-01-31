import pygame
from pygame import mixer
import sys
import random
import resources as res
import main

pygame.init()
pygame.display.set_icon(res.G2GICON)

BG = res.import_barney_bg_img((res.SCREEN_WIDTH, res.SCREEN_HEIGHT))
BARNEY_START = res.import_start_barney_img()
BARNEY_RUN = res.import_running_barney_gif()
BARNEY_DUCK = res.import_ducking_barney_gif()
BARNEY_JUMP = res.import_jumping_barney_img()
BARNEY_DEAD = res.import_dead_barney_img()
PACMAN = res.import_pacman_gif()
SHURIKEN = res.import_shuriken_gif()
BARNEY_HIGH_SCORE_DIR = "Barney\\Others\\barneyHighScore.txt"

with open(res.resource_path(BARNEY_HIGH_SCORE_DIR), 'r') as file:
    high_score = file.readline()
    high_score = high_score[:-1]
    high_score = int(high_score)
    high_score_name = file.readline()


class menu:
    def display_texts(self, menu_screen):
        res.display_text_centered(screen=menu_screen,
                                  text=f"High Score: {high_score} ({high_score_name})",
                                  size=100,
                                  color=res.BLACK,
                                  position=(res.SCREEN_WIDTH//2, res.SCREEN_HEIGHT//3))
        res.display_text_centered(screen=menu_screen,
                                  text=f"Press any key to START",
                                  size=75,
                                  color=res.BLACK,
                                  position=(res.SCREEN_WIDTH//2, res.SCREEN_HEIGHT//2))

    def display_buttons(self, screen, clicked_l, mouse_x, mouse_y):
        res.back_button(screen,
                        color=res.BLACK,
                        mouse_x=mouse_x, mouse_y=mouse_y,
                        clicked_l=clicked_l,
                        destination=main.main)

    def main(self):
        SCREEN = pygame.display.set_mode((res.SCREEN_WIDTH, res.SCREEN_HEIGHT))
        pygame.display.set_icon(res.G2GICON)
        run = True
        clock = pygame.time.Clock()

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    game().main()
                clicked_l = res.check_mouse_l_click(event)
            mouse_x, mouse_y = pygame.mouse.get_pos()

            SCREEN.fill(res.WHITE)
            SCREEN.blit(BG, (0, 0))
            SCREEN.blit(BARNEY_START, (50, 445))
            self.display_texts(SCREEN)
            self.display_buttons(SCREEN, clicked_l, mouse_x, mouse_y)

            clock.tick(60)
            pygame.display.update()


class game:
    def __init__(self):
        pygame.mixer.init()

    def moving_background(self, screen, status, game_speed):
        global background_x_pos
        if status == "RESUME":
            background_x_pos -= 10 * (game_speed)
            if background_x_pos <= -res.SCREEN_WIDTH:
                background_x_pos = 0
            screen.blit(BG, (background_x_pos, 0))
            screen.blit(BG, (res.SCREEN_WIDTH+background_x_pos, 0))
            return background_x_pos
        elif status == "PAUSE":
            screen.blit(BG, (background_x_pos, 0))
            screen.blit(BG, (res.SCREEN_WIDTH+background_x_pos, 0))

    def running_barney(self, screen):
        global counter, barney_dimension
        index = counter // 5
        if status == "RESUME":
            counter += 1
            if counter >= 10:
                counter = 0
            screen.blit(BARNEY_RUN[index], (barney_x_pos, 445))
        elif status == "PAUSE":
            screen.blit(BARNEY_RUN[index], (barney_x_pos, 445))
        barney_dimension = (barney_x_pos, 445, 85, 95)
        # pygame.draw.rect(screen, res.RED, (barney_x_pos, 445, 85, 95), 2)

    def ducking_barney(self, screen):
        global is_barney_duck, is_barney_run, counter, barney_dimension
        index = counter // 5
        if status == "RESUME":
            counter += 1
            if counter >= 10:
                counter = 0
            is_barney_duck = False
            is_barney_run = True
            screen.blit(BARNEY_DUCK[index], (barney_x_pos, 480))
        elif status == "PAUSE":
            screen.blit(BARNEY_DUCK[index], (barney_x_pos, 480))
        barney_dimension = (barney_x_pos, 480, 115, 60)
        # pygame.draw.rect(screen, res.RED, (barney_x_pos, 480, 115, 60), 2)

    def jumping_barney(self, screen):
        global is_barney_jump, ascending, is_barney_run, jump_counter, barney_dimension
        if status == "RESUME":
            if ascending:
                jump_counter += 1
                if jump_counter >= 20:
                    ascending = False
            elif ascending is False:
                jump_counter -= 1
                if jump_counter <= 0:
                    is_barney_jump = False
                    is_barney_run = True
            screen.blit(BARNEY_JUMP, (barney_x_pos, 445-(jump_counter*10)))
        elif status == "PAUSE":
            screen.blit(BARNEY_JUMP, (barney_x_pos, 445-(jump_counter*10)))
        barney_dimension = (barney_x_pos+10, 445-(jump_counter*10), 55, 95)
        # pygame.draw.rect(screen, res.RED, (barney_x_pos+10, 445 - (jump_counter * 10), 55, 95), 2)

    def escape_key(self, event):
        global key_pressed
        if event.type == pygame.KEYDOWN and event.key == 27:
            key_pressed = True
            return True

    def jump_key(self, key_input):
        global key_pressed, play_sound, play_sound_counter
        if ((key_input[pygame.K_UP]
             or key_input[pygame.K_SPACE]
             or key_input[pygame.K_w])
                and is_barney_jump is False
                and is_barney_duck is False):
            key_pressed = True
            if play_sound_counter == 0:
                play_sound = True
            return True

    def duck_key(self, key_input):
        global key_pressed, play_sound, play_sound_counter
        if ((key_input[pygame.K_DOWN]
             or key_input[pygame.K_s])
                and is_barney_jump is False):
            key_pressed = True
            if play_sound_counter == 0:
                play_sound = True
            return True

    def forward_key(self, key_input):
        if key_input[pygame.K_RIGHT] or key_input[pygame.K_d]:
            return True

    def backward_key(self, key_input):
        if key_input[pygame.K_LEFT] or key_input[pygame.K_a]:
            return True

    def manipulate_barney(self, key_input, screen, jump, duck):
        global is_barney_jump, ascending, play_sound
        global is_barney_run, is_barney_duck, barney_x_pos
        if status == "RESUME" and self.jump_key(key_input):
            is_barney_jump = True
            ascending = True
            is_barney_run = False
            if play_sound:
                jump.play()
                play_sound = False
        if status == "RESUME" and self.duck_key(key_input):
            is_barney_duck = True
            is_barney_run = False
            if play_sound:
                duck.play()
                play_sound = False
        if status == "RESUME" and self.forward_key(key_input) and barney_x_pos < 750:
            barney_x_pos += 10
        elif status == "RESUME" and self.backward_key(key_input) and barney_x_pos > 50:
            barney_x_pos -= 10

        if is_barney_jump:
            self.jumping_barney(screen)
        elif is_barney_duck:
            self.ducking_barney(screen)
        elif is_barney_run:
            self.running_barney(screen)

    def pacman_obstacle(self, screen):
        global obstacle_counter, obstacle_x_pos, spawn_obstacle, game_speed, obstacle_dimension
        index = obstacle_counter // 5
        if status == "RESUME":
            obstacle_counter += 1
            if obstacle_counter >= 15:
                obstacle_counter = 0
            obstacle_x_pos -= 10 * game_speed
            if obstacle_x_pos <= -150:
                obstacle_x_pos = res.SCREEN_WIDTH
                spawn_obstacle = True
                obstacle_counter = 0
                game_speed += 0.05
            screen.blit(PACMAN[index], (obstacle_x_pos, 430))
        elif status == "PAUSE":
            screen.blit(PACMAN[index], (obstacle_x_pos, 430))
        obstacle_dimension = (obstacle_x_pos+25, 440, 75, 90)
        # pygame.draw.rect(screen, res.RED, (obstacle_x_pos+25, 440, 75, 90), 2)

    def shuriken_obstacle(self, screen):
        global obstacle_counter, obstacle_x_pos, spawn_obstacle, game_speed, obstacle_dimension
        index = obstacle_counter // 5
        if status == "RESUME":
            obstacle_counter += 1
            if obstacle_counter >= 10:
                obstacle_counter = 0
            obstacle_x_pos -= 10 * game_speed
            if obstacle_x_pos <= -150:
                obstacle_x_pos = res.SCREEN_WIDTH
                spawn_obstacle = True
                obstacle_counter = 0
                game_speed += 0.05
            screen.blit(SHURIKEN[index], (obstacle_x_pos, 400))
        elif status == "PAUSE":
            screen.blit(SHURIKEN[index], (obstacle_x_pos, 400))
        obstacle_dimension = (obstacle_x_pos+15, 425, 75, 50)
        # pygame.draw.rect(screen, res.RED, (obstacle_x_pos+15, 425, 75, 50), 2)

    def display_spawn_obstacle(self, screen):
        global spawn_obstacle, what_obstacle
        if spawn_obstacle:
            what_obstacle = random.randint(0, 1)
            spawn_obstacle = False
        if what_obstacle == 0:
            self.pacman_obstacle(screen)
        elif what_obstacle == 1:
            self.shuriken_obstacle(screen)

    def check_barney_collide_top(self, barney_dimension, obstacle_dimension):
        if (barney_dimension[1] <= obstacle_dimension[1]+obstacle_dimension[3]
                and barney_dimension[1] >= obstacle_dimension[1]):
            return True

    def check_barney_collide_bottom(self, barney_dimension, obstacle_dimension):
        if (barney_dimension[1]+barney_dimension[3] >= obstacle_dimension[1]
                and barney_dimension[1]+barney_dimension[3] <= obstacle_dimension[1]+obstacle_dimension[3]):
            return True

    def check_barney_collide_right(self, barney_dimension, obstacle_dimension):
        if (barney_dimension[0]+barney_dimension[2] >= obstacle_dimension[0]
                and barney_dimension[0]+barney_dimension[2] <= obstacle_dimension[0]+obstacle_dimension[2]):
            return True

    def check_barney_collide_left(self, barney_dimension, obstacle_dimension):
        if (barney_dimension[0] >= obstacle_dimension[0]
                and barney_dimension[0] <= obstacle_dimension[0]+obstacle_dimension[2]):
            return True

    def check_collision(self, barney_dimension, obstacle_dimension):
        if (self.check_barney_collide_right(barney_dimension, obstacle_dimension)
            and (self.check_barney_collide_top(barney_dimension, obstacle_dimension)
                 or self.check_barney_collide_bottom(barney_dimension, obstacle_dimension))):
            return True
        if (self.check_barney_collide_left(barney_dimension, obstacle_dimension)
            and (self.check_barney_collide_top(barney_dimension, obstacle_dimension)
                 or self.check_barney_collide_bottom(barney_dimension, obstacle_dimension))):
            return True
        if (self.check_barney_collide_top(barney_dimension, obstacle_dimension)
            and (self.check_barney_collide_right(barney_dimension, obstacle_dimension)
                 or self.check_barney_collide_left(barney_dimension, obstacle_dimension))):
            return True
        if (self.check_barney_collide_bottom(barney_dimension, obstacle_dimension)
            and (self.check_barney_collide_right(barney_dimension, obstacle_dimension)
                 or self.check_barney_collide_left(barney_dimension, obstacle_dimension))):
            return True

    def collision_event(self, screen, score, barney_dimension, obstacle_dimension):
        global is_barney_run, is_barney_jump, is_barney_duck
        if self.check_collision(barney_dimension, obstacle_dimension):
            is_barney_run = False
            is_barney_jump = False
            is_barney_duck = False
            screen.blit(
                BARNEY_DEAD, (barney_dimension[0], barney_dimension[1]))
            res.display_text_centered(screen,
                                      text="You Died!",
                                      size=100,
                                      color=res.RED,
                                      position=(res.SCREEN_WIDTH//2, (res.SCREEN_HEIGHT//2)-100))
            res.display_text_centered(screen,
                                      text=f"{score}",
                                      size=150,
                                      color=res.BLACK,
                                      position=(res.SCREEN_WIDTH//2, res.SCREEN_HEIGHT//2))
            pygame.mixer.music.load(res.resource_path(
                "Barney\\Others\\Nooooooo.wav"))
            pygame.mixer.music.play()
            pygame.display.update()
            pygame.time.delay(1500)
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.check_high_score(score)
        else:
            res.display_text_centered(screen,
                                      text=f"SCORE: {score}",
                                      size=50,
                                      color=res.BLACK,
                                      position=(res.SCREEN_WIDTH//2, 50))

    def check_high_score(self, score):
        global high_score, high_score_name
        if score > high_score:
            high_score = score
            high_score_name = ""
            high_score_screen().main()
        else:
            menu().main()

    def pause_button(self, screen, color, mouse_x, mouse_y, clicked_l, escape_key_pressed):
        global status
        if status == "RESUME":
            temp_text = "Pause"
        elif status == "PAUSE":
            temp_text = "Resume"
        position = res.display_text(screen,
                                    text=temp_text,
                                    size=50,
                                    color=color,
                                    position=(950, 15))
        if (((mouse_x >= position[0]-10 and mouse_x <= position[0]+position[2]+10)
                and (mouse_y >= position[1]-10 and mouse_y <= position[1]+position[3]+10)
                and clicked_l)
                or escape_key_pressed):
            if status == "RESUME":
                pygame.mixer.music.pause()
                status = "PAUSE"
            elif status == "PAUSE":
                pygame.mixer.music.unpause()
                status = "RESUME"

    def display_buttons(self, screen, mouse_x, mouse_y, clicked_l, escape_key_pressed):
        res.back_button(screen,
                        color=res.BLACK,
                        mouse_x=mouse_x, mouse_y=mouse_y,
                        clicked_l=clicked_l,
                        destination=self.back_button_event)
        self.pause_button(screen,
                          color=res.RED,
                          mouse_x=mouse_x, mouse_y=mouse_y,
                          clicked_l=clicked_l,
                          escape_key_pressed=escape_key_pressed)
        self.pause_display(screen)

    def back_button_event(self):
        global MUSIC
        MUSIC.stop()
        MUSIC.unload()
        res.BG_MUSIC.load(res.resource_path("Theme.wav"))
        res.BG_MUSIC.play(-1)
        menu().main()

    def pause_display(self, screen):
        global score
        if status == "PAUSE":
            res.display_text_centered(screen,
                                      text="GAME PAUSED",
                                      size=100,
                                      color=res.RED,
                                      position=(res.SCREEN_WIDTH//2, res.SCREEN_HEIGHT//2))
        elif status == "RESUME":
            score += 1

    def main(self):
        global background_x_pos, counter
        global is_barney_run, is_barney_duck, is_barney_jump
        global barney_x_pos, ascending, jump_counter
        global obstacle_counter, obstacle_x_pos, spawn_obstacle, what_obstacle
        global barney_dimension, obstacle_dimension
        global score, game_speed, status, key_pressed, play_sound, play_sound_counter
        global MUSIC
        pygame.display.set_icon(res.G2GICON)
        SCREEN = pygame.display.set_mode((res.SCREEN_WIDTH, res.SCREEN_HEIGHT))
        res.BG_MUSIC.stop()
        MUSIC = pygame.mixer.music
        MUSIC.load(res.resource_path("Barney\\Others\\Music.wav"))
        MUSIC.play(-1)
        JUMP = pygame.mixer.Sound(
            res.resource_path("Barney\\Others\\Jump.wav"))
        DUCK = pygame.mixer.Sound(
            res.resource_path("Barney\\Others\\Duck.wav"))
        run = True
        clock = pygame.time.Clock()
        background_x_pos = 0
        counter = 0
        is_barney_run = True
        is_barney_duck = False
        is_barney_jump = False
        ascending = False
        jump_counter = 0
        barney_x_pos = 50
        obstacle_counter = 0
        obstacle_x_pos = res.SCREEN_WIDTH
        spawn_obstacle = True
        what_obstacle = 0
        score = 0
        game_speed = 1
        status = "RESUME"
        key_pressed = False
        play_sound = False
        play_sound_counter = 0

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                clicked_l = res.check_mouse_l_click(event)
                escape_key_pressed = self.escape_key(event)
            key_input = pygame.key.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()

            SCREEN.fill(res.WHITE)
            self.moving_background(SCREEN, status, game_speed)
            self.manipulate_barney(key_input, SCREEN, JUMP, DUCK)
            self.display_spawn_obstacle(SCREEN)
            self.collision_event(SCREEN,
                                 score, barney_dimension, obstacle_dimension)
            self.display_buttons(SCREEN, mouse_x, mouse_y,
                                 clicked_l, escape_key_pressed)

            clicked_l = False
            key_input = False
            escape_key_pressed = False
            if key_pressed:
                play_sound_counter += 1
                if play_sound_counter >= 50:
                    play_sound_counter = 0
                    key_pressed = False

            clock.tick(60)
            pygame.display.update()


class high_score_screen:
    def display_new_high_score_text(self, screen):
        global new_high_score_text_y_pos
        if new_high_score_text_y_pos > 125:
            new_high_score_text_y_pos -= 5
        res.display_text_centered(screen,
                                  text="NEW HIGH SCORE!",
                                  size=150,
                                  color=res.BLACK,
                                  position=(res.SCREEN_WIDTH//2, new_high_score_text_y_pos))

    def display_high_score(self, screen):
        global alpha
        font = pygame.font.SysFont("system", 250)
        text = font.render(str(high_score), True, res.BLACK)
        text_rect = text.get_rect()
        text_rect.center = (res.SCREEN_WIDTH//4, 325)
        if alpha < 255:
            if alpha < 50:
                alpha += 1
            else:
                alpha += 10
        text.set_alpha(alpha)
        screen.blit(text, text_rect)

    def display_name_input(self, screen):
        global cursor_timer
        res.display_text_centered(screen,
                                  text="Input Your Name:",
                                  size=50,
                                  color=res.BLACK,
                                  position=(750, 250))
        res.display_rectangle(screen,
                              color=res.GRAY,
                              position=(750, 325),
                              dimension=(500, 75))
        pygame.draw.rect(screen, res.BLACK, (500, 288, 500, 75), 2)
        name_rect = res.display_text(screen,
                                     text=high_score_name,
                                     size=75,
                                     color=res.BLACK,
                                     position=(515, 300))
        cursor_timer += 1
        if cursor_timer > 50:
            cursor_timer = 0
        if cursor_timer // 35 == 1:
            x_pos = name_rect[0]+name_rect[2]
            pygame.draw.rect(screen, res.BLACK, (x_pos, 295, 3, 63), 3)

    def input_high_score_name(self, event):
        global high_score_name
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                high_score_name = high_score_name[:-1]
            elif (len(high_score_name) < 10
                    and event.key != 9
                    and event.key != 13
                    and event.key != 27):
                high_score_name += event.unicode

    def submit_button(self, screen, high_score, high_score_name, clicked_l, mouse_x, mouse_y):
        if clicked_l and (mouse_x >= 700 and mouse_x <= 800) and (mouse_y >= 375 and mouse_y <= 425):
            res.display_rectangle(screen,
                                  color=res.MAGENTA,
                                  position=(750, 400),
                                  dimension=(100, 50))
            if high_score_name != "":
                with open(res.resource_path(res.resource_path(BARNEY_HIGH_SCORE_DIR)), 'w') as file:
                    file.write(f"{high_score}\n")
                    file.write(f"{high_score_name}")
                menu().main()
        else:
            res.display_rectangle(screen,
                                  color=res.GRAY,
                                  position=(750, 400),
                                  dimension=(100, 50))
        pygame.draw.rect(screen, res.BLACK, (700, 375, 100, 50), 2)
        res.display_text_centered(screen,
                                  text="Submit",
                                  size=25,
                                  color=res.BLACK,
                                  position=(750, 400))

    def submit_and_share_button(self, screen, high_score, high_score_name, clicked_l, mouse_x, mouse_y):
        if clicked_l and (mouse_x >= 670 and mouse_x <= 830) and (mouse_y >= 435 and mouse_y <= 485):
            res.display_rectangle(screen,
                                  color=res.MAGENTA,
                                  position=(750, 460),
                                  dimension=(160, 50))
            if high_score_name != "":
                with open(BARNEY_HIGH_SCORE_DIR, 'w') as file:
                    file.write(f"{high_score}\n")
                    file.write(f"{high_score_name}")
                menu().main()
        else:
            res.display_rectangle(screen,
                                  color=res.GRAY,
                                  position=(750, 460),
                                  dimension=(160, 50))
        pygame.draw.rect(screen, res.BLACK, (670, 435, 160, 50), 2)
        res.display_text_centered(screen,
                                  text="Submit and Share",
                                  size=25,
                                  color=res.BLACK,
                                  position=(750, 460))

    def display_after_text_ascend(self, screen, ascend_text, clicked_l, mouse_x, mouse_y):
        if ascend_text:
            self.display_high_score(screen)
            if alpha >= 250:
                self.display_name_input(screen)
                self.submit_button(screen, high_score,
                                   high_score_name, clicked_l, mouse_x, mouse_y)
                # self.submit_and_share_button(SCREEN, high_score, high_score_name, clicked_l, mouse_x, mouse_y)

    def check_ascend(self):
        global ascend_text
        if ascend_text is False:
            pygame.time.delay(500)
            ascend_text = True

    def main(self):
        global new_high_score_text_y_pos, alpha, cursor_timer, ascend_text
        pygame.display.set_icon(res.G2GICON)
        SCREEN = pygame.display.set_mode((res.SCREEN_WIDTH, res.SCREEN_HEIGHT))
        run = True
        clock = pygame.time.Clock()
        new_high_score_text_y_pos = res.SCREEN_HEIGHT//2
        alpha = 0
        cursor_timer = 0
        ascend_text = False

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.input_high_score_name(event)
                clicked_l = res.check_mouse_l_click(event)
            mouse_x, mouse_y = pygame.mouse.get_pos()

            SCREEN.fill(res.WHITE)
            SCREEN.blit(BG, (0, 0))
            self.display_new_high_score_text(SCREEN)
            self.display_after_text_ascend(SCREEN,
                                           ascend_text, clicked_l, mouse_x, mouse_y)

            clock.tick(60)
            pygame.display.update()
            self.check_ascend()


if __name__ == '__main__':
    menu().main()
