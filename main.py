import math
import pygame
import time
import sys
import randomcolor as randomcolor
import atmosphere
import guiClasses
import dataAnalysis
import particleClasses

# Constants of Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (245, 140, 140)
ORANGE = (247, 171, 89)
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

# Initialising Pygame
pygame.init()
clock = pygame.time.Clock()

X = 1200
Y = 700
window = guiClasses.Main(pygame.display.set_mode((X, Y), pygame.RESIZABLE))

pygame.display.set_caption("Particle Simulator")


def screen_blank(border_colour):
    window.screen.fill(WHITE)
    pygame.draw.rect(window.screen, border_colour,
                     pygame.Rect(0, 0, window.screen.get_width(), window.screen.get_height()), 5)


screen_blank(BLACK)


# Defining the Vector class which is used to deal with the two dimensions the particles can move in
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.magnitude = (x ** 2 + y ** 2) ** 0.5  # the magnitude of the vector
        self.hat = Vector(self.x / self.magnitude,
                          self.y / self.magnitude) if (self.magnitude not in [1, 0]) else None  # the unit vector in the
        # direction of the original, creates a vector itself, preventing recursion by setting the unit vector of the
        # unit vector to None

    def __str__(self):
        return f"({self.x}, {self.y})"  # for testing

    def __add__(self, other):
        return Vector(self.x + other.x,
                      self.y + other.y)  # operator methods so that vectors can be added, subtracted, multipled as
        # needed in calculations

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)


# Conversions between pygame and real scaling
def pygame_real(n, scale):
    return n * 10 ** scale


def real_pygame(n, scale):
    return round(n * 10 ** (-scale))


# Calculates the new position of the interacting particle
def simulation(b1, b2, particle1, particle2, p_i, trace_colour, running_time, energy, scale=-21,
               timescale=10 ** (-30) / 2):
    eps0 = 8.85 * 10 ** (-12)  # epsilon0, the permittivity of free space
    t = 5 * 10 ** timescale  # deltat, a small change in t
    b1vector = Vector(pygame_real(b1.centre[0], scale), pygame_real(b1.centre[1],
                                                                    scale))  # vectors to describe the current centre of the markers in real scaling
    b2vector = Vector(pygame_real(b2.centre[0], scale), pygame_real(b2.centre[1], scale))
    dispvector = b2vector - b1vector  # the displacement between the two calculated using the operator method __sub__ on the two vectors
    q1 = particle1.get_charge() * 1.6 * 10 ** (
        -19)  # using the getter methods of the particles to get the charge and convert it from e to Coulombs
    q2 = particle2.get_charge() * 1.6 * 10 ** (-19)
    mass = float(particle1._mass) * 1.79 * 10 ** (
        -30)  # getting the mass of particle1 and converting it from MeV/c^2 to kg
    F = dispvector.hat * (
            -q1 * q2 / (4 * math.pi * eps0 * dispvector.magnitude ** 2))  # using the formula of electric force
    p = F * t + p_i  # the momentum is calculated by adding the previous momentum to the new force multiplied by the small change in time
    deltad = p * (1 / mass) * t  # momentum/mass = velocity, velocity*t = displacement
    b1vector += deltad  # the position of b1 is updated with the displacement
    new_x = real_pygame(b1vector.x, scale)  # the components of the vector are converted from real to pygame units
    new_y = real_pygame(b1vector.y, scale)
    ocentre = b1.centre  # the original centre is stored so that it can be checked for overlap with the other particle
    b1.update_pos(
        (new_x, new_y))  # a setter method is used to change the centre of the ball to the newly calculated position
    trace = guiClasses.Ball(new_x, new_y, 2, "", trace_colour)  # a trace is made in the same position
    if ocentre == b2.centre or new_x <= 0 or new_x >= window.screen.get_width() or new_y <= 0 or new_y >= window.screen.get_height():  # checking for overlap and that the new position is within the bounds of the screen
        return b1vector.x, b1vector.y, running_time + t, True, Vector(
            float(energy) * (10 ** 6) * 1.6 * (10 ** (-19)) / 3 / (10 ** 8) * (2 ** 0.5),
            0), trace  # returns the newly calculated position, the time elapsed since the start of the simulation, that the simulation has finished, the original momentum so that the simulation can start again, and the trace
    return b1vector.x, b1vector.y, running_time + t, False, p, trace  # returns the newly calculated position, the time elapsed since the start of the simulation, that the simulation should continue, the momentum, and the trace


# Displays options to select a particle, returns selection
def display_menu():
    preexisting = guiClasses.Button(LIGHTBLUE, ["Pre-existing"], window.screen.get_width() // 2 - 190 / 2,
                                    window.screen.get_height() // 3 + 20, 190, 40)

    custom = guiClasses.Button(LIGHTORANGE, ["Custom"], window.screen.get_width() // 2 - 190 / 2,
                               window.screen.get_height() // 3 + 70, 190, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                preexisting.check_click(window.screen, event)
                custom.check_click(window.screen, event)

                if preexisting.state:
                    return "preexisting"
                if custom.state:
                    return "custom"

        screen_blank(LIGHTPINK)
        text = guiClasses.big_font.render("Particle Simulation:", True, DARKGREY, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (window.screen.get_width() // 2, window.screen.get_height() // 10)
        window.screen.blit(text, text_rect)
        preexisting.draw(window.screen)
        custom.draw(window.screen)
        pygame.display.update()


# Displays options for particle interaction, returns selection
def display_sim_menu():
    text = guiClasses.big_font.render("Simulation Options:", True, DARKGREY, WHITE)
    textRect = text.get_rect()
    textRect.center = (window.screen.get_width() // 2, window.screen.get_height() - 740)
    window.screen.blit(text, textRect)

    back = guiClasses.Button(TEAL, ["BACK"], 70, 360 + 500, 120, 40)
    back.draw(window.screen)
    interaction = guiClasses.Button(YELLOW, ["Interaction"], window.screen.get_width() // 2 - 190 / 2,
                                    window.screen.get_height() // 3 + 20, 190, 40)
    interaction.draw(window.screen)
    shower = guiClasses.Button(RED, ["Particle Shower"], window.screen.get_width() // 2 - 190 / 2,
                               window.screen.get_height() // 3 + 70, 190, 40)
    shower.draw(window.screen)

    stats_screen([p1, p2])

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                interaction.check_click(window.screen, event)
                shower.check_click(window.screen, event)
                back.check_click(window.screen, event)

                if interaction.state:
                    return "interaction"
                if shower.state:
                    return "shower"
                if back.state:
                    return "back"


def error(message):
    error_message = guiClasses.WriteBox(window.screen.get_width() - 350, 120, 280, 40, "Error:", RED, string=message)
    error_message.draw(window.screen)
    pygame.display.update()
    time.sleep(2)


# Displays the statistics of the chosen particle
def stats_screen(particles):
    options_xb = X / 9 + 31
    options = guiClasses.WriteBox(options_xb + 6, Y // 3, 300, 350, "", DARKGREY, string="")
    options.draw(window.screen)

    options_x = options_xb + 6
    options = guiClasses.WriteBox(options_x + 6, Y // 3 + 6, 288, 338, "", GREEN, string="")
    options.draw(window.screen)

    title = guiClasses.big_font.render(f"STATS:", True, DARKGREY, WHITE)
    textRect = title.get_rect()
    y = Y // 3 + 60
    textRect.center = (150 + options_x, y - 20)
    window.screen.blit(title, textRect)

    try:
        name1 = guiClasses.base_font.render(f"Name: {particles[0]._name}", True, DARKGREY, WHITE)
    except AttributeError:
        name1 = guiClasses.base_font.render(f"Name: ", True, DARKGREY, WHITE)

    textRect1 = name1.get_rect()
    textRect1.center = (150 + options_x, y + 20)
    window.screen.blit(name1, textRect1)

    try:
        name1 = guiClasses.base_font.render(f"Mass: {particles[0]._mass}MeV/c^2", True, DARKGREY, WHITE)
    except AttributeError:
        name1 = guiClasses.base_font.render(f"Mass: ", True, DARKGREY, WHITE)

    textRect1 = name1.get_rect()
    textRect1.center = (150 + options_x, y + 40)
    window.screen.blit(name1, textRect1)

    try:
        name1 = guiClasses.base_font.render(f"Charge: {particles[0]._charge}e", True, DARKGREY, WHITE)
    except AttributeError:
        name1 = guiClasses.base_font.render(f"Charge: ", True, DARKGREY, WHITE)

    textRect1 = name1.get_rect()
    textRect1.center = (150 + options_x, y + 60)
    window.screen.blit(name1, textRect1)

    try:
        name2 = guiClasses.base_font.render(f"Name: {particles[1]._name}", True, DARKGREY, WHITE)
    except AttributeError:
        name2 = guiClasses.base_font.render(f"Name: ", True, DARKGREY, WHITE)

    textRect1 = name2.get_rect()
    textRect1.center = (150 + options_x, y + 120)
    window.screen.blit(name2, textRect1)

    try:
        name2 = guiClasses.base_font.render(f"Mass: {particles[1]._mass}MeV/c^2", True, DARKGREY, WHITE)
    except AttributeError:
        name2 = guiClasses.base_font.render(f"Mass: ", True, DARKGREY, WHITE)

    textRect1 = name2.get_rect()
    textRect1.center = (150 + options_x, y + 140)
    window.screen.blit(name2, textRect1)

    try:
        name2 = guiClasses.base_font.render(f"Charge: {particles[1]._charge}e", True, DARKGREY, WHITE)
    except AttributeError:
        name2 = guiClasses.base_font.render(f"Charge: ", True, DARKGREY, WHITE)

    textRect1 = name2.get_rect()
    textRect1.center = (150 + options_x, y + 160)
    window.screen.blit(name2, textRect1)


# Takes the input of the user to determine what particles should be selected as well as the energy
def main_preexisting(dropdown1, dropdown2, energyBox):
    p1 = ""
    p2 = ""
    breaking = False

    while True:
        back_button = guiClasses.Button(TEAL, ["MENU"], 70, window.screen.get_height() // 10 * 8, 80, 40)
        enter = guiClasses.Button(GREEN, ["ENTER"], window.screen.get_width() // 10 * 8,
                                  window.screen.get_height() // 10 * 8, 190, 40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                energyBox.check_click(window.screen, event)
                enter.check_click(window.screen, event)
                back_button.check_click(window.screen, event)
                for d in dropdown1:
                    d.check_click(window.screen, event, dropdown1)
                for d in dropdown2:
                    d.check_click(window.screen, event, dropdown2)
                p1 = optionsobj[options.index(
                    dropdown1[0].string)]  # the particles are selected based on a lookup of the objects list
                p2 = optionsobj[options.index(dropdown2[0].string)]

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if energyBox.state:
                        energyBox.state = 0
                    enter.check_click(window.screen, event, True)

                else:
                    energyBox.write(event)

        if enter.state:
            energy = energyBox.string
            return p1, p2, energy, False

        if back_button.state:
            return None, None, None, True

        screen_blank(LIGHTBLUE)
        text = guiClasses.big_font.render("ENTER REQUIREMENTS:", True, RED, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (window.screen.get_width() // 2, window.screen.get_height() // 10)
        window.screen.blit(text, text_rect)
        stats_screen([p1, p2])

        for d in dropdown1:
            d.draw(window.screen)
        for d in dropdown2:
            d.draw(window.screen)
        enter.draw(window.screen)
        energyBox.draw(window.screen)
        back_button.draw(window.screen)

        pygame.display.update()
        clock.tick(120)
        if breaking:
            break


# Takes more inputs from the user to create a custom particle
def main_custom(mass1, charge1, energyBox, mass2, charge2):
    breaking = False

    while True:
        enter = guiClasses.Button(GREEN, ["ENTER"], window.screen.get_width() - 70 - 190, window.screen.get_height() // 10 * 8, 190, 40)
        back_button = guiClasses.Button(TEAL, ["MENU"], 70, window.screen.get_height() // 10 * 8, 80, 40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mass1.check_click(window.screen, event)
                charge1.check_click(window.screen, event)
                energyBox.check_click(window.screen, event)
                mass2.check_click(window.screen, event)
                charge2.check_click(window.screen, event)
                enter.check_click(window.screen, event)
                back_button.check_click(window.screen, event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if mass1.state:
                        mass1.state = 0
                        charge1.state = 1
                    elif charge1.state:
                        charge1.state = 0
                        energyBox.state = 1
                    elif energyBox.state:
                        energyBox.state = 0
                        mass2.state = 1
                    elif mass2.state:
                        mass2.state = 0
                        charge2.state = 1
                    elif charge2.state:
                        charge2.state = 0
                        enter.check_click(window.screen, event, True)


                else:
                    mass1.write(event)
                    charge1.write(event)
                    energyBox.write(event)
                    mass2.write(event)
                    charge2.write(event)

        if enter.state:
            energy = energyBox.string
            p1 = particleClasses.Particle("Particle1", "p1", charge1.string,
                                          mass1.string)  # a object type Particle is created with the parameters specified by the user
            p2 = particleClasses.Particle("Particle2", "p2", charge2.string, mass2.string)
            return p1, p2, energy, False

        if back_button.state:
            return None, None, None, True

        window.screen.fill(WHITE)
        pygame.draw.rect(window.screen, LIGHTBLUE,
                         pygame.Rect(0, 0, window.screen.get_width(), window.screen.get_height()), width=5)
        text = guiClasses.big_font.render("ENTER REQUIREMENTS:", True, RED, WHITE)
        textRect = text.get_rect()
        textRect.center = (253, 130)
        window.screen.blit(text, textRect)

        enter.draw(window.screen)
        back_button.draw(window.screen)

        mass1.draw(window.screen)
        charge1.draw(window.screen)
        energyBox.draw(window.screen)

        mass2.draw(window.screen)
        charge2.draw(window.screen)

        pygame.display.update()
        clock.tick(240)
        if breaking:
            break


# An intermediary screen between the second menu and the particle shower simulation allowing the user to input an energy
def get_energy(energyBox, filenameBox, back_button):
    enter = guiClasses.Button(GREEN, ["ENTER"], window.screen.get_width() - 70 - 190, 360 + 500, 190, 40)
    breaking = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                energyBox.check_click(window.screen, event)
                filenameBox.check_click(window.screen, event)
                enter.check_click(window.screen, event)
                back_button.check_click(window.screen, event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if energyBox.state:
                        energyBox.state = 0
                        filenameBox.state = 1

                else:
                    energyBox.write(event)
                    filenameBox.write(event)

        if enter.state:
            energy = energyBox.string
            filename = filenameBox.string
            return filename, energy, False

        if back_button.state:
            return None, None, True

        window.screen.fill(WHITE)
        pygame.draw.rect(window.screen, LIGHTPINK,
                         pygame.Rect(0, 0, window.screen.get_width(), window.screen.get_height()), width=5)
        text = guiClasses.big_font.render("ENTER REQUIREMENTS:", True, RED, WHITE)
        textRect = text.get_rect()
        textRect.center = (253, 130)
        window.screen.blit(text, textRect)

        enter.draw(window.screen)
        back_button.draw(window.screen)

        energyBox.draw(window.screen)
        filenameBox.draw(window.screen)

        pygame.display.update()
        clock.tick(240)
        if breaking:
            break


# Handles the display of the simulation
def main_interaction(p1, p2, energy, back_button, record):
    p1s = []  # allows for dynamic generation of marker objects
    p2s = []

    dragged = None  # variables for the movement and positioning of markers
    rectangle_dragging = False
    offset_x = 0
    offset_y = 0

    timecount = 0

    play = guiClasses.Button(GREEN, ["PLAY", "PAUSE"], window.screen.get_width // 10 * 8, window.screen.get_height // 2 + 150, 190,
                             40)  # play/pause button
    graph = guiClasses.Button(ORANGE, ["COMPARE"], window.screen.get_width // 10 * 8, window.screen.get_height // 2 + 100, 190,
                              40)  # button to display graphs
    clear = guiClasses.Button(YELLOW, ["CLEAR"], window.screen.get_width // 10 * 8, window.screen.get_height // 2 + 50, 190, 40)
    scaling = guiClasses.Combination(LIGHTPINK, "1px:", "", window.screen.get_width // 10 * 8, window.screen.get_height // 2, 190, 40,
                                     "10^-21m")
    time_scaling = guiClasses.Combination(LIGHTBLUE, "1 frame:", "", window.screen.get_width // 10 * 8, window.screen.get_height // 2 - 50,
                                          190, 40, "5*10^-31s")

    traces = []  # list containing all traces (previous positions as Ball objects)

    xpos = []  # a record of all positions in real units for graph display
    ypos = []
    times = []

    scale = str(-21)
    time_scale = "-31"

    error_found = False
    trace_colour = randomcolor.RandomColor().generate(format_="rgb")[0][4:-2].split(",")
    trace_colour = tuple(
        [int(i.lstrip()) if i != '' else 0 for i in
         trace_colour])  # a random colour generated so the traces are all different colours
    if energy == "":
        energy = 0

    try:
        momentum = Vector(float(energy) * (10 ** 6) * 1.6 * (10 ** (-19)) / 3 / (10 ** 8) * (2 ** 0.5),
                          0)  # momentum is calculated using the user inputted energy
    except ValueError:
        error("Incorrectly formatted data")
        return True

    while True:
        clearing = False
        action = False  # action is used to have a small delay after pressing a button
        reset = False  # is set to True when the simulation has finished running
        play.state = 0
        graph.state = 0
        gen_p1 = guiClasses.Button(LIGHTBLUE, ["P1"], 100, Y // 2 - 100, 40,
                                   40)  # buttons for the dynamic generation of Ball objects to be used as markers
        gen_p2 = guiClasses.Button(LIGHTPINK, ["P2"], 100, Y // 2 + 100, 40, 40)
        scaling = guiClasses.Combination(LIGHTPINK, "1px:", "", X - 70 - 190, Y // 2, 190, 40,
                                         "10^" + str(scale) + "m", scaling.text)
        time_scaling = guiClasses.Combination(LIGHTBLUE, "1 frame:", "", X - 70 - 190, Y // 2 - 50, 190, 40,
                                              "5*10^" + str(time_scale) + "m",
                                              time_scaling.text)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                gen_p1.check_click(window.screen, event)
                gen_p2.check_click(window.screen, event)
                play.check_click(window.screen, event)
                graph.check_click(window.screen, event)
                clear.check_click(window.screen, event)
                back_button.check_click(window.screen, event)
                if play.string != "PAUSE":
                    scaling.check_click(window.screen, event)
                    time_scaling.check_click(window.screen, event)

                for p in p1s:
                    if event.button == 1:
                        p.check_click(window.screen,
                                      event)  # checking if one of the draggable markers has been clicked on
                        if p.state:
                            rectangle_dragging = True  # if it has been clicked on, the offset of the mouse is recorded and the tracking variable is set to True
                            mouse_x, mouse_y = event.pos
                            offset_y = p.centre[1] - mouse_y
                            offset_x = p.centre[0] - mouse_x
                            dragged = p
                            break

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if scaling.text.state:
                        scaling.text.start_string = "10^" + scaling.text.string + "m"
                        scaling.text.string = ""
                        scale = scaling.text.start_string[3:-1]
                        scaling.text.state = 0
                    elif time_scaling.text.state:
                        time_scaling.text.start_string = "5*10^" + time_scaling.text.string + "s"
                        time_scaling.text.string = ""
                        time_scale = time_scaling.text.start_string[5:-1]
                        time_scaling.text.state = 0

                else:
                    if scaling.text.state:
                        scaling.write(event)
                    elif time_scaling.text.state:
                        time_scaling.write(event)

            if rectangle_dragging:
                if event.type == pygame.MOUSEBUTTONUP and dragged.state:  # the draggable marker's position is updated
                    if event.button == 1:
                        dragged.state = False
                        rectangle_dragging = False
                        dragged = None

                elif event.type == pygame.MOUSEMOTION and dragged != None and dragged.state:
                    if rectangle_dragging:
                        mouse_x, mouse_y = event.pos
                        dragged.centre = (mouse_x + offset_x, mouse_y + offset_y)

        try:
            if gen_p1.state:
                p1s.append(
                    guiClasses.Ball(window.screen.get_width() // 2, window.screen.get_height() // 2, 10, p1._symbol,
                                    LIGHTBLUE))  # dynamic generation of marker objects to be used in the simulations
                action = True

            elif gen_p2.state:
                p2s.append(guiClasses.Ball(window.screen.get_width() // 2 + 100, window.screen.get_height() // 2, 10,
                                           p2._symbol, LIGHTPINK))
                action = True
        except AttributeError:
            error("Incorrectly formatted data")
            return True

        if play.string == "PAUSE":  # this is true if the simulation is running
            try:
                # noinspection PyTypeChecker
                x, y, timecount, reset, momentum, trace = simulation(p1s[0], p2s[0], p1, p2, momentum, trace_colour,
                                                                     timecount, energy, float(
                        scale), float(time_scale))  # calculates the new position of the marker
                xpos.append(x)  # Appends new data to lists so that they can be plotted
                ypos.append(y)
                times.append(timecount)

                time.sleep(0.00000000000001)
                traces.append(trace)  # keeps track of the visited position of the markers to leave a trace

            except IndexError:
                # noinspection PyUnboundLocalVariable
                play.check_click(window.screen, event,
                                 True)  # an IndexError will occur if there is no queue of particles so the pause button is automatically pressed
                break
        if scaling.up_arrow.state:
            scale = float(scale) + 1
            scaling.text.start_string = "10^" + str(scale) + "m"
        elif scaling.down_arrow.state:
            scale = float(scale) - 1
            scaling.text.start_string = "10^" + str(scale) + "m"

        if time_scaling.up_arrow.state:
            time_scale = float(time_scale) + 1
            time_scaling.text.start_string = "5*10^" + str(time_scale) + "s"
        elif time_scaling.down_arrow.state:
            time_scale = float(time_scale) - 1
            time_scaling.text.start_string = "5*10^" + str(time_scale) + "s"

        if clear.state:
            traces = []
            clearing = True

        if back_button.state:
            return None

        if graph.state:
            dataAnalysis.compare(
                record)  # the module dataAnalysis is called to output graphs using all previous data in the session

        if reset:
            timecount = 0  # all parameters are reset here such that the simulation can start again with a new particle
            record.append([xpos, ypos, times,
                           trace_colour])  # the record contains a list of these arguments for each simulation run
            xpos = []  # reset variables
            ypos = []
            times = []
            momentum = Vector(float(energy) * (10 ** 6) * 1.6 * (10 ** (-19)) / 3 / (10 ** 8) * (2 ** 0.5), 0)
            p1s = p1s[1::]  # the previous marker is deleted
            try:
                # noinspection PyUnboundLocalVariable
                play.check_click(window.screen, event, True)
            except AttributeError:
                play.state = 0
            trace_colour = randomcolor.RandomColor().generate(format_="rgb")[0][4:-2].split(
                ",")  # trace colour is re-randomised
            trace_colour = tuple(
                [int(i.lstrip()) if i != "" else 0 for i in trace_colour])

        window.screen.fill(WHITE)
        pygame.draw.rect(window.screen, LIGHTBLUE,
                         pygame.Rect(0, 0, window.screen.get_width(), window.screen.get_height()), width=5)
        text = guiClasses.big_font.render("INTERACTION SIMULATION:", True, RED, WHITE)
        textRect = text.get_rect()
        textRect.center = (253, 130)
        window.screen.blit(text, textRect)

        for t in traces:
            error_found = t.draw(window.screen)
            if error_found:
                break
        if error_found:
            error("Invalid position")
            return True

        clear.draw(window.screen)
        play.draw(window.screen)
        graph.draw(window.screen)
        back_button.draw(window.screen)
        scaling.draw(window.screen)
        time_scaling.draw(window.screen)

        gen_p1.draw(window.screen)
        gen_p2.draw(window.screen)

        for p in p1s:
            p.draw(window.screen)
        for p in p2s:
            p.draw(window.screen)

        pygame.display.update()
        clock.tick(120)

        if action:
            time.sleep(0.2)
        else:
            time.sleep(0.05)

        if clearing:
            clear.state = False


if __name__ == "__main__":
    while True:
        while True:  # first initialises home screen
            window.screen.fill(WHITE)
            pygame.draw.rect(window.screen, RED,
                             pygame.Rect(0, 0, window.screen.get_width(), window.screen.get_height()), width=5)
            option = display_menu()

            if option == "preexisting":  # for user choosing to use a pre-defined particle
                # Selects all Lepton objects and Hadron objects for optionsobj and selects their names for options
                optionsobj = ["null"] + [x for xs in [particleClasses.Lepton.generations[generation] for generation in
                                                      particleClasses.Lepton.generations] for x in xs] + [x for xs in [
                    particleClasses.Hadron.hadrons] for x in xs]
                options = ["Select Particle"] + [x._name for xs in
                                                 [particleClasses.Lepton.generations[generation] for generation in
                                                  particleClasses.Lepton.generations] for x in xs] + [x._name for xs in
                                                                                                      [
                                                                                                          particleClasses.Hadron.hadrons]
                                                                                                      for x in xs]
                tempobj = [optionsobj[0]]
                tempOpts = [options[0]]

                for i, o in enumerate(optionsobj[
                                      1::]):  # removes all objects with charge 0 (they are not affected by the electromagnetic force)
                    # noinspection PyProtectedMember,PyUnresolvedReferences
                    if o._charge != 0:
                        tempOpts.append(options[i + 1])
                        tempobj.append(o)
                optionsobj = tempobj
                options = tempOpts

                dropdown1 = [guiClasses.DropDown(PURPLE, [options[i]], 490, 180, 240, 40, i) for i in
                             range(len(options))]
                energy1 = guiClasses.WriteBox(170, 180, 150, 40, "Energy:", start_string="MeV")
                dropdown2 = [guiClasses.DropDown(LIGHTPINK, [options[i]], 750, 180, 240, 40, i) for i in
                             range(len(options))]

                # Calls function main_preexisting to allow user input
                p1, p2, energy, back = main_preexisting(dropdown1, dropdown2, energy1)
                if not back:
                    screen_blank(RED)
                    break

            elif option == "custom":  # user chooses to define their own particle
                mass1 = guiClasses.WriteBox(170, 180, 150, 40, "Mass:", start_string="MeV/c^")
                charge1 = guiClasses.WriteBox(170, 240, 150, 40, "Charge:", start_string="e")
                energy1 = guiClasses.WriteBox(170, 300, 150, 40, "Energy:", start_string="MeV")

                mass2 = guiClasses.WriteBox(600, 180, 150, 40, "Mass:", start_string="MeV/c^")
                charge2 = guiClasses.WriteBox(600, 240, 150, 40, "Charge:", start_string="e")

                p1, p2, energy, back = main_custom(mass1, charge1, energy1, mass2, charge2)  # calling the main_custom function

                if not back:
                    screen_blank()
                    break

        while True:  # the particle has now been picked and the next option screen is shown
            window.screen.fill(WHITE)
            pygame.draw.rect(window.screen, RED,
                             pygame.Rect(0, 0, window.screen.get_width(), window.screen.get_height()), width=5)
            option = display_sim_menu()  # displays options for simulation
            options = guiClasses.Button(TEAL, ["OPTIONS"], 70, window.screen.get_height() // 10 * 8, 120, 40)
            record = []

            if option == "interaction":  # particle to particle interaction
                error_called = main_interaction(p1, p2, energy, options, record)
                if error_called:
                    break

            elif option == "shower":  # particle shower simulation
                back_button = guiClasses.Button(TEAL, ["MENU"], 70, window.screen.get_height() // 10 * 8, 80, 40)
                energyBox = guiClasses.WriteBox(170, 300, 150, 40, "Energy:", start_string="MeV")
                filenameBox = guiClasses.WriteBox(170, 360, 150, 40, "Filename:", start_string=".txt")
                filename, shower_energy, back = get_energy(energyBox, filenameBox, back_button)
                if shower_energy is not None:
                    atmosphere.main_atmosphere(filename, float(
                        energy))  # calls main_atmosphere from module atmosphere to simulate the particle shower with
                    # the given user inputs
                if not back:
                    screen_blank(LIGHTORANGE)
                    break

            elif option == "back":
                break
