class Settings():
	"""Класс для хранения всех настроек игры "Инопланетное вторжение"."""

	def __init__(self):
		"""Инициализирует настройки игры."""
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (0, 120, 230)

		# Настройки корабля.
		self.ship_limit = 3

		# Параметры снаряда.
		self.bullet_speed = 2.5
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullet_allowed = 10

		self.fleet_drop_speed = 10

		# Темп ускорения игры
		self.speedup_scale = 1.3

		self.initialize_dynamic_settings()
		# Очки за пришельцев.
		self.alien_points = 50
		self.score_scale = 1.5

	def initialize_dynamic_settings(self):
		"""Инициализирует настройки, изменяющиеся в ходе игры."""
		self.ship_speed = 1.5
		self.bullet_speed = 2.5
		self.alien_speed = 1.0

		# fleet_direction = 1, обозначает движение вправо; а -1 - влево.
		self.fleet_direction = 1

	def increase_speed(self):
		"""Увеличивает настройки скорости."""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)
