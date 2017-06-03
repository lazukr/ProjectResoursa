import pygame
from materials import Wood
from random import randint
import math

SCREEN_SIZE = (640, 480)
GENERATION_TRIES = 100

class Resoursa():
	def __init__(self):

		# initialization
		pygame.display.init()
		pygame.font.init()

		self.screen = pygame.display.set_mode(SCREEN_SIZE)
		pygame.display.set_caption("Resoursa")

		self.items = {
			"count": 0,
			"list": []
		}

		self.clock = pygame.time.Clock()

		self.world_start()
		



	def world_start(self):
		generation_parameters = {}
		with open("world_gen.txt") as f:
			for line in f:
				(name, probability) = line.split()
				generation_parameters[name] =  int(float(probability)*GENERATION_TRIES)
		print(generation_parameters)


		for materials, amount in generation_parameters.items():
			print(materials, amount)
			for x in range(amount):
				location = (randint(0, SCREEN_SIZE[0]), randint(0, SCREEN_SIZE[1]))
				self.items["list"].append((Wood(self.items["count"], materials),
							 location))
				self.items["count"] += 1


		print(self.items)



	def draw_screen(self):
		display_objects = self.items["list"]
		for elements in display_objects:
			#print(elements)
			self.screen.blit(elements[0].image, elements[1])


	def update(self):

		# maintain 60 hz
		self.clock.tick(60)
		self.screen.fill((0, 255, 255))
		self.draw_screen()

		mouse = pygame.mouse.get_pos()


		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				exit()

		# updates screen
		pygame.display.flip()


resoursa = Resoursa()
while True:
	resoursa.update()