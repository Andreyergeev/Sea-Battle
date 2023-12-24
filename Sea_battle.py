import pygame
import random

white = (255, 255, 255)
black = (0, 0, 0)

cell_size = 40
left_margin = 100
upper_margin = 60

size = [left_margin + 30 * cell_size, upper_margin + 15 * cell_size]

pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Морской бой")

font_size = int(cell_size / 1.5)
font = pygame.font.SysFont('Consolas', font_size)

class Ship:
	def __init__(self):
		self.available_blocks = set((a, b) for a in range(1, 11) for b in range(1, 11))
		self.ships_set = set()
		self.ships = self.populate_grid()

	def create_start_block(self, available_blocks):
		x_or_y = random.randint(0, 1)  # строим горизонтальный или вертикальный корабль, 0 - горизонт., 1 - вертикально
		str_rev = random.choice((1, -1))  # строим корабль двигаясь влево или право, вверх или вниз
		x, y = random.choice(tuple(available_blocks))
		return x, y, x_or_y, str_rev

	def create_ship(self, number_of_blocks, available_blocks):
		ship_coordinates = []
		x, y, x_or_y, str_rev = self.create_start_block(available_blocks)
		for _ in range(number_of_blocks):
			ship_coordinates.append((x, y))
			if not x_or_y:  # если корабль выходит за рамки поля
				str_rev, x = self.add_block_to_ship(x, str_rev, x_or_y, ship_coordinates)
			else:
				str_rev, y = self.add_block_to_ship(y, str_rev, x_or_y, ship_coordinates)
		if self.is_ship_valid(ship_coordinates):
			return ship_coordinates
		return self.create_ship(number_of_blocks, available_blocks)

	def add_block_to_ship(self, coordinate, str_rev, x_or_y, ship_coordinates):
		if (coordinate <= 1 and str_rev == -1) or (coordinate >= 10 and str_rev == 1):
			str_rev *= -1
			return str_rev, ship_coordinates[0][x_or_y] + str_rev
		else:
			return str_rev, ship_coordinates[-1][x_or_y] + str_rev

	def is_ship_valid(self, new_ship):  # правильно ли построен корабль
		ship = set(new_ship)
		return ship.issubset(self.available_blocks)

	def add_new_ship_to_set(self, new_ship):  # добавляем корабль во множество координат кораблей
		for element in new_ship:
			self.ships_set.add(element)

	def deleting_cells(self, new_ship):# удаляем из списка все клетки вокруг корабля
		for element in new_ship:
			for k in range(1, 2):
				for m in range(1, 2):
					if 0 < element[0] + k < 11 and 0 < element[1] + m < 11:
						self.available_blocks.discard((element[0] + k, element[1] + m))

	def populate_grid(self): # список кораблей, с разными палубами
		ships_coordinates_list = []
		for number_of_blocks in range(4, 0, -1):
			for _ in range(5 - number_of_blocks):
				new_ship = self.create_ship(number_of_blocks, self.available_blocks)
				ships_coordinates_list.append(new_ship)
				self.add_new_ship_to_set(new_ship)
				self.deleting_cells(new_ship)
		return ships_coordinates_list

ai = Ship()  # создали компьютер
person = Ship()  # создали человека

def draw_ships (ships_coordinates_list): # рисуем корабли
	for element in ships_coordinates_list:
		ship = sorted(element)
		x_start = ship[0][0]
		y_start = ship[0][1]
		# строим вертикальные корабли
		if len(ship) > 1 and ship[0][0] == ship[1][0]:
			ship_width = cell_size
			ship_height = cell_size * len(ship)
		else:
			ship_width = cell_size * len(ship)
			ship_height = cell_size
		x = cell_size * (x_start - 1) + left_margin
		y = cell_size * (y_start - 1) + upper_margin
		if ships_coordinates_list == person.ships:
			x += 15 * cell_size
		pygame.draw.rect(screen, black, ((x, y), (ship_width, ship_height)), width=cell_size // 10)

def draw_grid(): # рисуем поле
	letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
	for i in range(11):
		for j in range(11):
			# горизонтальная линия для 1 поля
			pygame.draw.line(screen, black, (left_margin, upper_margin + i * cell_size),
			                 (left_margin + 10 * cell_size, upper_margin + i * cell_size), 1)
			# вертикальная линия для 1 поля
			pygame.draw.line(screen, black, (left_margin + j * cell_size, upper_margin),
			                 (left_margin + j * cell_size, upper_margin + 10 * cell_size), 1)
			# горизонтальная линия для 2 поля
			pygame.draw.line(screen, black, (left_margin + 15 * cell_size, upper_margin + i * cell_size),
			                 (left_margin + 25 * cell_size, upper_margin + i * cell_size), 1)
			# вертикальная линия для 2 поля
			pygame.draw.line(screen, black, (left_margin + j * cell_size + 15 * cell_size, upper_margin),
			                 (left_margin + j * cell_size + 15 * cell_size, upper_margin + 10 * cell_size), 1)

		if i < 10:
			numbers = font.render(str(i + 1), True, black)
			letters_hor = font.render(letters[i], True, black)

			numbers_vert = numbers.get_width()
			numbers_high = numbers.get_height()
			letters_vert = letters_hor.get_width()

			# вертикальные цифры на 1 поле
			screen.blit(numbers, (left_margin - (cell_size // 2 + numbers_vert // 2),
			                      upper_margin + i * cell_size + (cell_size // 2 - numbers_high // 2)))
			# горизонтальные буквы на 1 поле
			screen.blit(letters_hor, (left_margin + i * cell_size + (cell_size // 2 - letters_vert // 2),
			                          upper_margin - cell_size))

			# вертикальные цифры на 2 поле
			screen.blit(numbers, (left_margin - (cell_size // 2 + numbers_vert // 2) + 15 * cell_size,
			                      upper_margin + i * cell_size + (cell_size // 2 - numbers_high // 2)))
			# горизонтальные буквы на 2 поле
			screen.blit(letters_hor, (left_margin + i * cell_size + (cell_size // 2 - letters_vert // 2) + 15*cell_size,
			                          upper_margin - cell_size))



def main():
	game_over = False
	screen.fill(white)
	draw_grid()
	draw_ships(ai.ships)
	draw_ships(person.ships)
	pygame.display.update()
	
	while not game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_over = True





main()
pygame.quit()
