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


def draw_grid():
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
	while not game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_over = True

		draw_grid()
		pygame.display.update()


main()
pygame.Quit()
