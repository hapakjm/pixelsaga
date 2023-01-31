from re import S
import pygame
import sys
import random
import os
import resources as res
import main

pygame.init()
pygame.display.set_icon(res.G2GICON)

COMING_SOON = res.import_coming_soon_img((1100, 600))
CHECK = res.import_check_img((50, 50))
SNAKE_HiGH_SCORE_DIR = "Snake\\snakeHighScore.txt"

with open(res.resource_path(SNAKE_HiGH_SCORE_DIR), 'r') as file:
    high_score = file.readline()
    high_score = high_score[:-1]
    high_score = int(high_score)
    high_score_name = file.readline()

activate_wall = True
game_speed = 10
game_speed_str = str(game_speed)


class menu:
    def display_texts(self, screen):
        res.display_text_centered(screen,
                                  text="Snake",
                                  size=200,
                                  color=res.BLUE,
                                  position=(res.SCREEN_WIDTH//2, 125))
        res.display_text_centered(screen,
                                  text="High Score:",
                                  size=75,
                                  color=res.WHITE,
                                  position=(res.SCREEN_WIDTH//4*3, 250))
        res.display_text_centered(screen,
                                  text=high_score_name + " " + str(high_score),
                                  size=100,
                                  color=res.YELLOW,
                                  position=(res.SCREEN_WIDTH//4*3, 350))

    def display_lines(self, screen):
        pygame.draw.line(screen, res.GRAY, (res.SCREEN_WIDTH //
                         2, 200), (res.SCREEN_WIDTH//2, 550), 5)

    def display_buttons(self, screen, mouse_x, mouse_y, clicked_l):
        res.back_button(screen,
                        color=res.WHITE,
                        mouse_x=mouse_x, mouse_y=mouse_y,
                        clicked_l=clicked_l,
                        destination=main.main)
        self.display_wall_selection(screen, mouse_x, mouse_y, clicked_l)
        self.display_speed_selection(screen, mouse_x, mouse_y, clicked_l)
        self.start_button(screen, mouse_x, mouse_y, clicked_l)

    def start_button(self, screen, mouse_x, mouse_y, clicked_l):
        global stop_click
        position = res.display_text(screen,
                                    text="START",
                                    size=100,
                                    color=res.GREEN,
                                    position=(res.SCREEN_WIDTH//2-110, res.SCREEN_HEIGHT//3*2+50))
        rectangle = pygame.Surface((position[2]+10, position[3]+10))
        rectangle_rect = rectangle.get_rect()
        rectangle_rect.x = position[0]-5
        rectangle_rect.y = position[1]-5
        rectangle.fill(res.WHITE)
        screen.blit(rectangle, rectangle_rect)
        res.display_text(screen,
                         text="START",
                         size=100,
                         color=res.GREEN,
                         position=(position[0], position[1]+3))
        pygame.draw.rect(
            screen, res.GREEN, (position[0]-5, position[1]-5, position[2]+10, position[3]+10), 2)
        if ((mouse_x >= position[0]-10 and mouse_x <= position[0]+position[2]+10)
                and (mouse_y >= position[1]-10 and mouse_y <= position[1]+position[3]+10)
                and clicked_l and stop_click is False):
            stop_click = True
            game().main()

    def display_wall_selection(self, screen, mouse_x, mouse_y, clicked_l):
        global activate_wall, stop_click
        res.display_text(screen,
                         text="Activate Wall:",
                         size=50,
                         color=res.WHITE,
                         position=(125, 225))
        rectangle = pygame.Surface((50, 50))
        rectangle_rect = rectangle.get_rect()
        rectangle_rect.x = 375
        rectangle_rect.y = 215
        rectangle.fill(res.WHITE)
        screen.blit(rectangle, rectangle_rect)
        pygame.draw.rect(screen, res.YELLOW, (375, 215, 50, 50), 2)
        if ((mouse_x >= 375-10 and mouse_x <= 375+50+10)
                and (mouse_y >= 215-10 and mouse_y <= 215+50+10)
                and clicked_l and stop_click is False):
            stop_click = True
            if activate_wall:
                activate_wall = False
            elif activate_wall is False:
                activate_wall = True
        if activate_wall:
            res.display_image(screen, CHECK, (375, 215))

    def display_speed_selection(self, screen, mouse_x, mouse_y, clicked_l):
        global stop_click, display_cursor, cursor_counter
        res.display_text(screen,
                         text="Game Speed:",
                         size=50,
                         color=res.WHITE,
                         position=(125, 325))
        rectangle = pygame.Surface((50, 50))
        rectangle_rect = rectangle.get_rect()
        rectangle_rect.x = 375
        rectangle_rect.y = 315
        rectangle.fill(res.WHITE)
        screen.blit(rectangle, rectangle_rect)
        pygame.draw.rect(screen, res.YELLOW, (375, 315, 50, 50), 2)
        position = res.display_text(screen,
                                    text=game_speed_str,
                                    size=50,
                                    color=res.BLACK,
                                    position=(380, 325))
        if ((mouse_x >= 375-10 and mouse_x <= 375+50+10)
                and (mouse_y >= 315-10 and mouse_y <= 315+50+10)
                and clicked_l and stop_click is False):
            stop_click = True
            display_cursor = True
        cursor_counter += 1
        if cursor_counter > 50:
            cursor_counter = 0
        if display_cursor and cursor_counter//25 == 0:
            pygame.draw.line(screen,
                             res.BLACK, (position[0]+position[2], position[1]-5), (position[0]+position[2], position[1]+35), 2)

    def key_inputs(self, event):
        global game_speed, game_speed_str
        if display_cursor:
            if event.key == pygame.K_BACKSPACE:
                if len(game_speed_str) == 2:
                    game_speed_str = game_speed_str[:-1]
                elif len(game_speed_str) == 1:
                    game_speed_str = ""
            elif (len(game_speed_str) <= 1
                    and event.key >= 48
                    and event.key <= 57):
                game_speed_str += event.unicode
        if game_speed_str != "":
            game_speed = int(game_speed_str)
            if game_speed > 10:
                game_speed_str = game_speed_str[:-1]

    def main(self):
        global stop_click, display_cursor, cursor_counter
        pygame.display.set_icon(res.G2GICON)
        SCREEN = pygame.display.set_mode((res.SCREEN_WIDTH, res.SCREEN_HEIGHT))
        run = True
        clock = pygame.time.Clock()
        click_counter = 0
        stop_click = True
        display_cursor = False
        cursor_counter = 0

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.key_inputs(event)
                clicked_l = res.check_mouse_l_click(event)
            mouse_x, mouse_y = pygame.mouse.get_pos()

            SCREEN.fill(res.BLACK)
            self.display_texts(SCREEN)
            self.display_lines(SCREEN)

            self.display_buttons(SCREEN, mouse_x, mouse_y, clicked_l)

            if stop_click:
                click_counter += 1
            if click_counter >= 25:
                click_counter = 0
                stop_click = False

            clock.tick(60)
            pygame.display.update()


class game:
    def display_images(self, screen):
        res.display_image(screen, images=COMING_SOON, rect=(0, 0))

    def display_text(self, screen, score, start):
        res.display_text_centered(screen,
                                  text=f"Score: {score}",
                                  size=75,
                                  color=res.BLUE,
                                  position=(res.SCREEN_WIDTH//2, 25))
        if start:
            res.display_text_centered(screen,
                                      text="Press move key to start.",
                                      size=100,
                                      color=res.GREEN,
                                      position=(res.SCREEN_WIDTH//2, 300))
        elif status == "PAUSE":
            res.display_text_centered(screen,
                                      text="GAME PAUSED",
                                      size=100,
                                      color=res.WHITE,
                                      position=(res.SCREEN_WIDTH//2, res.SCREEN_HEIGHT//2-100))
        elif has_died:
            res.display_text_centered(screen,
                                      text=f"YOUR SCORE: {score}",
                                      size=150,
                                      color=res.WHITE,
                                      position=(res.SCREEN_WIDTH//2, res.SCREEN_HEIGHT//2+50))
            res.display_text_centered(screen,
                                      text="YOU DIED",
                                      size=100,
                                      color=res.WHITE,
                                      position=(res.SCREEN_WIDTH//2, res.SCREEN_HEIGHT//2-100))

    def walls(self, screen):
        res.display_rectangle(screen,
                              color=res.BLACK,
                              position=(res.SCREEN_WIDTH//2-2.5,
                                        res.SCREEN_HEIGHT//2+10),
                              dimension=(1035, 510))
        if activate_wall:
            pygame.draw.rect(
                screen, res.RED, (25, 50, res.SCREEN_WIDTH-55, res.SCREEN_HEIGHT-80), 5)

    def square(self, screen, x_pos, y_pos, color):
        rectangle = pygame.Surface((15, 15))
        rectangle_rect = rectangle.get_rect()
        rectangle_rect.x = x_pos
        rectangle_rect.y = y_pos
        rectangle.fill(color)
        screen.blit(rectangle, rectangle_rect)

    def snake_at_random_pos(self):
        global random_position, snake_direction, x_pos_initial, y_pos_initial
        if random_position:
            x_pos_initial = random.choice(range(180, 915, 15))
            y_pos_initial = random.choice(range(205, 415, 15))
            self.snake_initial_position()
            random_position = False

    def snake_initial_position(self):
        global x_pos, y_pos, snake_direction
        x_pos.clear()
        y_pos.clear()
        snake_direction = random.choice(["UP", "DOWN", "RIGHT", "LEFT"])
        if snake_direction == "UP":
            for lenght in range(0, snake_lenght):
                x_pos.append(x_pos_initial)
                y_pos.append(y_pos_initial+(15*lenght))
        elif snake_direction == "DOWN":
            for lenght in range(0, snake_lenght):
                x_pos.append(x_pos_initial)
                y_pos.append(y_pos_initial-(15*lenght))
        elif snake_direction == "RIGHT":
            for lenght in range(0, snake_lenght):
                x_pos.append(x_pos_initial-(15*lenght))
                y_pos.append(y_pos_initial)
        elif snake_direction == "LEFT":
            for lenght in range(0, snake_lenght):
                x_pos.append(x_pos_initial+(15*lenght))
                y_pos.append(y_pos_initial)

    def escape_key(self, event):
        if event.type == pygame.KEYDOWN and event.key == 27:
            return True

    def up_key(self, key_input):
        if (key_input[pygame.K_UP] or key_input[pygame.K_w]):
            return True

    def down_key(self, key_input):
        if (key_input[pygame.K_DOWN] or key_input[pygame.K_s]):
            return True

    def right_key(self, key_input):
        if key_input[pygame.K_RIGHT] or key_input[pygame.K_d]:
            return True

    def left_key(self, key_input):
        if key_input[pygame.K_LEFT] or key_input[pygame.K_a]:
            return True

    def manipulate_snake(self, key_input):
        global start, key_pressed, snake_direction, previous_direction, can_change_direction
        if status == "RESUME" and not has_died:
            if (self.up_key(key_input)
                and snake_direction != "DOWN"
                    and snake_direction != "UP"
                    and can_change_direction):
                key_pressed = True
                previous_direction = snake_direction
                snake_direction = "UP"
                can_change_direction = False
                if start:
                    start = False
            elif (self.down_key(key_input)
                  and snake_direction != "UP"
                    and snake_direction != "DOWN"
                    and can_change_direction):
                key_pressed = True
                previous_direction = snake_direction
                snake_direction = "DOWN"
                can_change_direction = False
                if start:
                    start = False
            elif (self.right_key(key_input)
                  and snake_direction != "LEFT"
                    and snake_direction != "RIGHT"
                    and can_change_direction):
                key_pressed = True
                previous_direction = snake_direction
                snake_direction = "RIGHT"
                can_change_direction = False
                if start:
                    start = False
            elif (self.left_key(key_input)
                  and snake_direction != "RIGHT"
                    and snake_direction != "LEFT"
                    and can_change_direction):
                key_pressed = True
                previous_direction = snake_direction
                snake_direction = "LEFT"
                can_change_direction = False
                if start:
                    start = False

    def moving_snake(self, screen, snake_direction):
        global x_pos, y_pos, can_change_direction, speed
        if status == "RESUME" and not has_died and not start:
            speed += game_speed
            if speed >= 15 and snake_direction == "UP":
                self.moving_up()
                can_change_direction = True
                speed = 0
            elif speed >= 15 and snake_direction == "DOWN":
                self.moving_down()
                can_change_direction = True
                speed = 0
            elif speed >= 15 and snake_direction == "RIGHT":
                self.moving_right()
                can_change_direction = True
                speed = 0
            elif speed >= 15 and snake_direction == "LEFT":
                self.moving_left()
                can_change_direction = True
                speed = 0
        self.display_snake(screen)

    def moving_up(self):
        global x_pos, y_pos
        y_pos.insert(0, y_pos[0]-15)
        y_pos = y_pos[:-1]
        if y_pos[0] < 55:
            y_pos[0] = 550
        x_pos.insert(0, x_pos[0])
        x_pos = x_pos[:-1]

    def moving_down(self):
        global x_pos, y_pos
        y_pos.insert(0, y_pos[0]+15)
        y_pos = y_pos[:-1]
        if y_pos[0] > 550:
            y_pos[0] = 55
        x_pos.insert(0, x_pos[0])
        x_pos = x_pos[:-1]

    def moving_right(self):
        global x_pos, y_pos
        x_pos.insert(0, x_pos[0]+15)
        x_pos = x_pos[:-1]
        if x_pos[0] > 1050:
            x_pos[0] = 30
        y_pos.insert(0, y_pos[0])
        y_pos = y_pos[:-1]

    def moving_left(self):
        global x_pos, y_pos
        x_pos.insert(0, x_pos[0]-15)
        x_pos = x_pos[:-1]
        if x_pos[0] < 30:
            x_pos[0] = 1050
        y_pos.insert(0, y_pos[0])
        y_pos = y_pos[:-1]

    def display_snake(self, screen):
        for lenght in range(0, snake_lenght):
            if has_died:
                self.square(screen, x_pos[lenght], y_pos[lenght], res.RED)
            elif not has_died:
                if lenght == 0:
                    self.square(
                        screen, x_pos[lenght], y_pos[lenght], res.GREEN)
                elif lenght >= 1:
                    self.square(
                        screen, x_pos[lenght], y_pos[lenght], res.AQUA)

    def check_body_collision(self, x_pos, y_pos, direction):
        if direction == "UP":
            self.check_body_collision_vertical(x_pos, y_pos, 0, 15)
        elif direction == "DOWN":
            self.check_body_collision_vertical(x_pos, y_pos, 15, 0)
        elif direction == "RIGHT":
            self.check_body_collision_horizontal(x_pos, y_pos, 15, 0)
        elif direction == "LEFT":
            self.check_body_collision_horizontal(x_pos, y_pos, 0, 15)

    def check_body_collision_vertical(self, x_pos, y_pos, temp1, temp2):
        for lenght in range(1, len(y_pos)):
            if (y_pos[0] == y_pos[lenght]
                    and x_pos[0] == x_pos[lenght]):
                self.dead()
                break

    def check_body_collision_horizontal(self, x_pos, y_pos, temp1, temp2):
        for lenght in range(1, len(y_pos)):
            if (x_pos[0] == x_pos[lenght]
                    and y_pos[0] == y_pos[lenght]):
                self.dead()
                break

    def display_food(self, screen, x_pos, y_pos):
        global food_eaten
        if food_eaten:
            self.random_food_location(x_pos, y_pos)
            food_eaten = False
        self.square(screen, food_x_pos, food_y_pos, res.YELLOW)

    def random_food_location(self, x_pos, y_pos):
        global food_x_pos, food_y_pos
        snake_position = True
        while snake_position:
            food_x_pos = random.choice(range(180, 915, 15))
            food_y_pos = random.choice(range(205, 415, 15))
            index_counter = 0
            for length in range(0, len(x_pos)):
                index_counter += 1
                if food_x_pos == x_pos[length] and food_y_pos == y_pos[length]:
                    break
                if index_counter == len(x_pos):
                    snake_position = False

    def check_food_collision(self, x_pos, y_pos, food_x_pos, food_y_pos, direction, eat):
        if direction == "UP" or direction == "DOWN":
            self.check_food_collision_vertical(food_x_pos, food_y_pos, eat)
        elif direction == "RIGHT" or direction == "LEFT":
            self.check_food_collision_horizontal(food_x_pos, food_y_pos, eat)

    def check_food_collision_vertical(self, food_x_pos, food_y_pos, eat):
        global food_eaten, snake_lenght, score, x_pos, y_pos
        if (y_pos[0] == food_y_pos and x_pos[0] == food_x_pos):
            food_eaten = True
            snake_lenght += 1
            score += 1
            x_pos.append(x_pos[-1])
            y_pos.append(y_pos[-1])
            eat.play()

    def check_food_collision_horizontal(self, food_x_pos, food_y_pos, eat):
        global food_eaten, snake_lenght, score, x_pos, y_pos
        if (x_pos[0] == food_x_pos and y_pos[0] == food_y_pos):
            food_eaten = True
            snake_lenght += 1
            score += 1
            x_pos.append(x_pos[-1])
            y_pos.append(y_pos[-1])
            eat.play()

    def check_wall_collision(self, x_pos, y_pos, snake_direction):
        if activate_wall:
            if snake_direction == "UP":
                if y_pos[0] == 55:
                    self.dead()
            elif snake_direction == "DOWN":
                if y_pos[0] == 550:
                    self.dead()
            elif snake_direction == "RIGHT":
                if x_pos[0] == 1050:
                    self.dead()
            elif snake_direction == "LEFT":
                if x_pos[0] == 30:
                    self.dead()

    def dead(self):
        global has_died, status
        has_died = True
        pygame.mixer.music.load(res.resource_path(
            "Barney\\Others\\Nooooooo.wav"))
        pygame.mixer.music.play()

    def display_buttons(self, screen, clicked_l, mouse_x, mouse_y, escape_key_pressed, start):
        res.back_button(screen,
                        color=res.BLACK,
                        mouse_x=mouse_x, mouse_y=mouse_y,
                        clicked_l=clicked_l,
                        destination=self.back_button_event)
        if has_died is False:
            self.pause_button(screen,
                              color=res.BLACK,
                              mouse_x=mouse_x, mouse_y=mouse_y,
                              clicked_l=clicked_l,
                              escape_key_pressed=escape_key_pressed,
                              start=start)

    def back_button_event(self):
        global MUSIC
        MUSIC.stop()
        MUSIC.unload()
        res.BG_MUSIC.load(res.resource_path("Theme.wav"))
        res.BG_MUSIC.play(-1)
        menu().main()

    def pause_button(self, screen, color, mouse_x, mouse_y, clicked_l, escape_key_pressed, start):
        global status
        if status == "RESUME":
            text = "Pause"
        elif status == "PAUSE":
            text = "Resume"
        if not start:
            position = res.display_text(screen,
                                        text=text,
                                        size=50,
                                        color=color,
                                        position=(950, 15))
            if (((mouse_x >= 950 and mouse_x <= position[0]+position[2]+10)
                    and (mouse_y >= 15 and mouse_y <= position[1]+position[3]+10)
                    and clicked_l)
                    or escape_key_pressed):
                if status == "RESUME":
                    status = "PAUSE"
                elif status == "PAUSE":
                    status = "RESUME"

    def redirect_to(self, score):
        global high_score
        if has_died:
            if score > high_score:
                high_score = score
                pygame.time.delay(1500)
                high_score_screen().main()
            else:
                pygame.time.delay(1500)
                menu().main()

    def main(self):
        global start, random_position
        global snake_direction, can_change_direction, previous_direction
        global x_pos_initial, y_pos_initial, x_pos, y_pos, snake_lenght
        global key_pressed, has_died, food_x_pos, food_y_pos, food_eaten, score
        global speed, status, MUSIC
        pygame.display.set_icon(res.G2GICON)
        SCREEN = pygame.display.set_mode((res.SCREEN_WIDTH, res.SCREEN_HEIGHT))
        MUSIC = pygame.mixer.music
        MUSIC.load(res.resource_path("Snake\\Music.wav"))
        MUSIC.play(-1)
        EAT = pygame.mixer.Sound(res.resource_path("Snake\\Eat.wav"))
        run = True
        clock = pygame.time.Clock()
        start = True
        random_position = True
        snake_lenght = 10
        x_pos = [0]
        y_pos = [0]
        key_input = ""
        key_pressed = False
        snake_direction = ""
        can_change_direction = True
        previous_direction = ""
        has_died = False
        food_x_pos = 0
        food_y_pos = 0
        food_eaten = True
        score = 0
        speed = 0
        status = "RESUME"

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                clicked_l = res.check_mouse_l_click(event)
                escape_key_pressed = self.escape_key(event)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            key_input = pygame.key.get_pressed()

            SCREEN.fill(res.WHITE)
            # self.display_images(SCREEN)
            self.walls(SCREEN)
            self.snake_at_random_pos()
            self.manipulate_snake(key_input)
            self.moving_snake(SCREEN, snake_direction)
            self.check_body_collision(x_pos, y_pos, snake_direction)
            self.display_snake(SCREEN)
            self.display_food(SCREEN, x_pos, y_pos)
            self.check_food_collision(
                x_pos, y_pos, food_x_pos, food_y_pos, snake_direction, EAT)
            self.check_wall_collision(x_pos, y_pos, snake_direction)
            self.display_text(SCREEN, score, start)
            self.display_buttons(SCREEN,
                                 clicked_l, mouse_x, mouse_y, escape_key_pressed, start)

            clicked_l = False
            key_input = False
            escape_key_pressed = False
            key_pressed = False

            clock.tick(60)
            pygame.display.update()
            self.redirect_to(score)


class high_score_screen:

    def display_new_high_score_text(self, screen):
        global new_high_score_text_y_pos
        if new_high_score_text_y_pos > 125:
            new_high_score_text_y_pos -= 5
        res.display_text_centered(screen,
                                  text="NEW HIGH SCORE!",
                                  size=150,
                                  color=res.WHITE,
                                  position=(res.SCREEN_WIDTH//2, new_high_score_text_y_pos))

    def display_high_score(self, screen):
        global alpha
        font = pygame.font.SysFont("system", 250)
        text = font.render(str(high_score), True, res.WHITE)
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
                                  color=res.WHITE,
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
                with open(res.resource_path(res.resource_path(SNAKE_HiGH_SCORE_DIR)), 'w') as file:
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
                with open(SNAKE_HiGH_SCORE_DIR, 'w') as file:
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

            SCREEN.fill(res.BLACK)
            self.display_new_high_score_text(SCREEN)
            self.display_after_text_ascend(SCREEN,
                                           ascend_text, clicked_l, mouse_x, mouse_y)

            clock.tick(60)
            pygame.display.update()
            self.check_ascend()


if __name__ == "__main__":
    menu().main()
