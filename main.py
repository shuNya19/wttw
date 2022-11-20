import pygame as pg
import methods
from variables import Variables


def run():
	pg.init()
	screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
	variables = Variables(screen)
	while True:
		methods.check_events(variables, screen)
		methods.game_events(variables, screen)
		screen.fill((0, 0, 0))
		methods.show(variables, screen)
		pg.display.flip()
	pg.quit()


run()
