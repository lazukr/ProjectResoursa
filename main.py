import pygame, thorpy
from materials import Metal, MATERIALS
from random import randint
import math
from submenu import Inventory, Smelter

thorpy.application.DEBUG_MODE = True

SCREEN_SIZE = (640, 480)
GENERATION_TRIES = 100

class Game(object):
    def __init__(self, dim=SCREEN_SIZE, fps=60):
        self.dim = dim
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.screen = None
        self.items = {
            "count": 0,
            "list": []
        }

    def start(self):
        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.dim)
        self.first_render()
        is_running = True
        while is_running:
            self.clock.tick(self.fps)
            tick = self.clock.get_time()
            this_event = pygame.event.Event(thorpy.constants.THORPY_EVENT,
            id=thorpy.constants.EVENT_TIME, tick=tick)
            pygame.event.post(this_event)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down()
                self.on_event(event)
                self.render()
            pygame.display.flip()
        pygame.quit()

class Resoursa(Game):
    def __init__(self):

        # initialization
        super(Resoursa, self).__init__()
        pygame.display.set_caption("Resoursa")
        self.world_start()

    def world_start(self):
        generation_parameters = {}
        with open("world_gen.txt") as f:
            for line in f:
                (name, probability) = line.split()
                generation_parameters[name] =  int(float(probability)*GENERATION_TRIES)
        # print generation_parameters

        for materials, amount in generation_parameters.items():
            print materials, amount
            for x in range(amount):
                location = (randint(150, SCREEN_SIZE[0]), randint(0, SCREEN_SIZE[1]))
                this_item = Metal(self.items["count"], materials)
                this_item.image.move_ip(location)
                self.items["list"].append(this_item)
                self.items["count"] += 1
        # print(self.items)

        


    def combine(self):
        items = [checker.get_text() for checker in self.checkers if checker.get_value() ]
        print 'Combining: {}'.format(items)

        if set(items).issubset(set(self.inventory.get_items())):
            print "hey"


    def draw_items(self):
        display_objects = self.items["list"]
        for elements in display_objects:
            pygame.draw.rect(self.screen, elements.properties["colour"], elements.image)

    def draw_gui(self):
        self.inventory = Inventory()
        self.smelter = Smelter()
        self.inventory.link_smelter(self.smelter)
        self.smelter.link_list(self.items, SCREEN_SIZE)

        # self.checkers = [thorpy.Checker.make(resource, value=False) for resource in MATERIALS.keys()]
        # button = thorpy.make_button("Combine", func=self.combine)
        # elements = []
        # elements += self.checkers 
        # elements.append(button)
        # box = thorpy.Box.make(elements=elements)

        # box.set_topleft((0,0))
        # self.menu = thorpy.Menu(box)
        # thorpy.functions.set_current_menu(self.menu)
        # self.menu.blit_and_update()


    def first_render(self):
        self.draw_items()
        self.draw_gui()

    def render(self):
        self.screen.fill((255, 255, 255))
        self.draw_items()
       # self.menu.blit_and_update()
        self.inventory.render()
        self.smelter.render()      

    def on_event(self, event):
        #self.menu.react(event)
        self.inventory.react(event)
        self.smelter.react(event)

    def mouse_down(self):
        mw, mh = pygame.mouse.get_pos()
        for element in self.items["list"]:
            if element.image.collidepoint(mw, mh):
                print element
                if self.inventory.add_item(element):
                    self.items["list"].remove(element)




if __name__ == "__main__":
    resoursa = Resoursa()
    resoursa.start()

