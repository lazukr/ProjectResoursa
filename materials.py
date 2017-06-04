# materials.py contains all the outline
# to the fundamentals of all materials
import pygame
import ast

# dictionary for materials
MATERIALS_WOOD = {}

# keys to properties
PROPERTY_KEYS = []
with open("material_properties.txt") as f:
    for line in f:

        # detect all the properties
        if line.startswith("$"):
            this_line = line[2:].split(',')           
            for elements in [[x.strip() for x in properties.split('=')] for properties in this_line]:
                PROPERTY_KEYS.append(elements[1])

        # detect all the materials
        elif not line.startswith("#"):
            this_line = line.split()
            MATERIALS_WOOD[this_line[0]] = dict(zip(PROPERTY_KEYS[1:], this_line[1:]))


def rect(self, size, colour):
    surface = pygame.Surface(size)
    surface.fill(colour)
    return surface



class Wood():
    def __init__(self, unique_id, material):
        self.id = unique_id
        self.material = material
        self.properties = {}
        for properties in PROPERTY_KEYS[1:]:
            self.properties[properties] = ast.literal_eval(MATERIALS_WOOD[material][properties])
        self.image = rect(self, self.properties["size"], self.properties["colour"])



if __name__ == "__main__":
    aWood = Wood(1, "Oak")
    print vars(aWood)