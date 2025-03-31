import pygame.font
from pygame.sprite import Sprite, Group

from ship import Ship

class Scoreboard:
	"""Класс для вывода игровой статистики."""

	def __init__(self, ai_game):
		"""Инициализирует атрибуты подсчета очков."""
		self.ai_game = ai_game
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings
		self.stats = ai_game.stats

		# Настройки шрифта для вывода счета.
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		# Подготовка исходного изображения счета.
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()

	def prep_score(self):
		"""Преобразует текущий счет в графическое изображение."""
		rounded_score = round(self.stats.score, -1)  # Округляем до десятков
		score_str = "{:,}".format(rounded_score)  # Форматирование с разделителями
		self.score_image = self.font.render(score_str, True,
											self.text_color, self.settings.bg_color)

		# Вывод счета в правой верхней части экрана.
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def prep_high_score(self):
		"""Преобразует рекордный счет в графическое изображение."""
		high_score = round(self.stats.high_score, -1)  # Округляем до десятков
		high_score_str = "{:,}".format(high_score)  # Форматирование с разделителями
		self.high_score_image = self.font.render(high_score_str, True,
											self.text_color, self.settings.bg_color)

		# Вывод счета в правой верхней части экрана.
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top

	def prep_level(self):
		"""Преобразует текущий уровень в графическое изображение."""
		level_str = str(self.stats.level)
		self.level_image = self.font.render(level_str, True,
					self.text_color, self.settings.bg_color)

		# Уровень вводится под текущим счетом.
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10

	def prep_ships(self):
		"""Сообщает количество оставшихся кораблей."""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_game)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)

	def show_score(self):
		"""Выводит счет на экран."""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)

	def check_high_score(self):
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()