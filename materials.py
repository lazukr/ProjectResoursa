# materials.py contains all the outline
# to the fundamentals of all materials
from __future__ import division
import pygame
import ast
from decimal import Decimal
from random import randint
import math


# dictionary for materials
MATERIALS = {}

# keys to properties
PROPERTY_KEYS = []
with open("material_properties.txt") as f:
    for line in f:

        # detect all the properties
        if line.startswith("$"):
            this_line = line[2:].split(',')           
            for elements in [[x.strip() for x in properties.split('=')] for properties in this_line]:
                PROPERTY_KEYS.append(elements[1])


        elif line.startswith("%"):
            pass
        elif line.startswith("&"):
            pass
        # detect all the materials
        elif not line.startswith("#"):
            this_line = line.split()
            MATERIALS[this_line[0]] = dict(zip(PROPERTY_KEYS[1:], this_line[1:]))


class Material(object):
    def __init__(self, unique_id, material_class, material):
        self.id = unique_id
        self.type = material_class
        self.material = material
        self.temperature = 300
        self.properties = {}
        for properties in PROPERTY_KEYS[1:]:
            self.properties[properties] = ast.literal_eval(MATERIALS[material][properties])
        w, h = self.properties["size"]
        w_dev_max, h_dev_max = self.properties["size_deviation"]
        w_dev = randint(0, w_dev_max)
        h_dev = randint(0, h_dev_max)
        self.properties["size"] = (w + w_dev, h + h_dev)
        self.volume = self.properties["size"][0]* self.properties["size"][1]
        self.image = pygame.Rect((0, 0), self.properties["size"])


    def __str__(self):
        return ("Id: %s, Type: %s, Material: %s, Temperature: %s, Volume: %s \nProperties: %s" %
                 (self.id, self.type, self.material, self.temperature, self.volume, self.properties))


    def get_property_str(self):
        return ("Material Class: %s\nMaterial Name: %s\nTemperature: %s\nVolume: %s\nColour: %s" %
                (self.type, self.material, self.temperature, self.volume, self.properties["colour"]))




# class Wood(Material):
#     def __init__(self, unique_id, material):
#         super(Wood, self).__init__(unique_id, "Wood", material)


class Metal(Material):
    def __init__(self, unique_id, material):
        super(Metal, self).__init__(unique_id, "Metal", material)



class Alloy(Metal):
    def __init__(self, metal_1, metal_2):
        super(Alloy, self).__init__(metal_1.id, metal_1.material)

        # find the metal with the lower melting point
        low_mp_metal = metal_1
        high_mp_metal = metal_2

        if metal_1.properties["melting_point"] > metal_2.properties["melting_point"]:
            low_mp_metal = metal_2
            high_mp_metal = metal_1


        low_mp_metal_ma = low_mp_metal.properties["melting_affinity"]
        high_mp_metal_ma = high_mp_metal.properties["melting_affinity"]
        low_mp_metal_mp = low_mp_metal.properties["melting_point"]
        high_mp_metal_mp = high_mp_metal.properties["melting_point"]


        self.volume = low_mp_metal.volume + high_mp_metal.volume
        
        low_mp_ratio = round(Decimal(low_mp_metal.volume / self.volume), 4)
        high_mp_ratio = round(Decimal(1 - low_mp_ratio), 4)
        self.material = low_mp_metal.material + str(low_mp_ratio) + "-" + high_mp_metal.material + str(high_mp_ratio)
        self.properties["melting_affinity"] = (low_mp_metal_ma + high_mp_metal_ma) / 2
        self.properties["melting_point"]  = int(Decimal(low_mp_metal_mp)*(Decimal(low_mp_ratio) ** Decimal(low_mp_metal_ma)) \
                                        + Decimal(high_mp_metal_mp)*(1 - Decimal(low_mp_ratio) ** Decimal(high_mp_metal_ma)))

        r1,g1,b1 = low_mp_metal.properties["colour"]
        r2,g2,b2 = high_mp_metal.properties["colour"]

        r = int(Decimal(r1)*Decimal(low_mp_ratio)) + int(Decimal(r2)*Decimal(high_mp_ratio))
        g = int(Decimal(g1)*Decimal(low_mp_ratio)) + int(Decimal(g2)*Decimal(high_mp_ratio))
        b = int(Decimal(b1)*Decimal(low_mp_ratio)) + int(Decimal(b2)*Decimal(high_mp_ratio))

        h = math.ceil(math.sqrt(self.volume))
        w = math.floor(math.sqrt(self.volume))

        self.properties["colour"] = (r,g,b)
        self.properties["size"] = (int(w), int(h))
        self.volume = int(w*h)
        self.image = pygame.Rect((0, 0), self.properties["size"])





if __name__ == "__main__":
    all_materials = []
    counter = 0
    for x in MATERIALS:
        all_materials.append(Metal(counter, x))
        counter += 1

    all_materials.append(Alloy(all_materials[0], all_materials[1]))

    for materials in all_materials:
        print vars(materials)



