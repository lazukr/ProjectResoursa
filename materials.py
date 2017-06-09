# materials.py contains all the outline
# to the fundamentals of all materials
import pygame
import ast
import decimal as Decimal
from random import randint

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


# def rect(self, size):
#     width, height = size
#     this_rect = pygame.Rect((0, 0, width, height))
#     return this_rect



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
        return ("Id: %s, Type: %s, Temperature: %s, Volume: %s \nProperties: %s" %
                 (self.id, self.type, self.temperature, self.volume, self.properties))


    def get_property_str(self):
        return ("Material Class: %s\nMaterial Name: %s\nTemperature: %s\nVolume: %s" %
                (self.type, self.material, self.temperature, self.volume))




# class Wood(Material):
#     def __init__(self, unique_id, material):
#         super(Wood, self).__init__(unique_id, "Wood", material)


class Metal(Material):
    def __init__(self, unique_id, material):
        super(Metal, self).__init__(unique_id, "Metal", material)



# class Alloy(Metal):
#     def __init__(self, metal_1, metal_2):
#         total_volume = metal_1.volume + metal_2.volume
#         metal_1_ratio = round(Decimal(metal_1.volume / total_volume), 4)
#         metal_2_ratio = round(Decimal(1 - metal_1_ratio), 4)
#         name = metal_1.name + str(metal_1_ratio) + "-" + metal_2.name + str(metal_2_ratio)
#         melt_affinity = (metal_1.melt_affinity + metal_2.melt_affinity) / 2
#         melting_point = Decimal(metal_1.melting_point)*(Decimal(metal_1_ratio) ** Decimal(metal_1.melt_affinity)) \
#                      + Decimal(metal_2.melting_point)*(1 - Decimal(metal_1_ratio) ** Decimal(metal_2.melt_affinity)) 
#         super(Alloy, self).__init__(name, melt_affinity, melting_point, total_volume)





if __name__ == "__main__":
    all_materials = []
    counter = 0
    for x in MATERIALS:
        all_materials.append(Material(counter, x))
        counter += 1

    for materials in all_materials:
        print vars(materials)