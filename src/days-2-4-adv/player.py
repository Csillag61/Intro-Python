# Write a class to hold player information, e.g. what room they are in
# currently.


from item import LightSource


class Player:
    move_error_msg = "You can not go that way! \n"

    def __init__(self, name, room):
        self.name = name
        self.room = room
        self.score = 0
        self.items = []

    def move(self, direction):
        next_room = self.room.get_room_in_direction(direction)
        if next_room:
            self.room = next_room
            if self.has_light_source() or next_room.has_light_source() or next_room.lit:
                print(next_room)
                next_room.room_items()
            else:
                print("Do you need some light?")
        else:
            print('That is not a valid direction.')

    def look(self, direction):
        next_room = self.room.get_room_in_direction(direction)
        if next_room:
            print(next_room)
        else:
            print('There is nothing there')

    def get_item(self, item):
        if self.has_light_source() or self.room.has_light_source() or self.room.lit:
            if len(self.room.items) > 0:
                found_item = list(
                    filter(lambda i: i.name.lower() == item, self.room.items))
                if len(found_item) > 0:
                    self.items.append(found_item[0])
                    self.room.remove_item(found_item[0])
                    found_item[0].on_take(self)
                    print(f'You picked up a {found_item[0].name}. \n')
                    self.room.room_items()
                else:
                    print('There is no such item, please try again.')
        else:
            print('Good luck finding that!')

    def drop_item(self, item):
        if len(self.items) > 0:
            found_item = list(
                filter(lambda i: i.name.lower() == item, self.items))
            if len(found_item) > 0:
                if found_item[0].on_drop():
                    self.items.remove(found_item[0])
                    self.room.add_item(found_item[0])
                    print(f'You dropped a {found_item[0].name}. \n')
                    self.room.room_items()
            else:
                print('There is no such item, please try again.')

    def list_items(self):
        if self.has_items():
            print('Your inventory:')
            for i in self.items:
                print(i)
        else:
            print('Your inventory is empty.')

    def has_items(self):
        if len(self.items) > 0:
            return True
        return False

    def has_light_source(self):
        return any(isinstance(item, LightSource) for item in self.items)
