import pygame as pg
import os


class Variables:
	def __init__(self, screen):
		self.to_remove_2 = "/\\:*?\"<>|"
		self.table_2 = {ord(char): '' for char in self.to_remove_2}
		self.to_remove = "\'"
		self.table = {ord(char): '' for char in self.to_remove}
		self.font_size = 40
		# Cooper Black
		self.font_name = 'Comic Sans MS'
		self.font = pg.font.SysFont(self.font_name, self.font_size)
		self.numbers = [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]
		self.count = 0
		self.step = 16
		self.pause = self.step * 5
		self.stopping = False
		self.img_width = 450
		self.img_height = 630
		self.game_event = 'start'
		self.input = 250
		self.font_color = (255, 255, 255)
		self.alpha = 255
		self.titles = []
		self.TXT_COLOR = (255, 255, 255)
		self.my_list = []
		if os.path.exists('data/my_list.txt'):
			with open('data/my_list.txt', 'r', encoding="utf-8") as f:
				for line in f:
					self.my_list.append(line[:-1])
		self.rolling_titles = ''
		self.sorted_titles = []
		self.durations = [i * 10 for i in range(4, 15)]
		self.aired_list = [x for x in range(1940, 2021, 5)]
		self.alert = False
		self.minis_row = screen.get_width() // 200
