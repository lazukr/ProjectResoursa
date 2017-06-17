import pygame, thorpy
from materials import Metal, MATERIALS, Alloy
from random import randint
pygame.font.init()
pygame.display.init()



class Inventory(object):

    def __init__(self, max_inv_size=5, set_location=(0,100)):
        self.max_inv_size = max_inv_size
        self.items_in_inv = []
        self.first_render(set_location)
        
    def add_item(self, item, index=-1):

        # if index is greater than -1, then we assume we are inserting
        print "adding material: ", item.material
        cur_inv_count = len(self.items_in_inv)
        if cur_inv_count < self.max_inv_size:
            if index > -1:
                cur_inv_count = index
            else:
                self.items_in_inv.append(item)
    
            self.item_clickables[cur_inv_count].set_text(str(item.material))
            self.item_clickables[cur_inv_count].add_basic_help(item.get_property_str())
            self.item_clickables[cur_inv_count].scale_to_title()

            # due to the implementation of add_basic_help(), they only add the reaction
            # after it has been hovered. To prevent remove_help() from being unable to find
            # the reaction to delete, we force the add_basic_help()'s reaction to be added here
            self.item_clickables[cur_inv_count].add_reaction(self.item_clickables[cur_inv_count]._help_reaction)
            self.item_clickables[cur_inv_count].center(axis=(True, False), element=self.inv_box)
            self.item_box.fit_children()
            self.inv_box.fit_children()
            return True
        else:
            return False

    def get_items(self):
        return_list = []
        for item in self.items_in_inv:
            return_list.append(item.material)

        return return_list

    def _add_to_smelter(self, event, item):
        if event.el == item and not event.el.get_text() == "None":
            index = self.item_clickables.index(event.el)
            if self.smelter.add_item(self.items_in_inv[index]):
                self._delete_item(index)
            
    def _print_all(self):
        print "* * * * *   R U N N I N G   P R I N T   A L L   F U N C   * * * * *"
        print "* * * * *                                                 * * * * *"
        print "* * * * *                                                 * * * * *"
        print "* * * * *                                                 * * * * *"
        print "* * * * *                                                 * * * * *"
        print "* * * * *                                                 * * * * *"
        print "* * * * *                                                 * * * * *"
        for val, el in enumerate(self.item_clickables):
            print "__item#%d__" % val
            print el._reactions
            print el._help_reaction
            print el._help_blitted



    def first_render(self, location):
        self.elements = []
        self.elements.append(thorpy.make_text("Inventory"))
        self.item_clickables = [thorpy.Clickable.make("None") for x in range(self.max_inv_size)]
        self.item_box = thorpy.Box.make(elements=self.item_clickables)
        self.elements.append(self.item_box)
        self.button = thorpy.make_button("Inv", func=self._print_all)
        self.elements.append(self.button)
        self.inv_box = thorpy.Box.make(elements=self.elements)
        self.inv_drag = thorpy.Draggable.make(elements=[self.inv_box])


        for item in self.item_clickables:
            item.center(axis=(True, False), element=self.inv_box)
            
            # this reaction allows us to click the item we want to smelt
            # and transfer it into the smelter
            reaction = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                            reac_func=self._add_to_smelter,
                            params={"item": item},
                            event_args={"id":thorpy.constants.EVENT_PRESS})
            self.inv_drag.add_reaction(reaction)

        self.inv_drag.set_topleft(location)
        self.inv_menu = thorpy.Menu(self.inv_drag)
        thorpy.functions.set_current_menu(self.inv_menu)
        self.inv_menu.blit_and_update()

    def _delete_item(self, index):
        # grab number of items
        num_of_items = len(self.items_in_inv)

        # reset the last item to None as everything will be pushed up one
        # also reset the tooltip (undoes add_basic_help)
        self.item_clickables[num_of_items-1].set_text("None")
        self.item_clickables[num_of_items-1].remove_help()
        
        # delete the element from data
        del self.items_in_inv[index]
        
        # update the view
        for x in range(index, num_of_items - 1):
            self.add_item(self.items_in_inv[x], index=x)

            
    def render(self):
        self.inv_menu.blit_and_update()

    def react(self, event):
        self.inv_menu.react(event)

    def link_smelter(self, smelter):

        # this allows us to link the smelter so 
        # we can reference to it
        self.smelter = smelter


class Smelter(object):

    def __init__(self, max_inv_size=2, set_location=(0,300)):
        self.max_inv_size = 2
        self.items_in_smelt = []
        self.item_in_result = None
        self.first_render(set_location)

    def first_render(self, location):
        self.elements = []
        self.elements.append(thorpy.make_text("Smelter"))
        self.smelt_items = [thorpy.Clickable.make("None") for x in range(self.max_inv_size)]
        self.button = thorpy.make_button("Smelt", func=self.smelt)
        self.smelt_item_box = thorpy.Box.make(elements=self.smelt_items)
        self.elements.append(self.smelt_item_box)
        self.elements.append(self.button)

        self.smelted_item = thorpy.Clickable.make("None")
        self.smelted_item_box = thorpy.Box.make(elements=[self.smelted_item])
        self.elements.append(self.smelted_item_box)
        self.box = thorpy.Box.make(elements=self.elements)
        self.drag = thorpy.Draggable.make(elements=[self.box])

        reaction = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                            reac_func=self._pop_smelter,
                            params={"item": self.smelted_item},
                            event_args={"id":thorpy.constants.EVENT_PRESS})



        for item in self.elements:
            item.center(axis=(True, False), element=self.box)

        self.drag.add_reaction(reaction)
        self.drag.set_topleft(location)
        self.sub_menu = thorpy.Menu(self.drag)
        thorpy.functions.set_current_menu(self.sub_menu)
        self.sub_menu.blit_and_update()


    def _del_all(self):
        self.items_in_smelt = []
        for el in self.smelt_items:
            el.set_text("None")
            el.remove_help()


    def _pop_smelter(self, event, item):
        if event.el == item and self.item_in_result:
            print item
            location = (randint(150, self.screen_size[0]), randint(0, self.screen_size[1]))
            self.item_in_result.image.move_ip(location)
            self.list["list"].append(self.item_in_result)
            self.list["count"] += 1
            self.items_in_result = None
            item.set_text("None")
            item.remove_help()
            item.scale_to_title()
            item.center(axis=(True, False), element=self.box)
            self.smelted_item_box.fit_children()
            self.box.fit_children()


    def add_item(self, item):
        cur_inv_count = len(self.items_in_smelt)
        if cur_inv_count < self.max_inv_size:
            self.items_in_smelt.append(item)
            self.smelt_items[cur_inv_count].set_text(str(item.material))
            self.smelt_items[cur_inv_count].add_basic_help(item.get_property_str())
            self.smelt_items[cur_inv_count].add_reaction(self.smelt_items[cur_inv_count]._help_reaction)
            self.smelt_items[cur_inv_count].scale_to_title()
            self.smelt_items[cur_inv_count].center(axis=(True, False), element=self.box)
            self.smelt_item_box.fit_children()
            self.box.fit_children()
            return True
        else:
            return False

    def smelt(self):
        print "smelting"
        for el in self.items_in_smelt:
            print el.get_property_str()

        if len(self.items_in_smelt) == self.max_inv_size:
            item = Alloy(self.items_in_smelt[0], self.items_in_smelt[1])
            self.item_in_result = item
            self.smelted_item.set_text(str(item.material))
            self.smelted_item.add_basic_help(item.get_property_str())
            self.smelted_item.add_reaction(self.smelted_item._help_reaction)
            self.smelted_item.scale_to_title()
            self.smelted_item.center(axis=(True, False), element=self.box)
            self.smelted_item_box.fit_children()
            self.box.fit_children()
            self._del_all()
        


    def render(self):
        self.sub_menu.blit_and_update()

    def react(self, event):
        self.sub_menu.react(event)

    def link_list(self, rect_list, screen_size):
        self.list = rect_list
        self.screen_size = screen_size