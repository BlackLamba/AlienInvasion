import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""Класс представляющий одного пришельца."""

	def __init__(self, ai_game):
		"""Инициализирует пришельца и задает его начальную позицию."""
		super().__init__()
		self.screen = ai_game.screen

		# Загрузка изображения пришельца и назначение атрибута rect.
		self.image = pygame.image.load('images/alien_ship1.png')
		self.rect = self.image.get_rect()

		# Каждый новый пришелец появляется в левом верхнем углу экрана.
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		# Сохранение точной горизонтальной позиции пришельца
		self.x = float(self.rect.x)
		self.settings = ai_game.settings

	def check_edges(self):
		"""Возвращает True, если пришелец находится у края экрана."""
		screen_rect = self.screen.get_rect()
		return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

	def update(self):
		"""Перемещает пришельца вправо."""
		self.x += (self.settings.alien_speed * self.settings.fleet_direction)
		self.rect.x = self.x