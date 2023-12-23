import pygame
import random

white = (255, 255, 255)
black = (0, 0, 0)

cell_size = 40
left_margin = 50
upper_margin = 60

size = [left_margin + 30 * cell_size, upper_margin + 15 * cell_size]

pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Морской бой")

font_size = cell_size // 1.5
font = pygame.font.SysFont('Consolas', 30)


def draw_grid():
	for i in range(11):
		for j in range(11):
			pygame.draw.line(screen, black, (left_margin, upper_margin + i * cell_size),(left_margin + 10 * cell_size, upper_margin + i * cell_size), 1)


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
