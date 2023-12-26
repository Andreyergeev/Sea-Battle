import pygame
import random
import copy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

cell_size = 40
left_margin = 100
upper_margin = 60

size = (left_margin + 30 * cell_size, upper_margin + 15 * cell_size)
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Морской бой")

font_size = int(cell_size / 1.5)

font = pygame.font.SysFont('Consolas', font_size)
ai_available_to_fire_set = {(a, b) for a in range(1, 11) for b in range(1, 11)}
around_last_ai_hit_set = set()
hit_cells = set()
dotted_set = set()
dotted_set_for_ai_not_to_shoot = set()
hit_cells_for_ai_not_to_shoot = set()
last_hits_list = []
destroyed_ships_list = []


class Ships:
	def __init__(self):
		self.available_cells = {(a, b) for a in range(1, 11) for b in range(1, 11)}
		self.ships_set = set()
		self.ships = self.populate_grid()

	def create_start_cell(self, available_cells):
		x_or_y = random.randint(0, 1) # строим горизонтальный или вертикальный корабль, 0 - горизонт., 1 - вертикально
		str_rev = random.choice((-1, 1)) # строим корабль двигаясь влево или право, вверх или вниз
		x, y = random.choice(tuple(available_cells))
		return x, y, x_or_y, str_rev

	def create_ship(self, number_of_cells, available_cells):
		ship_coordinates = []
		x, y, x_or_y, str_rev = self.create_start_cell(available_cells)
		for _ in range(number_of_cells):
			ship_coordinates.append((x, y))
			if not x_or_y: # если корабль выходит за рамки поля
				str_rev, x = self.add_cell_to_ship(x, str_rev, x_or_y, ship_coordinates)
			else:
				str_rev, y = self.add_cell_to_ship(y, str_rev, x_or_y, ship_coordinates)
		if self.is_ship_valid(ship_coordinates):
			return ship_coordinates
		return self.create_ship(number_of_cells, available_cells)

	def add_cell_to_ship(self, coordinate, str_rev, x_or_y, ship_coordinates):
		if (coordinate <= 1 and str_rev == -1) or (coordinate >= 10 and str_rev == 1):
			str_rev *= -1
			return str_rev, ship_coordinates[0][x_or_y] + str_rev
		else:
			return str_rev, ship_coordinates[-1][x_or_y] + str_rev

	def is_ship_valid(self, new_ship):  # правильно ли построен корабль
		ship = set(new_ship)
		return ship.issubset(self.available_cells)

	def add_new_ship_to_set(self, new_ship):  # добавляем корабль во множество координат кораблей
		for element in new_ship:
			self.ships_set.add(element)

	def deleting_cells(self, new_ship): # удаляем из списка все клетки вокруг корабля
		for element in new_ship:
			for k in range(-1, 2):
				for m in range(-1, 2):
					if 0 < (element[0] + k) < 11 and 0 < (element[1] + m) < 11:
						self.available_cells.discard((element[0] + k, element[1] + m))

	def populate_grid(self): # список кораблей, с разными палубами
		ships_coordinates_list = []
		for number_of_cells in range(4, 0, -1):
			for _ in range(5 - number_of_cells):
				new_ship = self.create_ship(number_of_cells, self.available_cells)
				ships_coordinates_list.append(new_ship)
				self.add_new_ship_to_set(new_ship)
				self.deleting_cells(new_ship)
		return ships_coordinates_list


ai = Ships() # создали компьютер
person = Ships() # создали игрока
ai_ships_working = copy.deepcopy(ai.ships)
person_ships_working = copy.deepcopy(person.ships)


def draw_ships(ships_coordinates_list):  # рисуем корабли
	for element in ships_coordinates_list:
		ship = sorted(element)
		x_start = ship[0][0]
		y_start = ship[0][1]
		# строим вертикальные корабли
		if len(ship) > 1 and ship[0][0] == ship[1][0]:
			ship_width = cell_size
			ship_height = cell_size * len(ship)
		# одноклеточные и горизонтальные
		else:
			ship_width = cell_size * len(ship)
			ship_height = cell_size
		x = cell_size * (x_start - 1) + left_margin
		y = cell_size * (y_start - 1) + upper_margin
		if ships_coordinates_list == person.ships:
			x += 15 * cell_size
		pygame.draw.rect(screen, BLACK, ((x, y), (ship_width, ship_height)), width=cell_size // 10)


class Grid:
	def __init__(self, title, offset):
		self.title = title
		self.offset = offset
		self.draw_grid()
		self.sign_grids()
		self.add_nums_letters_to_grid()

	def draw_grid(self):
		for i in range(11):
			# горизонтальная линия для 1 поля
			pygame.draw.line(screen, BLACK, (left_margin + self.offset, upper_margin + i * cell_size),
			                 (left_margin + 10 * cell_size + self.offset, upper_margin + i * cell_size), 1)
			# вертикальная линия для 1 поля
			pygame.draw.line(screen, BLACK, (left_margin + i * cell_size + self.offset, upper_margin),
			                 (left_margin + i * cell_size + self.offset, upper_margin + 10 * cell_size), 1)

	def add_nums_letters_to_grid(self):
		for i in range(10):
			num_ver = font.render(str(i + 1), True, BLACK)
			letters_hor = font.render(LETTERS[i], True, BLACK)
			num_ver_width = num_ver.get_width()
			num_ver_height = num_ver.get_height()
			letters_hor_width = letters_hor.get_width()

			# горизонтальная линия для 2 поля
			screen.blit(num_ver, (left_margin - (cell_size // 2 + num_ver_width // 2) + self.offset,
			                      upper_margin + i * cell_size + (cell_size // 2 - num_ver_height // 2)))
			# вертикальная линия для 2 поля
			screen.blit(letters_hor, (left_margin + i * cell_size + (cell_size //
			                                                         2 - letters_hor_width // 2) + self.offset,
			                          upper_margin + 10 * cell_size))

	def sign_grids(self):
		player = font.render(self.title, True, BLACK)
		sign_width = player.get_width()
		screen.blit(player, (left_margin + 5 * cell_size - sign_width //
		                     2 + self.offset, upper_margin - cell_size // 2 - font_size))


def ai_shoots(set_to_shoot_from):
	pygame.time.delay(500)
	ai_fired_cell = random.choice(tuple(set_to_shoot_from))
	ai_available_to_fire_set.discard(ai_fired_cell)
	return check_hit_or_miss(ai_fired_cell, person_ships_working, True)


def check_hit_or_miss(fired_cell, opponents_ships_list, ai_turn, diagonal_only=True):
	for element in opponents_ships_list:
		if fired_cell in element:
			update_dotted_and_hit_sets(
				fired_cell, ai_turn, diagonal_only=True)
			ind = opponents_ships_list.index(element)

			if len(element) == 1:
				update_dotted_and_hit_sets(
					fired_cell, ai_turn, diagonal_only=False)

			element.remove(fired_cell)

			if ai_turn:
				last_hits_list.append(fired_cell)
				person.ships_set.discard(fired_cell)
				update_around_last_ai_hit(fired_cell)
			else:
				ai.ships_set.discard(fired_cell)

			if not element:
				draw_destroyed_ships(ind, opponents_ships_list, ai_turn)
				if ai_turn:
					last_hits_list.clear()
					around_last_ai_hit_set.clear()
				else:
					destroyed_ships_list.append(ai.ships[ind])

			return True
	put_dot_on_missed_cell(fired_cell, ai_turn)
	if ai_turn:
		update_around_last_ai_hit(fired_cell, False)
	return False


def put_dot_on_missed_cell(fired_cell, ai_turn = False):
	if not ai_turn:
		dotted_set.add(fired_cell)
	else:
		dotted_set.add((fired_cell[0] + 15, fired_cell[1]))
		dotted_set_for_ai_not_to_shoot.add(fired_cell)


def draw_destroyed_ships(ind, opponents_ships_list, ai_turn, diagonal_only = False):
	if opponents_ships_list == ai_ships_working:
		ships_list = ai.ships
	elif opponents_ships_list == person_ships_working:
		ships_list = person.ships
	ship = sorted(ships_list[ind])
	for i in range(-1, 1):
		update_dotted_and_hit_sets(ship[i], ai_turn, diagonal_only)


def update_around_last_ai_hit(fired_cell, ai_hits = True):
	global around_last_ai_hit_set, ai_available_to_fire_set
	if ai_hits and fired_cell in around_last_ai_hit_set:
		around_last_ai_hit_set = ai_hits_twice()

	elif ai_hits and fired_cell not in around_last_ai_hit_set:
		ai_first_hit(fired_cell)

	elif not ai_hits:
		around_last_ai_hit_set.discard(fired_cell)

	around_last_ai_hit_set -= dotted_set_for_ai_not_to_shoot
	around_last_ai_hit_set -= hit_cells_for_ai_not_to_shoot
	ai_available_to_fire_set -= around_last_ai_hit_set
	ai_available_to_fire_set -= dotted_set_for_ai_not_to_shoot


def ai_first_hit(fired_cell):
	xhit, yhit = fired_cell
	if 1 < xhit:
		around_last_ai_hit_set.add((xhit - 1, yhit))
	if xhit < 10:
		around_last_ai_hit_set.add((xhit + 1, yhit))
	if 1 < yhit:
		around_last_ai_hit_set.add((xhit, yhit - 1))
	if yhit < 10:
		around_last_ai_hit_set.add((xhit, yhit + 1))


def ai_hits_twice():
	last_hits_list.sort()
	new_around_last_hit_set = set()
	for i in range(len(last_hits_list) - 1):
		x1 = last_hits_list[i][0]
		x2 = last_hits_list[i + 1][0]
		y1 = last_hits_list[i][1]
		y2 = last_hits_list[i + 1][1]

		if x1 == x2:
			if y1 > 1:
				new_around_last_hit_set.add((x1, y1 - 1))
			if y2 < 10:
				new_around_last_hit_set.add((x1, y2 + 1))

		elif y1 == y2:
			if 1 < x1:
				new_around_last_hit_set.add((x1 - 1, y1))
			if x2 < 10:
				new_around_last_hit_set.add((x2 + 1, y1))

	return new_around_last_hit_set


def update_dotted_and_hit_sets(fired_cell, ai_turn, diagonal_only = True):
	global dotted_set
	x, y = fired_cell
	a, b = 0, 11
	if ai_turn:
		x += 15
		a += 15
		b += 15
		hit_cells_for_ai_not_to_shoot.add(fired_cell)
	hit_cells.add((x, y))
	for i in range(-1, 2):
		for j in range(-1, 2):
			if diagonal_only:
				if i != 0 and j != 0 and a < x + i < b and 0 < y + j < 11:
					dotted_set.add((x + i, y + j))
					if ai_turn:
						dotted_set_for_ai_not_to_shoot.add(
							(fired_cell[0] + i, y + j))
			else:
				if a < x + i < b and 0 < y + j < 11:
					dotted_set.add((x + i, y + j))
					if ai_turn:
						dotted_set_for_ai_not_to_shoot.add((
							fired_cell[0] + i, y + j))
	dotted_set -= hit_cells


def draw_from_dotted_set(dotted_set):
	for elem in dotted_set:
		pygame.draw.circle(screen, BLACK, (cell_size * (
				elem[0] - 0.5) + left_margin, cell_size * (elem[1] - 0.5) + upper_margin), cell_size // 6)


def draw_hit_cells(hit_cells):
	for block in hit_cells:
		x1 = cell_size * (block[0] - 1) + left_margin
		y1 = cell_size * (block[1] - 1) + upper_margin
		pygame.draw.line(screen, BLACK, (x1, y1),
		                 (x1 + cell_size, y1 + cell_size), cell_size // 6)
		pygame.draw.line(screen, BLACK, (x1, y1 + cell_size),
		                 (x1 + cell_size, y1), cell_size // 6)


def main():
	game_over = False
	ai_turn = False

	screen.fill(WHITE)
	ai_grid = Grid("Компьютер", 0)
	person_grid = Grid("Человек", 15 * cell_size)
	# draw_ships(computer.ships)
	draw_ships(person.ships)
	pygame.display.update()

	while not game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_over = True
			elif not ai_turn and event.type == pygame.MOUSEBUTTONDOWN:
				x, y = event.pos
				if (left_margin <= x <= left_margin + 10 * cell_size) and (
						upper_margin <= y <= upper_margin + 10 * cell_size):
					fired_cell = ((x - left_margin) // cell_size + 1,
					               (y - upper_margin) // cell_size + 1)
				ai_turn = not check_hit_or_miss(
					fired_cell, ai_ships_working, ai_turn)

		if ai_turn:
			if around_last_ai_hit_set:
				ai_turn = ai_shoots(around_last_ai_hit_set)
			else:
				ai_turn = ai_shoots(ai_available_to_fire_set)


		draw_from_dotted_set(dotted_set)
		draw_hit_cells(hit_cells)
		draw_ships(destroyed_ships_list)
		pygame.display.update()

main()
pygame.quit()