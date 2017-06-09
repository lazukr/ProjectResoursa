import pygame, thorpy
from materials import Metal, MATERIALS
from random import randint
import math

SCREEN_SIZE = (640, 480)
GENERATION_TRIES = 100

class Game(object):
    def __init__(self, dim=SCREEN_SIZE, fps=30):
        self.dim = dim
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.screen = None
        self.items = {
            "count": 0,
            "list": []
        }
        self.inventory = []
        self.max_inv = 5

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
                location = (randint(0, SCREEN_SIZE[0]), randint(0, SCREEN_SIZE[1]))
                this_item = Metal(self.items["count"], materials)
                this_item.image.move_ip(location)
                self.items["list"].append(this_item)
                self.items["count"] += 1
        # print(self.items)

        


    def combine(self):
        items = [checker.get_text() for checker in self.checkers if checker.get_value() ]
        print 'Combining: {}'.format(items)

    def draw_items(self):
        display_objects = self.items["list"]
        for elements in display_objects:
            pygame.draw.rect(self.screen, elements.properties["colour"], elements.image)

    def draw_gui(self):
        self.checkers = [thorpy.Checker.make(resource, value=False) for resource in MATERIALS.keys()]
        self.inv_display = [thorpy.Clickable.make("None") for x in range(self.max_inv)]
        button = thorpy.make_button("Combine", func=self.combine)
        elements = []
        elements += self.checkers 
        elements.append(button)
        self.inv_box = thorpy.Box.make(elements=self.inv_display)
        self.inv_box.fit_children(margins=(10,10))
        self.inv_drag = thorpy.Draggable.make(elements=[self.inv_box])

        self.box = thorpy.Box.make(elements=elements)
        self.menu = thorpy.Menu(self.box)
        self.inv_menu = thorpy.Menu(self.inv_drag)


        for element in self.menu.get_population():
            element.surface = self.screen

        for element in self.inv_menu.get_population():
            element.surface = self.screen

        self.box.set_topleft((0,0))
        self.box.blit()
        self.box.update()

        self.inv_drag.set_topleft((100,100))
        self.inv_drag.blit()
        self.inv_drag.update()

        thorpy.functions.set_current_menu(self.menu)
        thorpy.functions.set_current_menu(self.inv_menu)



    def first_render(self):
        self.draw_items()
        self.draw_gui()

    def render(self):
        self.screen.fill((255, 255, 255))
        self.draw_items()
        self.inv_drag.unblit_and_reblit()
        self.box.unblit_and_reblit()
        

    def on_event(self, event):
        self.menu.react(event)
        self.inv_menu.react(event)

    def mouse_down(self):
        mw, mh = pygame.mouse.get_pos()
        for elements in self.items["list"]:
            if elements.image.collidepoint(mw, mh):
                print elements
                cur_inv_stock = len(self.inventory)
                if cur_inv_stock < self.max_inv:
                    self.inventory.append(elements)
                    self.inv_display[cur_inv_stock].set_text(str(elements.id))
                    self.inv_display[cur_inv_stock].add_basic_help(elements.get_property_str())




if __name__ == "__main__":
    resoursa = Resoursa()
    resoursa.start()

