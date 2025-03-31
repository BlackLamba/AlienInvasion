import sys
import pygame
from time import sleep

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import  Button, DiffButton
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
	"""Класс для управления ресурсами и поведением игры"""
	def __init__(self):
		"""Инициализирует игру и создает игровые ресурсы"""
		pygame.init()
		self.clock = pygame.time.Clock()
		self.settings = Settings()
		#Поверхность, на которой отображается игровой элемент.
		#Каждый элемент представляет собой собственную поверхность.
		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		# self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		# self.settings.screen_width = self.screen.get_rect().width
		# self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		# Создание экземпляра для хранения игровой статистики и панели результатов.
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

		# Игра "Инопланетное вторжение" запускается в активном состоянии.
		self.game_active = False

		# Создание кнопки Play.
		self.play_button = Button(self, "Play")
		# Создание кнопок сложности.
		self.set_easy_button = DiffButton(self, 'Easy')
		self.set_medium_button = DiffButton(self, 'Medium')
		self.set_hard_button = DiffButton(self, 'Hard')

	def run_game(self):
		"""Запускает основной цикл игры."""
		while True:
			self._check_events()
			if self.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			self._update_screen()
			self.clock.tick(60)

	def _start_game(self):
		# Сброс игровой статистики.
		self.stats.reset_stats()
		self.game_active = True

		# Сброс настроек игры.
		self.settings.initialize_dynamic_settings()

		# Очистка групп aliens и bullets.
		self.bullets.empty()
		self.aliens.empty()

		# Создание нового флота и размещение корабля в центре.
		self._create_fleet()
		self.ship.center_ship()

		# Обновление счета
		self.sb.prep_score()

		# Указатель мыши скрывается.
		pygame.mouse.set_visible(False)

	def _check_events(self):
		"""Обрабатывает нажатия клавиш и события мыши."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self, mouse_pos):
		"""Запускает новую игру при нажатии кнопки Play."""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.game_active:
			self._start_game()
			self.stats.reset_stats()
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()

	def _check_keydown_events(self, event):
		"""Реагирует на нажатие клавиш."""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_p and not self.game_active:
			self._start_game()

	def _check_keyup_events(self, event):
		"""Реагирует на отпускание клавиш."""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _fire_bullet(self):
		"""Создает новый снаряд и добавляет его в группу bullets."""
		if len(self.bullets) < self.settings.bullet_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Обновляет позиции снарядов и уничтожает старые снаряды"""
		# Обновление позиций снарядов.
		self.bullets.update()

		# Удаление снарядов, вышедших за край экрана.
		for bullet in self.bullets.copy():  # copy() используется для изменения группы снарядов
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_aline_collisions()

	def _check_bullet_aline_collisions(self):
		"""Обрабатывает коллизии снарядов с пришельцами."""
		# Удаление снарядов и пришельцев, участвующих в коллизиях.
		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True
		)
		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

		if not self.aliens:
			# Уничтожение существующих снарядов и создание нового флота.
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			# Увеличиение уровня.
			self.stats.level += 1
			self.sb.prep_level()

	def _update_aliens(self):
		"""
		Проверяет, достиг ли флот края экрана, с последующим обновлением
		позиций всех пришельцев во флоте.
		"""
		self._check_fleet_edges()
		self.aliens.update()

		# Проверка коллизий "пришелец-корабль".
		if pygame.sprite.spritecollideany(self.ship, self.aliens): # получает два аргумента: спрайт и группу.
			self._ship_hit()

		# Проверить, сталкиваются ли пришельцы с нижним краем экрана.
		self._check_aliens_bottom()

	def _ship_hit(self):
		"""Обрабатывает столкновение корабля с пришельцем."""
		# Уменьшение ships_left.
		if self.stats.ships_left > 0:
			self.stats.ships_left -= 1
			self.sb.prep_ships()
			# Очистка групп aliens и bullets.
			self.aliens.empty()
			self.bullets.empty()
			# Создание нового флота и размещение корабля в центре.
			self._create_fleet()
			self.ship.center_ship()
			# Пауза.
			sleep(1)
		else:
			self.game_active = False
			pygame.mouse.set_visible(True)

	def _check_fleet_edges(self):
		"""Реагирует на достижение пришельцем края экрана."""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Опускает весь флот и меняет его направление."""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _create_fleet(self):
		"""Создает флот пришельцев."""
		# Создание пришельца и вычисление количества пришельцев в ряду.
		# Интервал между соседними пришельцами равен ширине пришельца.
		# Расстояние между пришельцами составляет одну ширину и одну высоту пришельца.
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size

		current_x, current_y = alien_width, alien_height
		while current_y < (self.settings.screen_height - 3 * alien_height):
			while current_x < (self.settings.screen_width - 2 * alien_width):
				self._create_alien(current_x, current_y)
				current_x += 2 * alien_width

			# Конец ряда: сбрасываем значение х и инкрементируем значение у.
			current_x = alien_width
			current_y += 2 * alien_height

	def _create_alien(self, x_position, y_position):
		"""Создает пришельца и размещает его во флот."""
		new_alien = Alien(self)
		new_alien.x = x_position
		new_alien.rect.x = x_position
		new_alien.rect.y = y_position
		self.aliens.add(new_alien)

	def _check_aliens_bottom(self):
		"""Проверяет, добрались ли пришельцы до нижнего края экрана."""
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= self.settings.screen_height:
				# Происходит то же самое, что и при столкновении с кораблем.
				self._ship_hit()
				break

	def _update_screen(self):
		"""Обновляет изображения на экране и отображает новый экран."""
		self.screen.fill(self.settings.bg_color)
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.ship.blitme()
		self.aliens.draw(self.screen)

		# Выводит информацию о счете.
		self.sb.show_score()

		# Кнопка Play отображается в том случае, если игра неактивна.
		if not self.game_active:
			self.play_button.draw_button()
			self.set_easy_button.draw_button()
			self.set_medium_button.draw_button()
			self.set_hard_button.draw_button()

		pygame.display.flip()

if __name__ == "__main__":
	#Создание экземпляра и запуск игры
	ai = AlienInvasion()
	ai.run_game()