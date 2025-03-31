import pygame
import sys

class RocketGame():

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((1200, 800))

	def run_game(self):
		while True:
