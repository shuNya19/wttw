import pygame as pg
from pandas import read_csv
from sys import exit
from random import choice
from math import isnan


def check_events(variables, screen):
	for event in pg.event.get():
		if event.type == pg.QUIT:
			exit()
		if event.type == pg.KEYDOWN:
			check_keydown(variables, event, screen)
		if event.type == pg.MOUSEBUTTONDOWN:
			check_mouse_down(variables, event, screen)
		if event.type == pg.MOUSEBUTTONUP:
			check_mouse_up(variables, event)


def game_events(variables, screen):
	if variables.game_event == 'rolling':
		if variables.stopping:
			if variables.count == variables.step * 10:
				if variables.step != 2:
					variables.step -= 1
					variables.count = 0
				else:
					variables.random_rec = choice(variables.sorted_titles)
					while variables.random_rec[0].right > screen.get_width() // 2:
						variables.random_rec = choice(variables.sorted_titles)
					variables.step = 1
			if variables.step == 1:
				if variables.random_rec[0].centerx == screen.get_width() // 2:
					variables.step = 0
					variables.stopping = False
					variables.game_event = 'vanishing'
			variables.count += 1
		for i in variables.sorted_titles:
			if screen.get_width() >= i[0].left:
				i[0].left += variables.step
				random_rect = choice(variables.sorted_titles)
			if variables.pause + variables.step > i[0].left >= variables.pause:
				while screen.get_width() >= random_rect[0].left:
					random_rect = choice(variables.sorted_titles)
				random_rect[0].left = -(random_rect[0].width // variables.step + 1) * variables.step

	if variables.game_event == 'vanishing':
		for i in variables.rects:
			if screen.get_width() >= i[0].left and i[0].centerx != screen.get_width() // 2:
				i[1].set_alpha(variables.alpha)
		variables.alpha -= 1
		if variables.alpha == 0:
			for i in variables.rects:
				if screen.get_width() >= i[0].left and i[0].centerx != screen.get_width() // 2:
					i[1].set_alpha(255)
			variables.game_event = 'prepearing-title'
			variables.count = 0

	if variables.game_event == 'prepearing-title':
		if variables.random_rec[0].left > 102:
			variables.random_rec[0].left -= 4
		else:
			variables.formatted_title = format_string_for_rect(variables,
			                                                   screen.get_width() - variables.img_width - 224,
			                                                   variables.random_rec[2], variables.TXT_COLOR)
			variables.prev_event = 'rolling'
			variables.game_event = 'showing-title'

	if variables.game_event == 'showing-title':
		variables.blocks = []
		variables.blocks.append(
			pg.Rect([screen.get_width() - 162, (screen.get_height() + variables.img_height) // 2 - 60, 40, 40]))
		variables.lines = []
		variables.lines.append([(102 + variables.img_width, (screen.get_height() - variables.img_height) // 2),
		                        (screen.get_width() - 102, (screen.get_height() - variables.img_height) // 2)])
		variables.lines.append([(screen.get_width() - 102, (screen.get_height() - variables.img_height) // 2),
		                        (screen.get_width() - 102, (screen.get_height() + variables.img_height) // 2)])
		variables.lines.append([(102 + variables.img_width, (screen.get_height() + variables.img_height) // 2),
		                        (screen.get_width() - 102, (screen.get_height() + variables.img_height) // 2)])
		variables.yes_block = []
		variables.yes_block.append([(screen.get_width() - 158, (screen.get_height() + variables.img_height) // 2 - 56),
		                            (screen.get_width() - 126, (screen.get_height() + variables.img_height) // 2 - 24)])
		variables.yes_block.append([(screen.get_width() - 158, (screen.get_height() + variables.img_height) // 2 - 24),
		                            (screen.get_width() - 126, (screen.get_height() + variables.img_height) // 2 - 56)])
		variables.no_block = []
		variables.no_block.append([(screen.get_width() - 158, (screen.get_height() + variables.img_height) // 2 - 41),
		                           (screen.get_width() - 126, (screen.get_height() + variables.img_height) // 2 - 41)])
		variables.no_block.append([(screen.get_width() - 142, (screen.get_height() + variables.img_height) // 2 - 25),
		                           (screen.get_width() - 142, (screen.get_height() + variables.img_height) // 2 - 57)])
		all_info = variables.df.loc[variables.df['Title Name'] == variables.random_rec[2]]
		aired = all_info['Aired'].item()
		# author = all_info['Author'].item()
		genres = all_info['Genres'].item()
		rating = all_info['Rating'].item()
		duration = all_info['Duration'].item()
		# type_ = all_info['Type'].item()
		meta = all_info['Metascore'].item()
		score = all_info['IMDb'].item()
		# episodes = all_info['Episodes'].item()
		font = pg.font.SysFont(variables.font_name, variables.font_size)
		variables.strings = []
		# aired
		variables.strings.append(font.render(f'Aired: {aired}', 0, variables.TXT_COLOR))
		genres_line = ', '.join(genres)
		# genres
		variables.strings.append(font.render(f'Genres: {genres_line}', 0, variables.TXT_COLOR))
		variables.reduced = 1
		while variables.strings[1].get_width() > screen.get_width() - variables.img_width - 224:
			genres_line = ', '.join(genres[:-variables.reduced]) + ','
			variables.reduced += 1
			genres_line_1 = ', '.join(genres[-variables.reduced + 1:])
			variables.strings[1] = font.render(f'Genres: {genres_line}', 0, variables.TXT_COLOR)
			if len(variables.strings) == 2:
				variables.strings.append(font.render(genres_line_1, 0, variables.TXT_COLOR))
			else:
				variables.strings[2] = font.render(genres_line_1, 0, variables.TXT_COLOR)
		genres = genres[-variables.reduced + 1:]
		variables.reduced = 1
		if len(variables.strings) == 3:
			while variables.strings[2].get_width() > screen.get_width() - variables.img_width - 224:
				genres_line_1 = ', '.join(genres[:-variables.reduced]) + ','
				variables.reduced += 1
				genres_line_2 = ', '.join(genres[-variables.reduced + 1:])
				variables.strings[2] = font.render(f'{genres_line_1}', 0, variables.TXT_COLOR)
				if len(variables.strings) == 3:
					variables.strings.append(font.render(genres_line_2, 0, variables.TXT_COLOR))
				else:
					variables.strings[3] = font.render(genres_line_2, 0, variables.TXT_COLOR)
		genres = genres[-variables.reduced + 1:]
		variables.reduced = 1
		if len(variables.strings) == 4:
			while variables.strings[3].get_width() > screen.get_width() - variables.img_width - 224:
				genres_line_2 = ', '.join(genres[:-variables.reduced]) + ','
				variables.reduced += 1
				genres_line_3 = ', '.join(genres[-variables.reduced + 1:])
				variables.strings[3] = font.render(f'{genres_line_2}', 0, variables.TXT_COLOR)
				if len(variables.strings) == 4:
					variables.strings.append(font.render(genres_line_3, 0, variables.TXT_COLOR))
				else:
					variables.strings[4] = font.render(genres_line_3, 0, variables.TXT_COLOR)
		# duration
		variables.strings.append(font.render(f'Duration: {format_time(duration)}', 0, variables.TXT_COLOR))
		# rating
		variables.strings.append(font.render(f'Rating: {rating}', 0, variables.TXT_COLOR))
		# stat
		if not isnan(meta):
			variables.strings.append(font.render('Metascore: {}'.format(meta), 0, variables.TXT_COLOR))
		# type
		variables.strings.append(font.render('IMDb: {:.2f}'.format(score), 0, variables.TXT_COLOR))
	# variables.favorite = pg.Rect([])

	if variables.game_event == 'start':
		if len(variables.titles) == 0:
			load_images(variables, screen)

	if variables.game_event == 'main-menu':
		variables.blocks = []
		variables.blocks.append(pg.Rect([(screen.get_width() - 600) // 2, (screen.get_height() - 525) // 2, 600, 525]))
		for i in range(4):
			variables.blocks.append(pg.Rect(
				[(screen.get_width() - 600) // 2 + 25, (screen.get_height() - 525) // 2 + 25 + 125 * i, 550, 100]))
		variables.string = []
		buttons = ['LET\'S SPIN', 'CATALOGUE', 'MY LIST', 'QUIT']
		for i in buttons:
			variables.string.append(variables.font.render(i, 0, (255, 255, 255)))

	if variables.game_event == 'catalogue':
		variables.blocks = []
		variables.blocks.append(pg.Rect([screen.get_width() - 60, screen.get_height() - 60, 40, 40]))
		variables.lines = []
		variables.lines.append(
			[(screen.get_width() - 60, screen.get_height() - 20), (screen.get_width() - 40, screen.get_height() - 60)])
		variables.lines.append(
			[(screen.get_width() - 40, screen.get_height() - 60), (screen.get_width() - 20, screen.get_height() - 20)])

	if variables.game_event == 'my-list':
		variables.string = variables.font.render('~~~IT\'S LITTLE BIT EMPTY~~~', 0, variables.TXT_COLOR)

	if variables.game_event == 'scrolling-up':
		while variables.navi_bar[0].top != 40:
			for i in variables.navi_bar[:-1]:
				i.top += 40
			for i in variables.sorted_minis:
				i[0].top += 40
		variables.game_event = 'catalogue'

	if variables.game_event == 'choosing-roll':
		variables.blocks = []
		variables.blocks.append(pg.Rect([(screen.get_width() - 600) // 2, (screen.get_height() - 400) // 2, 600, 400]))
		for i in range(3):
			variables.blocks.append(pg.Rect(
				[(screen.get_width() - 600) // 2 + 25, (screen.get_height() - 400) // 2 + 25 + 125 * i, 550, 100]))
		variables.string = []
		text = ['\'STANDART\' SPIN', '\'MY LIST\' SPIN', '\'SORTED\' SPIN']
		for i in text:
			variables.string.append(variables.font.render(i, 0, variables.TXT_COLOR))

	if variables.game_event == 'sorting':
		variables.blocks = []
		variables.blocks.append(pg.Rect([(screen.get_width() - 600) // 2, (screen.get_height() - 620) // 2, 600, 620]))
		for i in range(6):
			variables.blocks.append(pg.Rect(
				[(screen.get_width() - 600) // 2 + 20, (screen.get_height() - 620) // 2 + 20 + 120 * i, 560, 100]))
		variables.string = []
		text = ['GENRES', 'IMDb', 'DURATION', 'AIRED', 'SPIN!']
		for i in text:
			variables.string.append(variables.font.render(i, 0, variables.TXT_COLOR))

	if variables.game_event == 'sorting-catalogue':
		variables.blocks = []
		variables.blocks.append(pg.Rect([(screen.get_width() - 600) // 2, (screen.get_height() - 620) // 2, 600, 620]))
		for i in range(6):
			variables.blocks.append(pg.Rect(
				[(screen.get_width() - 600) // 2 + 20, (screen.get_height() - 620) // 2 + 20 + 120 * i, 560, 100]))
		variables.string = []
		text = ['GENRES', 'IMDb', 'DURATION', 'AIRED', 'SORT!']
		for i in text:
			variables.string.append(variables.font.render(i, 0, variables.TXT_COLOR))

	if variables.game_event == 'sorting-genres':
		variables.blocks = []
		variables.blocks.append(pg.Rect([(screen.get_width() - 900) // 2, (screen.get_height() - 620) // 2, 900, 620]))
		for i in range(20):
			variables.blocks.append(pg.Rect([(screen.get_width() - 900) // 2 + 20 + 220 * (i % 4),
			                                 (screen.get_height() - 620) // 2 + 20 + 120 * (i // 4), 200, 100]))
		variables.unique_genres = list(variables.df['Genres'].explode().unique())
		variables.string = []
		for i in variables.unique_genres:
			variables.string.append(variables.font.render(i, 0, variables.TXT_COLOR))

	if variables.game_event == 'sorting-imdb':
		variables.blocks = []
		variables.blocks.append(pg.Rect([(screen.get_width() - 660) // 2, (screen.get_height() - 380) // 2, 660, 380]))
		for i in range(6):
			variables.blocks.append(pg.Rect([(screen.get_width() - 660) // 2 + 20 + 320 * (i % 2),
			                                 (screen.get_height() - 380) // 2 + 20 + 120 * (i // 2), 300, 100]))
		variables.imdb_sorting = [6.0, 6.5, 7.0, 7.5, 8.0, 8.5]
		variables.string = []
		for i in variables.imdb_sorting:
			variables.string.append(variables.font.render(str(i) + '+', 0, variables.TXT_COLOR))

	if variables.game_event == 'sorting-duration':
		variables.blocks = []
		variables.blocks.append(pg.Rect([(screen.get_width() - 660) // 2, (screen.get_height() - 380) // 2, 660, 380]))
		for i in variables.duration:
			variables.blocks.append(pg.Rect([(screen.get_width() - 550) // 2 + 50 * variables.durations.index(i),
			                                 (screen.get_height() - variables.string[0].get_height()) // 2 - 20, 50,
			                                 40]))
		variables.string = []
		variables.string.append(variables.font.render(
			'{} - {}'.format(format_time(variables.duration[0]), format_time(variables.duration[1])), 0, (0, 0, 0)))
		variables.lines = []
		variables.lines.append(
			[((screen.get_width() - 550) // 2, (screen.get_height() - variables.string[0].get_height()) // 2),
			 ((screen.get_width() + 550) // 2 - 2, (screen.get_height() - variables.string[0].get_height()) // 2)])
		if hasattr(variables, 'moving_block'):
			if 30 < (pg.mouse.get_pos()[0] - (screen.get_width() - 550) // 2) // 50 * 10 + 40 < 150:
				if variables.moving_block == 0:
					if (pg.mouse.get_pos()[0] - (screen.get_width() - 550) // 2) // 50 * 10 + 40 < variables.duration[
						1]:
						variables.duration[variables.moving_block] = (pg.mouse.get_pos()[0] - (
								screen.get_width() - 550) // 2) // 50 * 10 + 40
				if variables.moving_block == 1:
					if (pg.mouse.get_pos()[0] - (screen.get_width() - 550) // 2) // 50 * 10 + 40 > variables.duration[
						0]:
						variables.duration[variables.moving_block] = (pg.mouse.get_pos()[0] - (
								screen.get_width() - 550) // 2) // 50 * 10 + 40
				update_sorted_titles(variables)

	if variables.game_event == 'sorting-aired':
		variables.blocks = []
		variables.blocks.append(pg.Rect([(screen.get_width() - 660) // 2, (screen.get_height() - 380) // 2, 660, 380]))
		for i in variables.aired:
			variables.blocks.append(pg.Rect([(screen.get_width() - 544) // 2 + 32 * variables.aired_list.index(i),
			                                 (screen.get_height() - variables.string[0].get_height()) // 2 - 20, 32,
			                                 40]))
		variables.string = []
		variables.string.append(
			variables.font.render('{} - {}'.format(variables.aired[0], variables.aired[1]), 0, (0, 0, 0)))
		variables.lines = []
		variables.lines.append(
			[((screen.get_width() - 544) // 2, (screen.get_height() - variables.string[0].get_height()) // 2),
			 ((screen.get_width() + 544) // 2 - 2, (screen.get_height() - variables.string[0].get_height()) // 2)])
		if hasattr(variables, 'moving_block'):
			if 1935 < (pg.mouse.get_pos()[0] - (screen.get_width() - 544) // 2) // 32 * 5 + 1940 < 2025:
				if variables.moving_block == 0:
					if (pg.mouse.get_pos()[0] - (screen.get_width() - 544) // 2) // 32 * 5 + 1940 < variables.aired[1]:
						variables.aired[variables.moving_block] = (pg.mouse.get_pos()[0] - (
								screen.get_width() - 544) // 2) // 32 * 5 + 1940
				if variables.moving_block == 1:
					if (pg.mouse.get_pos()[0] - (screen.get_width() - 544) // 2) // 32 * 5 + 1940 > variables.aired[0]:
						variables.aired[variables.moving_block] = (pg.mouse.get_pos()[0] - (
								screen.get_width() - 544) // 2) // 32 * 5 + 1940
				update_sorted_titles(variables)


def check_keydown(variables, event, screen):
	if event.key == pg.K_ESCAPE:
		if variables.game_event == 'catalogue':
			variables.navi_bar[0].topleft = (screen.get_width() - variables.minis_row * 200) // 2, 40
			variables.navi_bar[1].topleft = screen.get_width() - (
					screen.get_width() - variables.minis_row * 200) // 2 - 200 - 20, 60
			variables.game_event = 'main-menu'
		elif variables.game_event == 'main-menu':
			save(variables)
			exit()
		elif variables.game_event == 'showing-title' and variables.prev_event == 'rolling':
			variables.rolling_titles = ''
			variables.alpha = 255
			variables.step = 16
			variables.random_rec[0].left = screen.get_width() + variables.step
			for i in variables.rects:
				i[0].left = screen.get_width() + variables.step
			variables.rects[0][0].left = -(variables.img_width // variables.step + 1) * variables.step
			variables.game_event = 'choosing-roll'
		elif variables.game_event == 'showing-title' and variables.prev_event == 'catalogue':
			variables.random_rec[0].left = screen.get_width() + variables.step
			variables.game_event = 'catalogue'
		elif variables.game_event == 'showing-title' and variables.prev_event == 'my-list':
			variables.random_rec[0].left = screen.get_width() + variables.step
			format_my_list(variables, screen)
			variables.game_event = 'my-list'
		elif variables.game_event == 'my-list':
			variables.game_event = 'main-menu'
		elif variables.game_event == 'question-top':
			variables.game_event = 'choosing-roll'
		elif variables.game_event == 'choosing-roll':
			variables.alert = False
			variables.game_event = 'main-menu'
		elif variables.game_event == 'sorting-catalogue':
			variables.sorted_minis = variables.minis
			variables.alert = False
			variables.game_event = 'catalogue'
		elif variables.game_event == 'sorting':
			if hasattr(variables, 'imdb'):
				del variables.imdb
			variables.game_event = 'choosing-roll'
		elif (
				(variables.game_event == 'sorting-genres' or
				 variables.game_event == 'sorting-imdb' or
				 variables.game_event == 'sorting-duration' or
				 variables.game_event == 'sorting-aired') and
				variables.prev_event == 'sorting'
		):
			variables.game_event = 'sorting'
		elif (
				(variables.game_event == 'sorting-genres' or
				 variables.game_event == 'sorting-imdb' or
				 variables.game_event == 'sorting-duration' or
				 variables.game_event == 'sorting-aired') and
				variables.prev_event == 'sorting-catalogue'
		):
			variables.game_event = 'sorting-catalogue'
	if event.key == pg.K_SPACE:
		variables.stopping = True
	if variables.game_event == 'question-top':
		if event.key in variables.numbers:
			variables.rolling_titles += pg.key.name(event.key)
		if event.key == pg.K_BACKSPACE:
			variables.rolling_titles = variables.rolling_titles[:-1]
		if event.key == pg.K_RETURN:
			if 250 >= int(variables.rolling_titles) >= 5:
				variables.sorted_titles = variables.rects[:int(variables.rolling_titles)]
				variables.alpha = 255
				variables.step = 16
				for i in variables.sorted_titles:
					i[0].left = screen.get_width() + variables.step
				variables.sorted_titles[0][0].left = -(variables.img_width // variables.step + 1) * variables.step
				variables.game_event = 'rolling'
			else:
				variables.font_color = (255, 0, 0)
	if variables.game_event == 'showing-title':
		if variables.prev_event == 'rolling' and event.key == pg.K_RETURN:
			variables.alpha = 255
			variables.step = 16
			for i in variables.sorted_titles:
				i[0].left = screen.get_width() + variables.step
			format_my_list(variables, screen)
			variables.sorted_titles[0][0].left = -(variables.img_width // variables.step + 1) * variables.step
			variables.game_event = 'rolling'
		"""
		if variables.prev_event == 'my-list':
			if event.key == pg.K_RIGHT:
				for i in range(len(variables.my_list_rects)):
					if variables.random_rec[2] == variables.my_list_rects[i][2]:
						if i == len(variables.my_list_rects)-1:
							for j in range(len(variables.rects)):
								if variables.my_list_rects[i][2] == variables.rects[j][2]
									variables.random_rec = variables.rects[j]
						else:
							variables.random_rec = variables.my_list_rects[i+1]
						variables.formated_title = format_string_for_rect(variables, screen.get_width()-variables.img_width-224,variables.random_rec[2], variables.TXT_COLOR)
						break
			if event.key == pg.K_LEFT:
				for i in range(len(variables.my_list_rects)):
					if variables.random_rec[2] == variables.my_list_rects[i][2]:
						if i == 0:
							for j in range(len(variables.rects)):
								if variables.my_list_rects[i][2] == variables.rects[j][2]
									variables.random_rec = variables.rects[len(variables.rects)-1]
						else:
							for j in range(len(variables.rects)):
								if variables.my_list_rects[i][2] == variables.rects[j][2]
									variables.random_rec = variables.rects[j-1]
						variables.formated_title = format_string_for_rect(variables, screen.get_width()-variables.img_width-224,variables.random_rec[2], variables.TXT_COLOR)
						break
		"""


def check_mouse_down(variables, event, screen):
	if event.button == 1:

		if variables.game_event == 'main-menu':
			if variables.blocks[1].collidepoint(event.pos):
				variables.game_event = 'choosing-roll'
			elif variables.blocks[2].collidepoint(event.pos):
				variables.sorted_minis = variables.minis
				format_minis(variables, screen)
				variables.game_event = 'catalogue'
			elif variables.blocks[3].collidepoint(event.pos):
				variables.game_event = 'my-list'
				format_my_list(variables, screen)
			elif variables.blocks[4].collidepoint(event.pos):
				save(variables)
				exit()

		elif variables.game_event == 'catalogue':
			for i in variables.sorted_minis:
				if i[0].collidepoint(event.pos):
					variables.prev_event = 'catalogue'
					for j in variables.rects:
						if i[2] == j[2]:
							variables.random_rec = j
					variables.random_rec[0].topleft = (102, (screen.get_height() - variables.img_height) // 2)
					variables.formatted_title = format_string_for_rect(variables,
					                                                   screen.get_width() - variables.img_width - 224,
					                                                   variables.random_rec[2], variables.TXT_COLOR)
					variables.game_event = 'showing-title'
					break
			if variables.blocks[0].collidepoint(event.pos) and variables.navi_bar[0].top < 0:
				variables.game_event = 'scrolling-up'
			if variables.navi_bar[1].collidepoint(event.pos):
				variables.sorted_df = variables.df.copy()
				variables.sorted_genres = []
				variables.duration = [40, 140]
				variables.aired = [1940, 2020]
				variables.game_event = 'sorting-catalogue'

		elif variables.game_event == 'my-list':
			for i in variables.my_list_rects:
				if i[0].collidepoint(event.pos):
					variables.prev_event = 'my-list'
					for j in variables.rects:
						if i[2] in j:
							variables.random_rec = j
							break
					variables.random_rec[0].topleft = (102, (screen.get_height() - variables.img_height) // 2)
					variables.formatted_title = format_string_for_rect(variables,
					                                                   screen.get_width() - variables.img_width - 224,
					                                                   variables.random_rec[2], variables.TXT_COLOR)
					variables.game_event = 'showing-title'
					break

		elif variables.game_event == 'showing-title':
			if variables.blocks[0].collidepoint(event.pos):
				if not variables.random_rec[2] in variables.my_list:
					variables.my_list.append(variables.random_rec[2])
				else:
					for i in range(len(variables.my_list)):
						if variables.random_rec[2] == variables.my_list[i]:
							del variables.my_list[i]
							break

		elif variables.game_event == 'choosing-roll':
			if variables.blocks[1].collidepoint(event.pos):
				variables.game_event = 'question-top'
			elif variables.blocks[2].collidepoint(event.pos):
				if len(variables.my_list) >= 5:
					variables.sorted_titles = []
					for i in variables.rects:
						for j in variables.my_list:
							if j == i[2]:
								variables.sorted_titles.append(i)
					variables.alpha = 255
					variables.step = 16
					for i in variables.sorted_titles:
						i[0].left = screen.get_width() + variables.step
					variables.sorted_titles[0][0].left = -(variables.img_width // variables.step + 1) * variables.step
					variables.game_event = 'rolling'
				else:
					variables.alert = True
			elif variables.blocks[3].collidepoint(event.pos):
				variables.sorted_df = variables.df.copy()
				variables.sorted_genres = []
				variables.duration = [40, 140]
				variables.aired = [1940, 2020]
				variables.game_event = 'sorting'

		elif variables.game_event == 'sorting':
			if variables.blocks[1].collidepoint(event.pos):
				variables.prev_event = 'sorting'
				variables.game_event = 'sorting-genres'
			if variables.blocks[2].collidepoint(event.pos):
				variables.prev_event = 'sorting'
				variables.game_event = 'sorting-imdb'
			if variables.blocks[3].collidepoint(event.pos):
				variables.prev_event = 'sorting'
				variables.game_event = 'sorting-duration'
			if variables.blocks[4].collidepoint(event.pos):
				variables.prev_event = 'sorting'
				variables.game_event = 'sorting-aired'
			if variables.blocks[5].collidepoint(event.pos):
				if len(variables.sorted_df) >= 5:
					variables.sorted_titles = []
					for i in variables.rects:
						if i[2] in variables.sorted_df['Title Name'].to_list():
							variables.sorted_titles.append(i)
					variables.alpha = 255
					variables.step = 16
					for i in variables.sorted_titles:
						i[0].left = screen.get_width() + variables.step
					variables.sorted_titles[0][0].left = -(variables.img_width // variables.step + 1) * variables.step
					variables.game_event = 'rolling'
				else:
					variables.alert = True

		elif variables.game_event == 'sorting-catalogue':
			if variables.blocks[1].collidepoint(event.pos):
				variables.prev_event = 'sorting-catalogue'
				variables.game_event = 'sorting-genres'
			if variables.blocks[2].collidepoint(event.pos):
				variables.prev_event = 'sorting-catalogue'
				variables.game_event = 'sorting-imdb'
			if variables.blocks[3].collidepoint(event.pos):
				variables.prev_event = 'sorting-catalogue'
				variables.game_event = 'sorting-duration'
			if variables.blocks[4].collidepoint(event.pos):
				variables.prev_event = 'sorting-catalogue'
				variables.game_event = 'sorting-aired'
			if variables.blocks[5].collidepoint(event.pos):
				if len(variables.sorted_df) != 0:
					variables.sorted_minis = []
					for i in variables.minis:
						if i[2] in variables.sorted_df['Title Name'].to_list():
							variables.sorted_minis.append(i)
					format_minis(variables, screen)
					variables.game_event = 'catalogue'
				else:
					variables.alert = True

		elif variables.game_event == 'sorting-genres':
			for i in variables.blocks[1:]:
				if i.collidepoint(event.pos):
					genre = variables.unique_genres[variables.blocks.index(i) - 1]
					if not genre in variables.sorted_genres:
						variables.sorted_genres.append(genre)
						variables.sorted_df = variables.sorted_df[
							variables.sorted_df.apply(lambda x: genre in x['Genres'], axis=1)]
					break

		elif variables.game_event == 'sorting-imdb':
			for i in variables.blocks[1:]:
				if i.collidepoint(event.pos):
					variables.imdb = variables.imdb_sorting[variables.blocks.index(i) - 1]
					update_sorted_titles(variables)

		elif variables.game_event == 'sorting-duration':
			for i in variables.blocks[1:]:
				if i.collidepoint(event.pos):
					variables.moving_block = variables.blocks[1:].index(i)

		elif variables.game_event == 'sorting-aired':
			for i in variables.blocks[1:]:
				if i.collidepoint(event.pos):
					variables.moving_block = variables.blocks[1:].index(i)

	if event.button == 3:

		if variables.game_event == 'sorting-genres':
			for i in variables.blocks[1:]:
				if i.collidepoint(event.pos):
					genre = variables.unique_genres[variables.blocks.index(i) - 1]
					if genre in variables.sorted_genres:
						del variables.sorted_genres[variables.sorted_genres.index(genre)]
						update_sorted_titles(variables)

		if variables.game_event == 'sorting-imdb':
			for i in variables.blocks[1:]:
				if i.collidepoint(event.pos):
					if hasattr(variables, 'imdb'):
						del variables.imdb
						update_sorted_titles(variables)

	if event.button == 5:

		if variables.game_event == 'catalogue' and variables.sorted_minis[-1:][0][0].bottom > screen.get_height() - 40:
			for i in variables.sorted_minis:
				i[0].top -= 40
			for i in variables.navi_bar[:-1]:
				i.top -= 40

		if variables.game_event == 'my-list' and variables.my_list_rects[-1:][0][0].bottom > screen.get_height() - 40:
			for i in variables.my_list_rects:
				i[0].top -= 40

	if event.button == 4:

		if variables.game_event == 'catalogue' and variables.navi_bar[0].top < 40:
			for i in variables.sorted_minis:
				i[0].top += 40
			for i in variables.navi_bar[:-1]:
				i.top += 40

		if variables.game_event == 'my-list' and variables.my_list_rects[0][0].top < 40:
			for i in variables.my_list_rects:
				i[0].top += 40


def check_mouse_up(variables, event):
	if event.button == 1:

		if variables.game_event == 'sorting-duration':
			if hasattr(variables, 'moving_block'):
				del variables.moving_block

		if variables.game_event == 'sorting-aired':
			if hasattr(variables, 'moving_block'):
				del variables.moving_block


def show(variables, screen):
	if variables.game_event == 'question-top':
		variables.string = []
		variables.string.append(
			variables.font.render('PLEASE, ENTER NUMBER OF TITLES IN TOP (5 TO 250)', 0, variables.font_color))
		variables.string.append(variables.font.render('{}_'.format(variables.rolling_titles), 0, (255, 255, 255)))
		for line in range(len(variables.string)):
			screen.blit(variables.string[line], ((screen.get_width() - variables.string[line].get_width()) // 2, (
					screen.get_height() - variables.string[line].get_height() * len(variables.string)) // 2 + line *
			                                     variables.string[line].get_height()))

	if variables.game_event == 'rolling' or variables.game_event == 'vanishing':
		for i in variables.rects:
			if screen.get_width() >= i[0].left:
				screen.blit(i[1], i[0])

	if variables.game_event == 'prepearing-title':
		screen.blit(variables.random_rec[1], variables.random_rec[0])

	if variables.game_event == 'showing-title':
		for i in variables.blocks:
			pg.draw.rect(screen, (255, 255, 255), i)
		if variables.random_rec[2] in variables.my_list:
			for i in variables.yes_block:
				pg.draw.line(screen, (0, 0, 0), i[0], i[1], 4)
		else:
			for i in variables.no_block:
				pg.draw.line(screen, (0, 0, 0), i[0], i[1], 4)
		for i in variables.lines:
			pg.draw.line(screen, (255, 255, 255), i[0], i[1])
		screen.blit(variables.random_rec[1], variables.random_rec[0])
		screen.blit(variables.formatted_title,
		            (variables.img_width + 122, (screen.get_height() - variables.img_height) // 2 + 20))
		for i in range(len(variables.strings)):
			screen.blit(variables.strings[i], (variables.img_width + 122, (
					screen.get_height() - variables.img_height) // 2 + 20 + 60 * i + variables.formatted_title.get_height()))

	if variables.game_event == 'main-menu':
		pg.draw.rect(screen, (255, 255, 255), variables.blocks[0])
		for i in range(1, len(variables.blocks)):
			pg.draw.rect(screen, (0, 0, 0), variables.blocks[i])
		for i in variables.string:
			screen.blit(i, ((screen.get_width() - i.get_width()) // 2, (screen.get_height() - 525) // 2 + 25 + (
					100 - i.get_height()) // 2 + 125 * variables.string.index(i)))

	if variables.game_event == 'catalogue':
		for i in variables.sorted_minis:
			# pg.draw.rect(screen, (255,255,255), i[0])
			screen.blit(i[1], i[0])
		for i in variables.navi_bar[:1]:
			pg.draw.rect(screen, (255, 255, 255), i)
		for i in variables.navi_bar[1:-1]:
			pg.draw.rect(screen, (0, 0, 0), i)
		screen.blit(variables.navi_bar[2], (
			screen.get_width() - (screen.get_width() - variables.minis_row * 200) // 2 - 20 - (
					200 - variables.navi_bar[2].get_width()) // 2 - variables.navi_bar[2].get_width(),
			variables.navi_bar[0].top + 20 + (60 - variables.navi_bar[2].get_height()) // 2))
		if variables.navi_bar[0].top < 0:
			for i in variables.lines:
				pg.draw.line(screen, (255, 255, 255), i[0], i[1], 6)

	if variables.game_event == 'my-list':
		if len(variables.my_list) != 0:
			for i in variables.my_list_rects:
				screen.blit(i[1], i[0])
		else:
			screen.blit(variables.string, ((screen.get_width() - variables.string.get_width()) // 2,
			                               (screen.get_height() - variables.string.get_height()) // 2))

	if variables.game_event == 'choosing-roll':
		pg.draw.rect(screen, (255, 255, 255), variables.blocks[0])
		for i in variables.blocks[1:]:
			pg.draw.rect(screen, (0, 0, 0), i)
		for i in variables.string:
			screen.blit(i, ((screen.get_width() - i.get_width()) // 2, (screen.get_height() - 400) // 2 + 25 + (
					100 - i.get_height()) // 2 + 125 * variables.string.index(i)))
		if variables.alert:
			i = variables.font.render('At least 5 Titles!', 0, (255, 0, 0))
			screen.blit(i, (0, screen.get_height() - i.get_height()))

	if variables.game_event == 'sorting':
		pg.draw.rect(screen, (255, 255, 255), variables.blocks[0])
		for i in variables.blocks[1:]:
			pg.draw.rect(screen, (0, 0, 0), i)
		for i in variables.string:
			screen.blit(i, ((screen.get_width() - i.get_width()) // 2, (screen.get_height() - 620) // 2 + 20 + (
					100 - i.get_height()) // 2 + 120 * variables.string.index(i)))
		if variables.alert:
			i = variables.font.render('At least 5 Titles!', 0, (255, 0, 0))
			screen.blit(i, (0, screen.get_height() - i.get_height()))

	if variables.game_event == 'sorting-catalogue':
		pg.draw.rect(screen, (255, 255, 255), variables.blocks[0])
		for i in variables.blocks[1:]:
			pg.draw.rect(screen, (0, 0, 0), i)
		for i in variables.string:
			screen.blit(i, ((screen.get_width() - i.get_width()) // 2, (screen.get_height() - 620) // 2 + 20 + (
					100 - i.get_height()) // 2 + 120 * variables.string.index(i)))
		if variables.alert:
			i = variables.font.render('No Titles!', 0, (255, 0, 0))
			screen.blit(i, (0, screen.get_height() - i.get_height()))

	if variables.game_event == 'sorting-genres':
		pg.draw.rect(screen, (255, 255, 255), variables.blocks[0])
		for i in variables.blocks[1:]:
			if variables.unique_genres[variables.blocks[1:].index(i)] in variables.sorted_genres:
				pg.draw.rect(screen, (100, 100, 100), i)
			else:
				pg.draw.rect(screen, (0, 0, 0), i)
		for i in variables.string:
			screen.blit(i, (
				(screen.get_width() - variables.blocks[0].width) // 2 + 20 + (200 - i.get_width()) // 2 + 220 * (
						variables.string.index(i) % 4),
				(screen.get_height() - variables.blocks[0].height) // 2 + 20 + (100 - i.get_height()) // 2 + 120 * (
						variables.string.index(i) // 4)))

	if variables.game_event == 'sorting-imdb':
		pg.draw.rect(screen, (255, 255, 255), variables.blocks[0])
		for i in variables.blocks[1:]:
			if hasattr(variables, 'imdb'):
				if variables.imdb_sorting[variables.blocks.index(i) - 1] == variables.imdb:
					pg.draw.rect(screen, (100, 100, 100), i)
				else:
					pg.draw.rect(screen, (0, 0, 0), i)
			else:
				pg.draw.rect(screen, (0, 0, 0), i)
		for i in variables.string:
			screen.blit(i, (
				(screen.get_width() - variables.blocks[0].width) // 2 + 20 + (300 - i.get_width()) // 2 + 320 * (
						variables.string.index(i) % 2),
				(screen.get_height() - variables.blocks[0].height) // 2 + 20 + (100 - i.get_height()) // 2 + 120 * (
						variables.string.index(i) // 2)))

	if variables.game_event == 'sorting-duration':
		pg.draw.rect(screen, (255, 255, 255), variables.blocks[0])
		screen.blit(variables.string[0], ((screen.get_width() - variables.string[0].get_width()) // 2,
		                                  (screen.get_height() - variables.string[0].get_height()) // 2 + 40))
		pg.draw.line(screen, (0, 0, 0), variables.lines[0][0], variables.lines[0][1], 2)
		for i in variables.blocks[1:]:
			pg.draw.rect(screen, (0, 0, 0), i)

	if variables.game_event == 'sorting-aired':
		pg.draw.rect(screen, (255, 255, 255), variables.blocks[0])
		screen.blit(variables.string[0], ((screen.get_width() - variables.string[0].get_width()) // 2,
		                                  (screen.get_height() - variables.string[0].get_height()) // 2 + 40))
		pg.draw.line(screen, (0, 0, 0), variables.lines[0][0], variables.lines[0][1], 2)
		for i in variables.blocks[1:]:
			pg.draw.rect(screen, (0, 0, 0), i)

	if (
			variables.game_event == 'sorting' or
			variables.game_event == 'sorting-genres' or
			variables.game_event == 'sorting-imdb' or
			variables.game_event == 'sorting-duration' or
			variables.game_event == 'sorting-aired' or
			variables.game_event == 'sorting-catalogue'
	):
		variables.sorted_titles = []
		for i in variables.rects:
			if i[2] in variables.sorted_df['Title Name'].to_list():
				variables.sorted_titles.append(i)
		title_string = variables.font.render('{} Titles'.format(len(variables.sorted_titles)), 0, (255, 255, 255))
		screen.blit(title_string,
		            (screen.get_width() - title_string.get_width(), screen.get_height() - title_string.get_height()))


def loading(variables, screen):
	variables.navi_bar = []
	variables.navi_bar.append(
		pg.Rect([(screen.get_width() - variables.minis_row * 200) // 2, 40, variables.minis_row * 200, 100]))
	variables.navi_bar.append(
		pg.Rect([screen.get_width() - (screen.get_width() - variables.minis_row * 200) // 2 - 200 - 20, 60, 200, 60]))
	variables.navi_bar.append(variables.font.render('SORT', 0, (255, 255, 255)))
	variables.string = []
	variables.string.append(variables.font.render('~~~LOADING~~~'.format(variables.input), 0, (0, 0, 0)))
	variables.lines = []
	variables.lines.append(
		[((screen.get_width() - 400) // 2, (screen.get_height() - variables.string[0].get_height()) // 2 - 10),
		 ((screen.get_width() + 400) // 2, (screen.get_height() - variables.string[0].get_height()) // 2 - 10)])
	variables.lines.append(
		[((screen.get_width() - 400) // 2, (screen.get_height() + variables.string[0].get_height()) // 2 + 10),
		 ((screen.get_width() + 400) // 2, (screen.get_height() + variables.string[0].get_height()) // 2 + 10)])
	variables.lines.append(
		[((screen.get_width() - 400) // 2, (screen.get_height() - variables.string[0].get_height()) // 2 - 10),
		 ((screen.get_width() - 400) // 2, (screen.get_height() + variables.string[0].get_height()) // 2 + 10)])
	variables.lines.append(
		[((screen.get_width() + 400) // 2, (screen.get_height() - variables.string[0].get_height()) // 2 - 10),
		 ((screen.get_width() + 400) // 2, (screen.get_height() + variables.string[0].get_height()) // 2 + 10)])
	variables.loading_bar = pg.Rect(
		[(screen.get_width() - 400) // 2 + 1, (screen.get_height() - variables.string[0].get_height()) // 2 - 9,
		 int((len(variables.rects) / int(variables.input)) * 400), variables.string[0].get_height() + 19])
	screen.fill((0, 0, 0))
	pg.draw.rect(screen, (255, 255, 255), variables.loading_bar)
	for line in range(len(variables.string)):
		screen.blit(variables.string[line], ((screen.get_width() - variables.string[line].get_width()) // 2, (
				screen.get_height() - variables.string[line].get_height() * len(variables.string)) // 2 + line *
		                                     variables.string[line].get_height()))
	for line in variables.lines:
		pg.draw.line(screen, (255, 255, 255), line[0], line[1])
	pg.display.flip()


def load_images(variables, screen):
	variables.rects = [[pg.Rect([-(variables.img_width // variables.step + 1) * variables.step,
	                             (screen.get_height() - variables.img_height) // 2, variables.img_width,
	                             variables.img_height])]]
	variables.minis = [[pg.Rect([(screen.get_width() - variables.minis_row * 200) // 2 + 10, 160, 180, 252])]]
	variables.titles = []
	variables.df = read_csv('data/data.csv', encoding='cp1251')
	variables.df['Genres'] = [(list(i[1:-1].translate(variables.table).split(', '))) for i in variables.df['Genres']]
	for i in variables.df['Title Name']:
		variables.titles.append(i)
	for i in range(int(variables.input) - 1):
		variables.rects.append([pg.Rect(
			[screen.get_width() + variables.step, (screen.get_height() - variables.img_height) // 2,
			 variables.img_width, variables.img_height])])
		variables.rects[i].append(pg.image.load(
			'data/images/{}-{}/{}.jpg'.format(variables.img_width, variables.img_height,
			                                  variables.titles[i].translate(variables.table_2))).convert())
		variables.rects[i].append(variables.titles[i])
		variables.minis.append([pg.Rect(
			[(screen.get_width() - variables.minis_row * 200) // 2 + 10 + ((i + 1) % variables.minis_row) * 200,
			 160 + ((i + 1) // variables.minis_row) * 272, 180, 252])])
		variables.minis[i].append(pg.image.load(
			'data/images/180-252/{}.jpg'.format(variables.titles[i].translate(variables.table_2))).convert())
		variables.minis[i].append(variables.titles[i])
		loading(variables, screen)
	variables.rects[int(variables.input) - 1].append(pg.image.load(
		'data/images/{}-{}/{}.jpg'.format(variables.img_width, variables.img_height,
		                                  variables.titles[int(variables.input) - 1].translate(
			                                  variables.table_2))).convert())
	variables.rects[int(variables.input) - 1].append(variables.titles[int(variables.input) - 1])
	variables.minis[int(variables.input) - 1].append(pg.image.load('data/images/180-252/{}.jpg'.format(
		variables.titles[int(variables.input) - 1].translate(variables.table_2))).convert())
	variables.minis[int(variables.input) - 1].append(variables.titles[int(variables.input) - 1])
	variables.game_event = 'main-menu'


def format_string_for_rect(variables, width, text, color):
	size = 80
	line = variables.font.render(u'{}'.format(text), 0, color)
	while line.get_width() > width:
		size -= 1
		variables.font = pg.font.SysFont(variables.font_name, size)
		line = variables.font.render(u'{}'.format(text), 0, color)
	variables.font = pg.font.SysFont(variables.font_name, 40)
	return line


def save(variables):
	with open('data/my_list.txt', 'w', encoding="utf-8") as f:
		for i in variables.my_list:
			f.write(i + '\n')


def format_my_list(variables, screen):
	if len(variables.my_list) != 0:
		variables.my_list_rects = []
		for i in variables.minis:
			if i[2] in variables.my_list:
				variables.my_list_rects.append([None, i[1], i[2]])
		for i in range(len(variables.my_list_rects)):
			variables.my_list_rects[i][0] = pg.Rect(
				[(screen.get_width() - variables.minis_row * 200) // 2 + 10 + (i % variables.minis_row) * 200,
				 40 + (i // variables.minis_row) * 272, 180, 252])


def update_sorted_titles(variables):
	variables.alert = False
	variables.sorted_df = variables.df.copy()
	for i in variables.sorted_genres:
		variables.sorted_df = variables.sorted_df[variables.sorted_df.apply(lambda x: i in x['Genres'], axis=1)]
	if hasattr(variables, 'imdb'):
		variables.sorted_df = variables.sorted_df[variables.sorted_df['IMDb'] >= float(variables.imdb)]
	variables.sorted_df = variables.sorted_df[((variables.sorted_df['Duration'] >= variables.duration[0]) & (
			variables.sorted_df['Duration'] <= variables.duration[1]))]
	variables.sorted_df['Year'] = [splitting(i) for i in variables.sorted_df['Aired']]
	variables.sorted_df = variables.sorted_df[
		((variables.sorted_df['Year'] >= variables.aired[0]) & (variables.sorted_df['Year'] <= variables.aired[1]))]


def format_time(minutes):
	h = minutes // 60
	m = minutes % 60
	if h == 0:
		return '{}min'.format(m)
	return '{}h {}min'.format(h, m)


def splitting(i):
	try:
		y = list(i.split(' '))[2]
		y = int(y)
		return y
	except:
		return int(i)


def format_minis(variables, screen):
	temp = variables.sorted_minis
	variables.sorted_minis = []
	for i in range(len(temp)):
		variables.sorted_minis.append([pg.Rect(
			[(screen.get_width() - variables.minis_row * 200) // 2 + 10 + (i % variables.minis_row) * 200,
			 160 + (i // variables.minis_row) * 272, 180, 252])])
		variables.sorted_minis[i].append(temp[i][1])
		variables.sorted_minis[i].append(temp[i][2])
