# materials.py contains all the outline
# to the fundamentals of all materials

import random
import pygame_sdl2
pygame_sdl2.import_as_pygame()
import pygame

MATERIALS_WOOD = {
	"Oak": {
		"size": ((4, 16)),
		"width_deviation": 0,
		"height_deviation": 1,
		"colour": (79, 36, 18)
	},
	"Birch": {
		"size": ((6, 27)),
		"width_deviation": 1,
		"height_deviation": 2,
		"colour": (51, 45, 30)
	}
}


def rect(self, size, colour):
	surface = pygame.Surface(size)
	surface.fill(colour)
	return surface



class Wood():
	def __init__(self, unique_id, material):
		self.id = unique_id
		self.material = material
		self.size = MATERIALS_WOOD[material]["size"]
		self.colour = MATERIALS_WOOD[material]["colour"]
		self.image = rect(self, self.size, self.colour)

