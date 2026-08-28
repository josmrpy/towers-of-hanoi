import pygame as py
from sys import exit
from colorama import init, Fore, Back, Style

class Colors:
    BLUE = (0, 85, 255)
    DARK_BLUE = (0, 3, 182)
    WHITE = (255, 255, 255)
    BROWN = (254, 182, 114)
    GREEN = (181, 255, 217)
    BLACK = (0, 0, 0)

init()

print(fr"""{Fore.BLUE}
  _____                                          __                               _
 /__   \ ___ __      __ ___  _ __  ___    ___   / _|   /\  /\ __ _  _ __    ___  (_)
   / /\// _ \\ \ /\ / // _ \| '__|/ __|  / _ \ | |_   / /_/ // _` || '_ \  / _ \ | |
  / /  | (_) |\ V  V /|  __/| |   \__ \ | (_) ||  _| / __  /| (_| || | | || (_) || |
  \/    \___/  \_/\_/  \___||_|   |___/  \___/ |_|   \/ /_/  \__,_||_| |_| \___/ |_|
-------------------------------------------------------------------------------------
Version: 1.9.0
By: Jasiel{Fore.RESET}

Start by choosing a {Fore.BLUE}number of disks{Fore.RESET}, between {Style.BRIGHT}1{Style.RESET_ALL} and {Style.BRIGHT}20{Style.RESET_ALL}.""")
try:
	total = int(input('>>> '))
	if total < 1 or total > 20:
		raise ValueError
except:
	total = None
	print('\n# Please enter a VALID number!')

py.init()

# Screen dimensions
SCR_WIDTH = 900
SCR_HEIGHT = 800

# Screen display settings
screen = py.display.set_mode((SCR_WIDTH, SCR_HEIGHT))

py.display.set_caption('Towers of Hanoi')

# text and font management
MAIN_FONT = py.font.SysFont('comic sans', 32, True)
RESET_FONT = py.font.SysFont('snap itc', 25)

# total of disks
DISK_TOTAL = total or 5

MIN_MOVES = 2 ** DISK_TOTAL - 1

# Tower, disk and reset parameters
TOWER_HEIGHT = 350
DISK_SIZE = TOWER_HEIGHT // (DISK_TOTAL + 3)
TOWER_WIDTH = DISK_SIZE // 2

DISK_MARGIN = DISK_SIZE // 10 + 3

RESET_WIDTH = 110
RESET_HEIGHT = 60
RESET_OFFSET = 10
RESET_X = SCR_WIDTH - RESET_WIDTH - RESET_OFFSET

# positioning and calculating towers
TOWER_OFFSET = 50

TOWER_BASE = SCR_HEIGHT - TOWER_HEIGHT

TOWER2_X = (SCR_WIDTH - TOWER_WIDTH) // 2
TOWER1_X = TOWER2_X // 2 - TOWER_OFFSET
TOWER3_X = TOWER2_X * 1.5 + TOWER_OFFSET
TOWER_POSITIONS = [TOWER1_X, TOWER2_X, TOWER3_X]

# Initialize disks on the first tower
towers = [[i for i in range(DISK_TOTAL, 0, -1)],[],[]]
placeholder = []

# Game objects

def drawPlaceholder(stack: list, tower_position):
	disk_size_factor = DISK_SIZE * stack
	disk_X = tower_position + (TOWER_WIDTH - disk_size_factor) // 2

	disk = py.draw.rect(screen, Colors.BLUE, (disk_X, TOWER_BASE // 2, disk_size_factor, DISK_SIZE), 0, DISK_MARGIN)
	py.draw.rect(screen, Colors.DARK_BLUE, ((disk.topleft), (disk.size)), DISK_MARGIN, DISK_MARGIN)

def drawDisks(stack: list, tower_position):
	distance_factor = 0

	for i in stack:
		disk_size_factor = DISK_SIZE * i
		disk_X = tower_position + (TOWER_WIDTH - disk_size_factor) // 2
		disk_Y = SCR_HEIGHT - DISK_SIZE - distance_factor

		disk = py.draw.rect(screen, Colors.BLUE, (disk_X, disk_Y, disk_size_factor, DISK_SIZE), 0, DISK_MARGIN)
		py.draw.rect(screen, Colors.DARK_BLUE, ((disk.topleft), (disk.size)), DISK_MARGIN, DISK_MARGIN)
		distance_factor += DISK_SIZE + 1

# Function for positioning the disks
def takeDiskFromTower(index: int):
	stack: list = towers[index]
	if not stack:
		return True

	top_disk = stack[-1]
	placeholder.extend([top_disk, index])
	stack.pop()
	return False

def placeDiskInTower(index: int):
	stack: list = towers[index]
	disk, idx = placeholder

	top_disk = min(stack or [0])

	if top_disk == 0 or top_disk > disk:
		stack.append(disk)
		placeholder.clear()
	else:
		return False, 0
	return True, 0 if idx == index else 1

# functions for checking on events
MOUSE_OFFSET = 90

def clickedTower(mouseX, mouseY):
	def is_touching(tower):
		isX = (mouseX >= tower - MOUSE_OFFSET and mouseX <= tower + TOWER_WIDTH + MOUSE_OFFSET)
		isY = (mouseY >= TOWER_BASE and mouseY <= TOWER_BASE + TOWER_HEIGHT)
		return isX and isY

	check = lambda tower, num: (is_touching(tower) and str(num))
	return check(TOWER1_X, 0) or check(TOWER2_X, 1) or check(TOWER3_X, 2) or None

def onResetClicked(mouseX, mouseY):
	isX = (mouseX >= RESET_X and mouseX <= RESET_X + RESET_WIDTH)
	isY = (mouseY >= RESET_OFFSET and mouseY <= RESET_OFFSET + RESET_HEIGHT)
	isClicking = isX and isY

	if not isClicking:
		return isTake, move_count

	if any(placeholder):
		towers[0].append(placeholder[0])
		placeholder.clear()

	if any(towers[i] for i in range(1, 3)):
		for i in range(1, 3):
			towers[0].extend(towers[i])
			towers[i].clear()

	towers[0].sort(reverse=True)
	return True, 0

# As the name suggests, this is the main loop function
move_count = 0

def main():
	screen.fill(Colors.WHITE)

	# Reset button background
	py.draw.rect(screen, Colors.BLUE, (RESET_X, RESET_OFFSET, RESET_WIDTH, RESET_HEIGHT), 0, 11)

	# Render minimum moves text
	min_moves_text = MAIN_FONT.render(f'Best: {MIN_MOVES}', True, Colors.BLACK)
	min_moves_rect = min_moves_text.get_rect()
	min_moves_rect.topleft = (20, 10)

	# Render move count text
	move_count_text = MAIN_FONT.render('Move count: ' + str(move_count), True, Colors.BLACK)
	move_count_rect = move_count_text.get_rect()
	move_count_rect.topleft = min_moves_rect.bottomleft

	# Render reset button Text
	reset_button = RESET_FONT.render('Reset', True, Colors.WHITE)
	reset_rect = reset_button.get_rect()
	reset_rect.center = (RESET_X + RESET_WIDTH // 2, RESET_OFFSET + RESET_HEIGHT // 2)

	screen.blit(move_count_text, move_count_rect)
	screen.blit(min_moves_text, min_moves_rect)
	screen.blit(reset_button, reset_rect)

	for i in range(3):
		py.draw.rect(screen, Colors.GREEN, (TOWER_POSITIONS[i] - MOUSE_OFFSET, TOWER_BASE, TOWER_WIDTH + MOUSE_OFFSET * 2, TOWER_HEIGHT))
		py.draw.rect(screen, Colors.BROWN, (TOWER_POSITIONS[i], TOWER_BASE, TOWER_WIDTH, TOWER_HEIGHT))

		drawDisks(towers[i], TOWER_POSITIONS[i])

	placeholder and drawPlaceholder(placeholder[0], TOWER_POSITIONS[placeholder[1]])

	for i in range(1, 3):
		if len(towers[i]) == DISK_TOTAL:
			# Render solved achievement text
			score1, score2 = "That's a perfect score!",'You achieved to solve it!'
			solved_state = move_count == MIN_MOVES and score1 or score2

			solved_text = MAIN_FONT.render(solved_state, True, Colors.BLUE)
			solved_rect = solved_text.get_rect()
			solved_rect.center = (SCR_WIDTH // 2, TOWER_BASE // 2.8)

			screen.blit(solved_text, solved_rect)

	py.display.flip()

isTake = True
isRunning = True
while isRunning:
	for event in py.event.get():
		if event.type == py.QUIT:
			isRunning = False
		elif event.type == py.MOUSEBUTTONDOWN:
			mouseX, mouseY = py.mouse.get_pos()

			clicked_tower = int(clickedTower(mouseX, mouseY) or -1)
			if clicked_tower != -1:
				if isTake:
					isTake = takeDiskFromTower(clicked_tower)
				else:
					isTake, move = placeDiskInTower(clicked_tower)
					move_count += move
			else:
				isTake, move_count = onResetClicked(mouseX, mouseY)
	main( )

py.quit()
exit()
