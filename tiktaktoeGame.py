import pygame
import sys
import random
import resources as res
import main

pygame.init()
pygame.display.set_icon(res.G2GICON)

STARTGAME_G_GIF = res.import_start_green_gif((300, 150))
STARTGAME_Y_GIF = res.import_start_yellow_gif((300, 150))
X_MARK = res.import_x_mark_img((150, 150))
O_MARK = res.import_o_mark_img((150, 150))

x_name = "X"
o_name = "O"
vs_computer = False
difficulty = "EASY"
player_mark = "X"
computer_mark = "O"


class menu:
    def display_texts_menu(self, screen):
        res.display_text_centered(screen,
                                  text="Tik-Tak-Toe",
                                  size=200,
                                  color=res.GREEN,
                                  position=(res.SCREEN_WIDTH//2, 125))
        res.display_text_centered(screen,
                                  text="Player vs. Player",
                                  size=75,
                                  color=res.WHITE,
                                  position=(res.SCREEN_WIDTH//4, 275))
        res.display_text_centered(screen,
                                  text="Player vs. Comp.",
                                  size=75,
                                  color=res.WHITE,
                                  position=(res.SCREEN_WIDTH//4*3-25, 275))

    def display_buttons(self, screen, clicked_l, mouse_x, mouse_y):
        res.back_button(screen,
                        color=res.WHITE,
                        mouse_x=mouse_x, mouse_y=mouse_y,
                        clicked_l=clicked_l,
                        destination=main.main)
        self.pvp_button(screen, clicked_l, mouse_x, mouse_y)
        self.pve_button(screen, clicked_l, mouse_x, mouse_y)

    def pvp_button(self, screen, clicked_l, mouse_x, mouse_y):
        global startgame_image_timer, vs_computer
        startgame_image_timer = res.display_image(screen,
                                                  images=STARTGAME_G_GIF,
                                                  rect=(150, 300),
                                                  counter=startgame_image_timer,
                                                  speed=8)
        if ((mouse_x >= 175 and mouse_x <= 425) and (mouse_y >= 305 and mouse_y <= 390)
                and clicked_l):
            vs_computer = False
            pvp().main()

    def pve_button(self, screen, clicked_l, mouse_x, mouse_y):
        global vs_computer
        res.display_image(screen,
                          images=STARTGAME_Y_GIF,
                          rect=(650, 300),
                          counter=startgame_image_timer,
                          speed=8)
        if ((mouse_x >= 675 and mouse_x <= 925) and (mouse_y >= 305 and mouse_y <= 390)
                and clicked_l):
            vs_computer = True
            pve().main()

    def main(self):
        global startgame_image_timer
        pygame.display.set_icon(res.G2GICON)
        SCREEN = pygame.display.set_mode((res.SCREEN_WIDTH, res.SCREEN_HEIGHT))
        run = True
        clock = pygame.time.Clock()
        startgame_image_timer = 0

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                clicked_l = res.check_mouse_l_click(event)
            mouse_x, mouse_y = pygame.mouse.get_pos()

            SCREEN.fill(res.BLUE)
            self.display_texts_menu(SCREEN)
            self.display_buttons(SCREEN, clicked_l, mouse_x, mouse_y)

            clock.tick(60)
            pygame.display.update()


class pvp:
    def display_texts_pvp(self, screen):
        res.display_text(screen,
                         text="Input name:",
                         size=75,
                         color=res.WHITE,
                         position=(520, 95))
        res.display_text(screen,
                         text="Player X:",
                         size=75,
                         color=res.WHITE,
                         position=(200, 170))
        res.display_text(screen,
                         text="Player O:",
                         size=75,
                         color=res.WHITE,
                         position=(200, 295))
        res.display_text(screen,
                         text="Player X moves first!",
                         size=50,
                         color=res.WHITE,
                         position=(375, 375))

    def display_boxes_pvp(self, screen):
        res.display_rectangle(screen,
                              color=res.GRAY,
                              position=(700, 195),
                              dimension=(500, 75))
        res.display_rectangle(screen,
                              color=res.GRAY,
                              position=(700, 320),
                              dimension=(500, 75))

    def display_names_pvp(self, screen, clicked_l, mouse_x, mouse_y):
        global x_name, o_name, x_cursor, o_cursor, cursor_timer
        x_name_rect = res.display_text(screen,
                                       text=x_name,
                                       size=75,
                                       color=res.BLACK,
                                       position=(450, 170))
        o_name_rect = res.display_text(screen,
                                       text=o_name,
                                       size=75,
                                       color=res.BLACK,
                                       position=(450, 295))
        if clicked_l:
            if (mouse_x >= 450 and mouse_x <= 950) and (mouse_y >= 155 and mouse_y <= 235):
                x_cursor = True
                o_cursor = False
            elif (mouse_x >= 450 and mouse_x <= 950) and (mouse_y >= 280 and mouse_y <= 360):
                x_cursor = False
                o_cursor = True
        cursor_timer += 1
        if cursor_timer > 50:
            cursor_timer = 0
        self.display_text_cursor_pvp(screen,
                                     x_name_rect, o_name_rect, x_cursor, o_cursor, cursor_timer)

    def display_text_cursor_pvp(self, screen, x_name_rect, o_name_rect, x_cursor, o_cursor, cursor_timer):
        if x_cursor:
            x_pos = x_name_rect[0] + x_name_rect[2]
            if cursor_timer // 35 == 1:
                pygame.draw.rect(screen, res.BLACK,
                                 (x_pos, 170, 3, 50), 5)
        elif o_cursor:
            x_pos = o_name_rect[0] + o_name_rect[2]
            if cursor_timer // 35 == 1:
                pygame.draw.rect(screen, res.BLACK,
                                 (x_pos, 295, 3, 50), 5)

    def change_name_pvp(self, event, x_cursor, o_cursor):
        global x_name, o_name
        if x_cursor:
            x_name = self.key_inputs(event, x_name)
        elif o_cursor:
            o_name = self.key_inputs(event, o_name)

    def key_inputs(self, event, name):
        if event.key == pygame.K_BACKSPACE:
            name = name[:-1]
        elif (len(name) < 10
                and event.key != 9
                and event.key != 13
                and event.key != 27):
            name += event.unicode
        return name

    def start_game_button(self, screen, clicked_l, mouse_x, mouse_y):
        global startgame_timer
        startgame_timer = res.display_image(screen,
                                            images=STARTGAME_G_GIF,
                                            rect=((res.SCREEN_WIDTH//3)+35,
                                                  (res.SCREEN_HEIGHT//2)+100),
                                            counter=startgame_timer,
                                            speed=5)
        if ((mouse_x >= 425 and mouse_x <= 675) and (mouse_y >= 430 and mouse_y <= 515)
                and clicked_l):
            self.start_game_button_event()

    def start_game_button_event(self):
        game().main()

    def display_buttons(self, screen, clicked_l, mouse_x, mouse_y):
        res.main_menu_button(screen,
                             color=res.GRAY,
                             mouse_x=mouse_x, mouse_y=mouse_y,
                             clicked_l=clicked_l,
                             destination=main.main)
        res.back_button(screen,
                        color=res.GRAY,
                        mouse_x=mouse_x, mouse_y=mouse_y,
                        clicked_l=clicked_l,
                        destination=self.back_button_event)

    def back_button_event(self):
        global x_name, o_name
        x_name = "X"
        o_name = "O"
        menu().main()

    def main(self):
        global x_cursor, o_cursor, cursor_timer, startgame_timer
        pygame.display.set_icon(res.G2GICON)
        SCREEN = pygame.display.set_mode((res.SCREEN_WIDTH, res.SCREEN_HEIGHT))
        run = True
        clock = pygame.time.Clock()
        x_cursor = False
        o_cursor = False
        cursor_timer = 0
        startgame_timer = 0

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.change_name_pvp(event, x_cursor, o_cursor)
                clicked_l = res.check_mouse_l_click(event)
                '''self.click_events_pvp(clicked, mouse_x, mouse_y)'''
            mouse_x, mouse_y = pygame.mouse.get_pos()

            SCREEN.fill(res.BLUE)

            '''
            self.display_texts_pvp(SCREEN)
            self.display_boxes_pvp(SCREEN)
            startgame_timer = self.display_images_pvp(SCREEN, startgame_timer)
            x_name_text_rectangle, o_name_text_rectangle = self.display_names_pvp(
                SCREEN)
            cursor_timer = self.cursor_timer_pvp(cursor_timer)
            self.display_text_cursor_pvp(
                SCREEN, x_name_text_rectangle, o_name_text_rectangle, cursor_timer)
            '''

            self.display_texts_pvp(SCREEN)
            self.display_boxes_pvp(SCREEN)
            self.display_names_pvp(SCREEN, clicked_l, mouse_x, mouse_y)
            self.start_game_button(SCREEN, clicked_l, mouse_x, mouse_y)
            self.display_buttons(SCREEN, clicked_l, mouse_x, mouse_y)

            clock.tick(60)
            pygame.display.update()


class game:
    BOARD = [
        '', '', '',
        '', '', '',
        '', '', ''
    ]

    POSITION_COORDINATES = [
        (325, 95), (475, 95), (625, 95),
        (325, 245), (475, 245), (625, 245),
        (325, 395), (475, 395), (625, 395),
    ]

    def display_texts(self, screen, current_mark):
        res.display_text_centered(screen,
                                  text="Tik-Tak-Toe",
                                  size=100,
                                  color=res.GREEN,
                                  position=(res.SCREEN_WIDTH//2, 40))
        res.display_text_centered(screen,
                                  text="TURN",
                                  size=100,
                                  color=res.AQUA,
                                  position=(150, 200))
        res.display_text_centered(screen,
                                  text=current_mark,
                                  size=200,
                                  color=res.BLACK,
                                  position=(150, 350))
        '''
        res.display_text_centered(screen,
                                  text=x_name,
                                  size=100,
                                  color=res.WHITE,
                                  position=(950, 155))
        res.display_text_centered(screen,
                                  text=str(0),
                                  size=200,
                                  color=res.WHITE,
                                  position=(950, 250))
        res.display_text_centered(screen,
                                  text=o_name,
                                  size=100,
                                  color=res.WHITE,
                                  position=(950, 380))
        res.display_text_centered(screen,
                                  text=str(0),
                                  size=200,
                                  color=res.WHITE,
                                  position=(950, 475))
        '''

    def display_board(self, screen):
        board = pygame.Surface((500, 500))
        board_square = board.get_rect()
        board_square.center = (res.SCREEN_WIDTH // 2,
                               (res.SCREEN_HEIGHT // 2) + 20)
        board.fill(res.GRAY)
        screen.blit(board, board_square)
        pygame.draw.rect(screen, res.BLACK, board_square, 5)
        pygame.draw.rect(screen, res.BLACK, (475, 95, 5, 450), 5)
        pygame.draw.rect(screen, res.BLACK, (625, 95, 5, 450), 5)
        pygame.draw.rect(screen, res.BLACK, (325, 245, 450, 5), 5)
        pygame.draw.rect(screen, res.BLACK, (325, 395, 450, 5), 5)

    def check_mouse_position_top_row(self, mouse_x, mouse_y):
        if (mouse_x >= 325 and mouse_x <= 470) and (mouse_y >= 95 and mouse_y <= 245):
            return 0
        if (mouse_x >= 475 and mouse_x <= 615) and (mouse_y >= 95 and mouse_y <= 245):
            return 1
        if (mouse_x >= 625 and mouse_x <= 760) and (mouse_y >= 95 and mouse_y <= 245):
            return 2

    def check_mouse_position_mid_row(self, mouse_x, mouse_y):
        if (mouse_x >= 325 and mouse_x <= 470) and (mouse_y >= 245 and mouse_y <= 395):
            return 3
        if (mouse_x >= 475 and mouse_x <= 615) and (mouse_y >= 245 and mouse_y <= 395):
            return 4
        if (mouse_x >= 625 and mouse_x <= 760) and (mouse_y >= 245 and mouse_y <= 395):
            return 5

    def check_mouse_position_low_row(self, mouse_x, mouse_y):
        if (mouse_x >= 325 and mouse_x <= 470) and (mouse_y >= 395 and mouse_y <= 545):
            return 6
        if (mouse_x >= 475 and mouse_x <= 615) and (mouse_y >= 395 and mouse_y <= 545):
            return 7
        if (mouse_x >= 625 and mouse_x <= 760) and (mouse_y >= 395 and mouse_y <= 545):
            return 8

    def check_mouse_position(self, mouse_x, mouse_y):
        temp1 = self.check_mouse_position_top_row(mouse_x, mouse_y)
        temp2 = self.check_mouse_position_mid_row(mouse_x, mouse_y)
        temp3 = self.check_mouse_position_low_row(mouse_x, mouse_y)
        if temp1 in [0, 1, 2]:
            return temp1
        elif temp2 in [3, 4, 5]:
            return temp2
        elif temp3 in [6, 7, 8]:
            return temp3

    def mouse_hover(self, screen, mouse_x, mouse_y):
        temp = self.check_mouse_position(mouse_x, mouse_y)
        try:
            self.mouse_hover_event(screen, self.POSITION_COORDINATES[temp])
        except TypeError:
            '''print("(TypeError): do nothing.")'''

    def mouse_hover_event(self, screen, position_coordinates):
        mouse_hover_bg = pygame.Surface((150, 150), pygame.SRCALPHA, 32)
        mouse_hover_bg.set_alpha(100)
        mouse_hover_bg.fill(res.BLACK)
        screen.blit(mouse_hover_bg, position_coordinates)

    def place_mark(self, clicked_l, mouse_x, mouse_y, current_mark):
        global POP
        if clicked_l:
            temp = self.check_mouse_position(mouse_x, mouse_y)
            try:
                if self.BOARD[temp] == '':
                    self.BOARD[temp] = current_mark
                    # POP.play()
                    self.change_current_mark()
            except TypeError:
                '''print("(TypeError): do nothing.")'''

    def change_current_mark(self):
        global current_mark
        if current_mark == "X":
            current_mark = "O"
        elif current_mark == "O":
            current_mark = "X"

    def display_marks_on_board(self, screen):
        for position in range(len(self.BOARD)):
            if self.BOARD[position] == "X":
                screen.blit(X_MARK, self.POSITION_COORDINATES[position])
            elif self.BOARD[position] == "O":
                screen.blit(O_MARK, self.POSITION_COORDINATES[position])

    def check_winner_horizontal(self, mark, board):
        if (mark == board[0]
            and board[0] == board[1]
            and board[1] == board[2]
                and board[0] == board[2]):
            return True
        elif (mark == board[3]
              and board[3] == board[4]
              and board[4] == board[5]
                and board[3] == board[5]):
            return True
        elif (mark == board[6]
              and board[6] == board[7]
              and board[7] == board[8]
                and board[6] == board[8]):
            return True
        else:
            return False

    def check_winner_vertical(self, mark, board):
        if (mark == board[0]
            and board[0] == board[3]
            and board[3] == board[6]
                and board[0] == board[6]):
            return True
        elif (mark == board[1]
              and board[1] == board[4]
              and board[4] == board[7]
                and board[1] == board[7]):
            return True
        elif (mark == board[2]
              and board[2] == board[5]
              and board[5] == board[8]
                and board[2] == board[8]):
            return True
        else:
            return False

    def check_winner_diagonal(self, mark, board):
        if (mark == board[0]
            and board[0] == board[4]
            and board[4] == board[8]
                and board[0] == board[8]):
            return True
        elif (mark == board[2]
              and board[2] == board[4]
              and board[4] == board[6]
                and board[2] == board[6]):
            return True
        else:
            return False

    def check_winner(self, mark, board):
        if self.check_winner_horizontal(mark, board):
            return True
        elif self.check_winner_vertical(mark, board):
            return True
        elif self.check_winner_diagonal(mark, board):
            return True
        else:
            return False

    def check_draw(self):
        blank = 0
        for index in range(len(self.BOARD)):
            if self.BOARD[index] == '':
                blank += 1
        if blank == 0:
            return True
        else:
            return False

    def check_result(self):
        global winner_x, winner_o, draw
        if self.check_winner('X', self.BOARD):
            winner_x = True
        elif self.check_winner('O', self.BOARD):
            winner_o = True
        elif self.check_draw():
            draw = True
        else:
            winner_x = False
            winner_o = False
            draw = False

    def display_result(self, screen, vs_computer, winner_x, winner_o, computer_mark):
        x_pos = 950
        y_pos = 250
        board = pygame.Surface((250, 250))
        board_square = board.get_rect()
        board_square.center = (x_pos, y_pos)
        board.fill(res.WHITE)
        if vs_computer:
            if ((winner_x and computer_mark == "X")
                    or (winner_o and computer_mark == "O")):
                screen.blit(board, board_square)
                pygame.draw.rect(screen, res.BLACK, board_square, 5)
                res.display_text_centered(screen,
                                          text="YOU",
                                          size=125,
                                          color=res.BLACK,
                                          position=(950, 200))
                res.display_text_centered(screen,
                                          text="LOST!",
                                          size=115,
                                          color=res.RED,
                                          position=(950, 290))
                self.end_event()
            elif ((winner_x and computer_mark == "O")
                    or (winner_o and computer_mark == "X")):
                screen.blit(board, board_square)
                pygame.draw.rect(screen, res.BLACK, board_square, 5)
                res.display_text_centered(screen,
                                          text="YOU",
                                          size=125,
                                          color=res.BLACK,
                                          position=(950, 200))
                res.display_text_centered(screen,
                                          text="WON!",
                                          size=115,
                                          color=res.GREEN,
                                          position=(950, 290))
                self.end_event()
            elif draw:
                screen.blit(board, board_square)
                pygame.draw.rect(screen, res.BLACK, board_square, 5)
                res.display_text_centered(screen,
                                          text="IT'S A",
                                          size=75,
                                          color=res.BLACK,
                                          position=(950, 215))
                res.display_text_centered(screen,
                                          text="DRAW",
                                          size=100,
                                          color=res.RED,
                                          position=(950, 275))
                self.end_event()
        else:
            if winner_x:
                screen.blit(board, board_square)
                pygame.draw.rect(screen, res.BLACK, board_square, 5)
                res.display_text_centered(screen,
                                          text="WINNER",
                                          size=75,
                                          color=res.BLACK,
                                          position=(950, 165))
                res.display_text_centered(screen,
                                          text="X",
                                          size=300,
                                          color=res.GREEN,
                                          position=(950, 290))
                self.end_event()
            elif winner_o:
                screen.blit(board, board_square)
                pygame.draw.rect(screen, res.BLACK, board_square, 5)
                res.display_text_centered(screen,
                                          text="WINNER",
                                          size=75,
                                          color=res.BLACK,
                                          position=(950, 165))
                res.display_text_centered(screen,
                                          text="O",
                                          size=300,
                                          color=res.GREEN,
                                          position=(950, 290))
                self.end_event()
            elif draw:
                screen.blit(board, board_square)
                pygame.draw.rect(screen, res.BLACK, board_square, 5)
                res.display_text_centered(screen,
                                          text="IT'S A",
                                          size=75,
                                          color=res.BLACK,
                                          position=(950, 215))
                res.display_text_centered(screen,
                                          text="DRAW",
                                          size=100,
                                          color=res.RED,
                                          position=(950, 275))
                self.end_event()

    def end_event(self):
        global stop_click_capture
        stop_click_capture = True
        pygame.display.update()
        pygame.time.delay(1000)
        self.reset_all()

    def reset_all(self):
        global current_mark, winner_x, winner_o, draw, stop_click_capture, first_move
        self.BOARD = [
            '', '', '',
            '', '', '',
            '', '', ''
        ]
        current_mark = "X"
        winner_x = False
        winner_o = False
        draw = False
        stop_click_capture = False
        first_move = True

    def diplay_buttons(self, screen, clicked_l, mouse_x, mouse_y, board):
        res.main_menu_button(screen,
                             color=res.GRAY,
                             mouse_x=mouse_x, mouse_y=mouse_y,
                             clicked_l=clicked_l,
                             destination=main.main)
        res.back_button(screen,
                        color=res.GRAY,
                        mouse_x=mouse_x, mouse_y=mouse_y,
                        clicked_l=clicked_l,
                        destination=self.back_button_event)
        # self.new_button(screen, clicked_l, mouse_x, mouse_y)
        self.reset_button(screen, clicked_l, mouse_x, mouse_y)

    def back_button_event(self):
        global MUSIC
        MUSIC.stop()
        MUSIC.unload()
        res.BG_MUSIC.load(res.resource_path("Theme.wav"))
        res.BG_MUSIC.play(-1)
        if vs_computer:
            pve().main()
        else:
            pvp().main()

    def reset_button(self, screen, clicked_l, mouse_x, mouse_y):
        rect = res.display_text_centered(screen,
                                         text="RESET",
                                         size=50,
                                         color=res.RED,
                                         position=(150, 450))
        pygame.draw.rect(screen, res.GREEN, (75, 425, 150, 50), 2)
        if ((mouse_x >= rect[0] - 10 and mouse_x <= rect[0] + rect[2] + 10)
                and (mouse_y >= rect[1] - 10 and mouse_y <= rect[1] + rect[3] + 10)
                and clicked_l):
            self.reset_all()

    def new_button(self, screen, clicked_l, mouse_x, mouse_y):
        rect = res.display_text_centered(screen,
                                         text="NEW",
                                         size=50,
                                         color=res.GREEN,
                                         position=(150, 500))
        pygame.draw.rect(screen, res.GREEN, (75, 475, 150, 50), 2)
        if ((mouse_x >= rect[0] - 10 and mouse_x <= rect[0] + rect[2] + 10)
                and (mouse_y >= rect[1] - 10 and mouse_y <= rect[1] + rect[3] + 10)
                and clicked_l):
            self.reset_all()

    def computer_move(self, computer_mark, player_mark):
        pygame.time.delay(500)
        if difficulty == "EASY":
            self.computer_minimizing(computer_mark, player_mark)
        elif difficulty == "HARD":
            self.computer_maximizing(computer_mark, player_mark)
        self.change_current_mark()

    def computer_minimizing(self, computer_mark, player_mark):
        global first_move
        if first_move:
            self.computer_first_move(computer_mark)
            first_move = False
        else:
            if (self.maximize_move(player_mark, computer_mark) is False
                    and self.maximize_move(computer_mark, computer_mark) is False):
                self.computer_random_move(computer_mark)

    def computer_maximizing(self, computer_mark, player_mark):
        global first_move
        if first_move:
            self.computer_first_move(computer_mark)
            first_move = False
        else:
            if (self.maximize_move(computer_mark, computer_mark) is False
                    and self.maximize_move(player_mark, computer_mark) is False):
                self.computer_random_move(computer_mark)

    def computer_first_move(self, computer_mark):
        if self.BOARD[4] == '':
            self.BOARD[4] = computer_mark
        else:
            self.computer_random_move(computer_mark)

    def computer_random_move(self, computer_mark):
        move = True
        while move:
            random_index = random.randint(0, 8)
            if self.BOARD[random_index] == '':
                self.BOARD[random_index] = computer_mark
                move = False

    def maximize_move(self, check_mark, computer_mark):
        for pos in range(len(self.BOARD)):
            board_copy = self.BOARD.copy()
            if board_copy[pos] == '':
                board_copy[pos] = check_mark
                if self.check_winner(check_mark, board_copy):
                    self.BOARD[pos] = computer_mark
                    return True
        return False

    def check_turn(self, screen, vs_computer, current_mark, computer_mark, player_mark, clicked_l, mouse_x, mouse_y):
        if vs_computer and current_mark == computer_mark:
            self.computer_move(computer_mark, player_mark)
            self.display_marks_on_board(screen)
            self.check_result()
        else:
            self.place_mark(clicked_l, mouse_x, mouse_y, current_mark)
            self.display_marks_on_board(screen)
            self.check_result()

    def main(self):
        global current_mark, winner_x, winner_o, draw, stop_click_capture, first_move
        global MUSIC, POP
        pygame.display.set_icon(res.G2GICON)
        SCREEN = pygame.display.set_mode((res.SCREEN_WIDTH, res.SCREEN_HEIGHT))
        res.BG_MUSIC.stop()
        MUSIC = pygame.mixer.music
        MUSIC.load(res.resource_path("TikTakToe\\Music.wav"))
        MUSIC.play(-1)
        POP = pygame.mixer.Sound(
            res.resource_path("TikTakToe\\Pop.wav"))
        run = True
        clock = pygame.time.Clock()
        self.BOARD = ['', '', '', '', '', '', '', '', '']
        current_mark = "X"
        winner_x = False
        winner_o = False
        draw = False
        stop_click_capture = False
        first_move = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if stop_click_capture is False:
                    clicked_l = res.check_mouse_l_click(event)
            mouse_x, mouse_y = pygame.mouse.get_pos()

            SCREEN.fill(res.BLUE)
            self.display_texts(SCREEN, current_mark)
            self.display_board(SCREEN)
            self.mouse_hover(SCREEN, mouse_x, mouse_y)
            self.check_turn(SCREEN, vs_computer, current_mark,
                            computer_mark, player_mark, clicked_l, mouse_x, mouse_y)
            self.display_result(SCREEN, vs_computer,
                                winner_x, winner_o, computer_mark)
            self.diplay_buttons(SCREEN, clicked_l, mouse_x,
                                mouse_y, self.BOARD)

            clock.tick(60)
            pygame.display.update()


class pve:
    def display_texts(self, screen):
        res.display_text_centered(screen,
                                  text="Tik-Tak-Toe",
                                  size=200,
                                  color=res.GREEN,
                                  position=(res.SCREEN_WIDTH//2, 125))
        res.display_text_centered(screen,
                                  text="Choose Difficulty",
                                  size=100,
                                  color=res.WHITE,
                                  position=(res.SCREEN_WIDTH//2, 250))
        res.display_text_centered(screen,
                                  text="You use X mark",
                                  size=50,
                                  color=res.BLACK,
                                  position=(res.SCREEN_WIDTH//4+50, 490))
        res.display_text_centered(screen,
                                  text="You're 1st to move.",
                                  size=50,
                                  color=res.BLACK,
                                  position=(res.SCREEN_WIDTH//4+50, 525))
        res.display_text_centered(screen,
                                  text="There is a 50% chance you'll win this!",
                                  size=25,
                                  color=res.BLACK,
                                  position=(res.SCREEN_WIDTH//4+50, 550))
        res.display_text_centered(screen,
                                  text="You use O mark",
                                  size=50,
                                  color=res.BLACK,
                                  position=(res.SCREEN_WIDTH//4*3-50, 490))
        res.display_text_centered(screen,
                                  text="You're 2nd to move.",
                                  size=50,
                                  color=res.BLACK,
                                  position=(res.SCREEN_WIDTH//4*3-50, 525))
        res.display_text_centered(screen,
                                  text="It is almost imposible to win this! Goodluck!",
                                  size=25,
                                  color=res.BLACK,
                                  position=(res.SCREEN_WIDTH//4*3-50, 550))

    def display_buttons(self, screen, clicked_l, mouse_x, mouse_y):
        res.main_menu_button(screen,
                             color=res.GRAY,
                             mouse_x=mouse_x, mouse_y=mouse_y,
                             clicked_l=clicked_l,
                             destination=main.main)
        res.back_button(screen,
                        color=res.GRAY,
                        mouse_x=mouse_x, mouse_y=mouse_y,
                        clicked_l=clicked_l,
                        destination=menu().main)
        self.easy_button(screen, clicked_l, mouse_x, mouse_y)
        self.hard_button(screen, clicked_l, mouse_x, mouse_y)

    def easy_button(self, screen, clicked_l, mouse_x, mouse_y):
        global difficulty, player_mark, computer_mark
        res.display_rectangle(screen,
                              color=res.GRAY,
                              position=(res.SCREEN_WIDTH//4+50, 400),
                              dimension=(325, 125))
        if ((mouse_x >= 160 and mouse_x <= 485)
                and (mouse_y >= 335 and mouse_y <= 460)):
            res.display_rectangle(screen,
                                  color=res.BLACK,
                                  position=(res.SCREEN_WIDTH//4+50, 400),
                                  dimension=(325, 125))
            if clicked_l:
                difficulty = "EASY"
                player_mark = "X"
                computer_mark = "O"
                game().main()
        pygame.draw.rect(screen, res.BLACK, (160, 335, 330, 130), 5)
        res.display_text_centered(screen,
                                  text="EASY",
                                  size=150,
                                  color=res.AQUA,
                                  position=(res.SCREEN_WIDTH//4+50, 405))

    def hard_button(self, screen, clicked_l, mouse_x, mouse_y):
        global difficulty, player_mark, computer_mark
        res.display_rectangle(screen,
                              color=res.GRAY,
                              position=(res.SCREEN_WIDTH//4*3-50, 400),
                              dimension=(325, 125))
        if ((mouse_x >= 610 and mouse_x <= 940)
                and (mouse_y >= 335 and mouse_y <= 460)):
            res.display_rectangle(screen,
                                  color=res.BLACK,
                                  position=(res.SCREEN_WIDTH//4*3-50, 400),
                                  dimension=(325, 125))
            if clicked_l:
                difficulty = "HARD"
                player_mark = "O"
                computer_mark = "X"
                game().main()
        pygame.draw.rect(screen, res.BLACK, (610, 335, 330, 130), 5)
        res.display_text_centered(screen,
                                  text="HARD",
                                  size=150,
                                  color=res.RED,
                                  position=(res.SCREEN_WIDTH//4*3-50, 405))

    def main(self):
        global vs_computer
        pygame.display.set_icon(res.G2GICON)
        SCREEN = pygame.display.set_mode((res.SCREEN_WIDTH, res.SCREEN_HEIGHT))
        run = True
        clock = pygame.time.Clock()
        vs_computer = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                clicked_l = res.check_mouse_l_click(event)
            mouse_x, mouse_y = pygame.mouse.get_pos()

            SCREEN.fill(res.BLUE)

            self.display_texts(SCREEN)
            self.display_buttons(SCREEN, clicked_l, mouse_x, mouse_y)

            clock.tick(60)
            pygame.display.update()


if __name__ == "__main__":
    menu().main()
