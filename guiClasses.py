import pygame
import math
import time

pygame.font.init()

# Constants of Colour
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (245, 140, 140)
ORANGE = (227, 153, 84)
YELLOW = (250, 242, 172)
GREEN = (209, 252, 174)
TEAL = (155, 224, 194)
BLUE = (84, 124, 227)
PURPLE = (196, 154, 245)
PINK = (250, 172, 197)
GREY = (200, 204, 201)
DARKGREY = (94, 88, 83)
LIGHTORANGE = (255, 227, 181)
LIGHTBLUE = (173, 226, 255)
LIGHTPINK = (255, 182, 193)
base_font = pygame.font.Font("freesansbold.ttf", 16)
big_font = pygame.font.Font("freesansbold.ttf", 30)



class Main():
    def __init__(self, screen):
        self.screen = screen




class Ball:  # used to represent the particles when simulating their interaction
    def __init__(self, x, y, r, label, colour=DARKGREY):
        self.colour = colour
        self.x = x
        self.y = y
        self.state = 0
        self.centre = (self.x, self.y)
        self.radius = r
        self.label = label  # used to keep a constant label following the particle such as "proton"

    def draw(self, screen):  # renders the object on the screen (its label and circle)
        label = base_font.render(self.label, True, DARKGREY)
        try:
            screen.blit(label, (self.centre[0] - 50, self.centre[1] + 10))
        except TypeError:
            return True
        pygame.draw.circle(screen, self.colour, self.centre, self.radius)

    def check_click(self, screen, event):  # checking if the circle has been clicked upon
        x, y = event.pos  # the ball has been clicked if the click is within a radius of the centre
        distance = math.hypot(x - self.centre[0], y - self.centre[1])
        if distance <= self.radius:
            self.state = not self.state
            self.draw(screen)

    def update_pos(self, coord):  # a setter method to change the position of the centre of the Ball
        self.centre = coord


class WriteBox:  # an input box
    def __init__(self, x, y, w, h, label, colour=BLACK, string="", start_string="", expand=True):  # start_string is
        # displayed before the box is edited, generally used to display units; expand determines whether the box
        # expands when overfull or not.
        self.color_active = pygame.Color(GREY)  # the active colour is used when the box has been clicked on
        self.color_passive = colour  # the passive colour is used when the box has not been clicked on
        self.x = x
        self.y = y
        self.state = 0
        self.w = w
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, w, h)
        self.string = string
        self.label = label
        self.start_string = start_string
        self.expand = expand

    def draw(self, screen):  # renders the box (label, box, string)
        label = base_font.render(self.label, True, BLACK)
        screen.blit(label, (self.rect.x - 100, self.rect.y + 10))
        pygame.draw.rect(screen, (self.color_passive if self.state == 0 else self.color_active), self.rect, width=5)
        if not self.state and self.string == "":  # if the box is empty and not clicked on, then the box is displayed
            # empty and with the start_string in it
            guide = base_font.render(self.start_string, True, GREY)
            screen.blit(guide, (self.rect.x + 10, self.rect.y + 12))
        else:
            guide = base_font.render(self.start_string, True, WHITE)  # if it is not, it is covered by rewriting over
            # the start string in white
            screen.blit(guide, (self.rect.x + 10, self.rect.y + 12))
        text_surface = base_font.render(self.string, True, DARKGREY)  # the text is rendered
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 12))
        if self.expand:
            self.rect.w = max(300, text_surface.get_width() + 12)

    def check_click(self, screen, event, auto=False):  # a method called to check if the box has been clicked on
        check_collide = False
        try:
            check_collide = self.rect.collidepoint(event.pos)
        except AttributeError:
            pass

        if check_collide or auto:  # if it has been clicked on or is being called from the program to automatically
            # click it
            self.state = 1
            self.draw(screen)
            pygame.display.update()
            time.sleep(0.5)

    def write(self, event):  # updates the text with the key that has been pressed or deletes if backspace has been
        # pressed
        if self.state:
            if event.key == pygame.K_BACKSPACE:
                self.string = self.string[:-1]
            else:
                self.string += event.unicode


class Button:  # a clickable button
    def __init__(self, colour, strings, x, y, w, h):
        self.colour = colour
        self.strings = strings
        self.str_count = 1  # a record of how many times a button has been clicked such that the string displayed can be
        # iterated through, e.g. pause and play
        if strings is not None:  # used if Arrow is not instantiated
            self.string = strings[0]
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.state = 0
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, screen):  # renders the button
        pygame.draw.rect(screen, self.colour if self.state == 0 else GREY, self.rect, width=0)
        text_surface = base_font.render(self.string, True, DARKGREY)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 12))

    def check_click(self, screen, event, auto=False):  # checking if the button has been clicked on with the same
        # conditions as WriteBox
        check_collide = False
        try:
            check_collide = self.rect.collidepoint(event.pos)
        except AttributeError:
            pass

        if check_collide or auto:
            self.state = 1
            self.str_count += 1
            if self.strings is not None:
                self.string = self.strings[self.str_count % 2 - 1]
            self.draw(screen)
            pygame.display.update()
            time.sleep(0.25)


class DropDown(Button):
    def __init__(self, colour, string, x, y, w, h, index):  # DropDown is initialised as a list of buttons that
        # change index to change display order
        super().__init__(colour, string, x, y, w, h)
        self.index = index
        self.y = y + h * self.index
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, screen):  # renders the first box if the selection is not happening else the whole list
        if self.index == 0 or self.state == 1:
            pygame.draw.rect(screen, self.colour, self.rect, width=5)
            text_surface = base_font.render(self.string, True, DARKGREY)
            screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 12))
            if self.index == 0:
                pygame.draw.polygon(screen, self.colour,
                                    [(self.w / 10 * 8 + self.x, self.y + self.h / 3), (self.x + self.w / 10 * 9,
                                                                                       self.y + self.h / 3),
                                     (self.x + self.w / 10 * 8.5, self.y + self.h / 3 * 2)])

    def check_click(self, screen, event, dropdown_list=None):  # checks whether an object in the list has been
        # clicked on
        if self.rect.collidepoint(event.pos) and self.index == 0:  # clicks the list on and off
            self.state = not self.state
            for d2 in dropdown_list[1::]:
                d2.state = self.state

        elif self.rect.collidepoint(event.pos) and self.state == 1:  # changes the selection to the one that has been
            # clicked on
            dropdown_list[0].string = self.string
            self.string = dropdown_list[0].string
            for d2 in dropdown_list:  # clicks the list off
                d2.state = 0


class Arrow(Button):  # for adjusting the energy
    def __init__(self, colour, x, y, w, h, up_down):  # up_down determines whether to use an up or down arrow in
        # rendering
        super().__init__(colour, None, x, y, w, h)
        self.up_down = up_down

    def draw(self, screen):  # returns the button
        pygame.draw.rect(screen, self.colour if self.state == 0 else GREY, self.rect, width=5)
        text_surface = base_font.render("", True, DARKGREY)
        screen.blit(text_surface, (self.rect.x + 40, self.rect.y + 12))
        if self.up_down == 0:  # down arrow
            pygame.draw.polygon(screen, self.colour,
                                [(self.w / 3 + self.x, self.y + self.h / 3), (self.x + 2 * self.w / 3,
                                                                              self.y + self.h / 3),
                                 (self.x + self.w / 2, self.y + self.h / 3 * 2 - 1)])
        else:  # up arrow
            pygame.draw.polygon(screen, self.colour,
                                [(self.w / 3 + self.x, self.y + self.h / 3 * 2 - 1), (self.x + 2 * self.w / 3,
                                                                                      self.y + self.h / 3 * 2 - 1),
                                 (self.x + self.w / 2, self.y + self.h / 3)])


class Combination:  # a compound of a WriteBox and an up arrow and down arrow, used to change the scaling in main.py
    def __init__(self, colour, label, string, x, y, w, h, start_string="", text=None):
        self.start_string = start_string
        self.colour = colour
        self.x = x
        self.y = y
        self.w_arrow = 40
        self.w_text = w - self.w_arrow
        self.h = h
        self.string = string
        if text is None:  # the Combination box is refreshed hence this is for the first instantiation
            self.text = WriteBox(self.x, self.y, self.w_text, self.h, label, colour=BLACK, string="",
                                 start_string=self.start_string, expand=False)
        else:  # if the Combination has been previously instantiated and text has been passed into the parameter
            self.text = text
        self.up_arrow = Arrow(self.colour, self.x + self.w_text + 24, y, self.w_arrow - 4, h // 2 - 2, 1)
        self.down_arrow = Arrow(self.colour, self.x + self.w_text + 24, y + h // 2 + 2, self.w_arrow - 4, h // 2 - 2, 0)

    def draw(self, screen):  # renders all components of the Combination
        self.text.draw(screen)
        self.up_arrow.draw(screen)
        self.down_arrow.draw(screen)

    def check_click(self, screen, event):  # checks if any component has been clicked on
        self.text.check_click(screen, event)
        self.up_arrow.check_click(screen, event)
        self.down_arrow.check_click(screen, event)

    def write(self, event):  # updates the text box with the event
        self.text.write(event)
