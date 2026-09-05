import pygame as py
from sys import exit
from colorama import init, Fore, Style

init()
py.init()

clock = py.Clock()


class Color:
    BLUE = (0, 85, 255)
    DARK_BLUE = (0, 3, 182)
    WHITE = (255, 255, 255)
    BROWN = (254, 182, 114)
    GREEN = (181, 255, 217)
    BLACK = (0, 0, 0)


def decor(text: str, method=Fore.LIGHTBLUE_EX) -> str:
    chain = [method, text, Style.RESET_ALL]
    return "".join(chain)


# Game Version/intro :::
print(decor(r"""
   _____                              ___    _____             _
  |_   _|___ _ _ _ ___ ___ ___    ___|  _|  |  |  |___ ___ ___|_|
    | | | . | | | | -_|  _|_ -|  | . |  _|  |     | .'|   | . | |
    |_| |___|_____|___|_| |___|  |___|_|    |__|__|__,|_|_|___|_|
  ---------------------------------------------------------------
Version: 2.1.3
By: Josimar M. (@josmr.py)
"""))

lines = [decor("number of disks"), decor("1", Style.BRIGHT), decor("13", Style.BRIGHT)]

print(f"Start by choosing a {lines[0]}, between {lines[1]} and {lines[2]}.")

# Disk input
total = input(">>> ")

try:
    total = int(total)
    if total < 1 or total > 13:
        raise ValueError
except:
    total = 5
    print()
    print(decor("[Err]", Fore.RED), "Please enter a VALID number!")

# Screen dimensions
SCR_WIDTH = 800
SCR_HEIGHT = 700

# Screen display settings
screen = py.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
py.display.set_caption("Towers of Hanoi")

# total of disks
DISK_TOTAL = total
MIN_MOVES = 2**DISK_TOTAL - 1

# Tower, disk and reset parameters
TOWER_HEIGHT = int(
    SCR_HEIGHT // (700 / 350)
)  # 700: original screen height, 350: original rect height

DISK_SIZE = TOWER_HEIGHT // (DISK_TOTAL + 3)
TOWER_WIDTH = DISK_SIZE // 2

DISK_RADIUS = int(
    DISK_SIZE // (43 / 7)
)  # 43: original disk size, 7: original corner radius
BORDER_WIDTH = DISK_SIZE // 10 + 3

RESET_WIDTH = int(
    SCR_WIDTH // (800 / 110)
)  # 800: original screen width, 110: original rect width
RESET_HEIGHT = int(
    SCR_HEIGHT // (700 / 60)
)  # 700: original screen height, 60: original rect height

RESET_OFFSET = 10
RESET_X = SCR_WIDTH - RESET_WIDTH - RESET_OFFSET
RESET_RECT = py.Rect(RESET_X, RESET_OFFSET, RESET_WIDTH, RESET_HEIGHT)

# positioning and calculating towers
MOUSE_OFFSET = 90
TOWER_OFFSET = 50

TOWER_CENTER = (SCR_WIDTH - TOWER_WIDTH) // 2
TOWER_BASE = SCR_HEIGHT - TOWER_HEIGHT

TOWER1_X = TOWER_CENTER // 2 - TOWER_OFFSET
TOWER3_X = TOWER_CENTER * 1.5 + TOWER_OFFSET

TOWER_POSITIONS = list(
    py.Rect(x, TOWER_BASE, TOWER_WIDTH, TOWER_HEIGHT)
    for x in [TOWER1_X, TOWER_CENTER, TOWER3_X]
)
TRIGGER_POSITIONS = list(
    rect.copy().inflate(MOUSE_OFFSET * 2, 0) for rect in TOWER_POSITIONS
)

# text and font management
MAIN_FONT = py.font.SysFont("comic sans", 32, True)
RESET_FONT = py.font.SysFont("Arial", 25, True)

towers = [[i for i in range(DISK_TOTAL, 0, -1)], [], []]
placeholder = []


# main functions for drawing or rendering disks and text
def render_Text(
    font: py.font.Font,
    text: str,
    surface_position: tuple,
    color: tuple = Color.BLACK,
    align: str = "topleft",
    get_rect: bool = False,
    antialias: bool = True,
) -> py.Rect | None:

    surface = font.render(text, antialias, color)
    surface_rect = surface.get_rect()
    setattr(surface_rect, align, surface_position)

    screen.blit(surface, surface_rect)

    if get_rect:
        return surface_rect


def drawPlaceholder(stack: int, tower_position: py.Rect):
    disk_size_factor = DISK_SIZE * stack
    disk_X = tower_position.left + (TOWER_WIDTH - disk_size_factor) // 2

    disk = py.draw.rect(
        screen,
        Color.BLUE,
        (disk_X, TOWER_BASE // 2, disk_size_factor, DISK_SIZE),
        0,
        DISK_RADIUS,
    )
    py.draw.rect(screen, Color.DARK_BLUE, disk, BORDER_WIDTH, DISK_RADIUS)


""" TODO:
Cambiar el uso de la posicion x de la torre para calcular la distancia de los discos por un rect acomodado en el centro basado en los valores de la torre
ajustar el tamaño en base a la torre de arriba principal para que quizas se pueda ajustar con la funcion "inflate" la cual permite aumentar el tamaño de los lados,
    manteniendo la posicion
"""


def drawDisks(stack: list, tower_position: py.Rect | int):
    fact_values = range(DISK_SIZE, (DISK_SIZE + 1) * len(stack), DISK_SIZE + 1)
    for i, distance_factor in zip(stack, fact_values):
        disk_size_factor = DISK_SIZE * i
        disk_X = tower_position + (TOWER_WIDTH - disk_size_factor) // 2
        disk_Y = SCR_HEIGHT - distance_factor

        disk = py.draw.rect(
            screen,
            Color.BLUE,
            (disk_X, disk_Y, disk_size_factor, DISK_SIZE),
            0,
            DISK_RADIUS,
        )
        py.draw.rect(screen, Color.DARK_BLUE, disk, BORDER_WIDTH, DISK_RADIUS)


# Function for positioning the disks
def takeDiskFromTower(index: int) -> bool:
    stack: list = towers[index]

    if not stack:
        return True

    top_disk = stack[-1]
    placeholder.extend([top_disk, index])
    stack.pop()
    return False


def placeDiskInTower(index: int) -> tuple[bool, int]:
    stack: list = towers[index]
    disk, idx = placeholder

    top_disk = 0 if not stack else stack[-1]

    if top_disk == 0 or top_disk > disk:
        stack.append(disk)
        placeholder.clear()
    else:
        return False, 0
    return True, 0 if idx == index else 1


# As the name suggests, this is the main loop function
move_count = 0


def main():
    screen.fill(Color.WHITE)  #

    reset_bg = py.draw.rect(screen, Color.BLUE, RESET_RECT, 0, 11)

    min_moves_text = render_Text(
        MAIN_FONT, f"Best: {MIN_MOVES}", (20, 10), get_rect=True
    )
    if min_moves_text is not None:
        render_Text(MAIN_FONT, f"Move count: {move_count}", min_moves_text.bottomleft)
    render_Text(RESET_FONT, "Reset", reset_bg.center, Color.WHITE, "center")

    for i in range(3):
        py.draw.rect(screen, Color.GREEN, TRIGGER_POSITIONS[i])
        py.draw.rect(screen, Color.BROWN, TOWER_POSITIONS[i])

        drawDisks(towers[i], TOWER_POSITIONS[i].left)

    if placeholder:
        drawPlaceholder(placeholder[0], TOWER_POSITIONS[placeholder[1]])

    if any(len(towers[i]) == DISK_TOTAL for i in range(1, 3)):
        w1, w2 = "That's a perfect score!", "You achieved to solve it!"
        solved_state = move_count == MIN_MOVES and w1 or w2
        render_Text(
            MAIN_FONT,
            solved_state,
            (SCR_WIDTH // 2, TOWER_BASE // 2),
            Color.BLUE,
            "center",
        )

    py.display.flip()  #


isHolding = True
isRunning = True
while isRunning:
    for event in py.event.get():
        if event.type == py.QUIT:  # Quit the game
            isRunning = False
        elif event.type == py.MOUSEBUTTONDOWN:  # Clicking on something
            mouseX, mouseY = py.mouse.get_pos()

            clicked_tower = -1
            for i in range(3):
                left = TOWER_POSITIONS[i].left - MOUSE_OFFSET
                width = TOWER_WIDTH + MOUSE_OFFSET * 2

                trigger = py.Rect(left, TOWER_BASE, width, TOWER_HEIGHT)

                if trigger.collidepoint(mouseX, mouseY):
                    clicked_tower = i

            if clicked_tower != -1:
                if isHolding:
                    isHolding = takeDiskFromTower(clicked_tower)
                else:
                    isHolding, move = placeDiskInTower(clicked_tower)
                    move_count += move
            elif RESET_RECT.collidepoint(mouseX, mouseY):
                if placeholder:
                    towers[0].append(placeholder[0])
                    placeholder.clear()

                if any(towers[i] for i in range(1, 3)):
                    for i in range(1, 3):
                        towers[0].extend(towers[i])
                        towers[i].clear()

                towers[0].sort(reverse=True)
                isHolding, move_count = True, 0
    main()
    clock.tick(30)

py.quit()
exit()
