import enum
import math
from dataclasses import dataclass
from random import choice, shuffle
from typing import List, Dict, Optional


class RoomContent(enum.Enum):
    ALTAR = 'ALTAR'
    PORTAL = 'PORTAL'
    CHEST = 'CHEST'
    NO_CONTENT = 'NO_CONTENT'


@dataclass(unsafe_hash=True)
class ColRow:
    col: int
    row: int


@dataclass(unsafe_hash=True)
class Pair:
    first: ColRow
    second: ColRow


class MyDungeon:
    def __init__(self):
        self.layers_structure: List[ColRow] = []
        self.optional_walls_part: float = 0
        self.altars_part: float = 0
        self.chests_part: float = 0
        self.layers: List[MyLayer] = []

    def build_layers(self):
        for index, arr_elem in enumerate(self.layers_structure):
            rows = arr_elem.row
            cols = arr_elem.col
            altars_cnt = math.floor(self.altars_part * rows * cols)
            chests_cnt = math.floor(self.chests_part * rows * cols)
            portals_cnt = 1 if index == len(self.layers_structure) - 1 or index == 0 else 2
            my_layer = MyLayer()
            my_layer.col_row = ColRow(cols, rows)
            my_layer.filled_part = self.optional_walls_part
            my_layer.altars_cnt = altars_cnt
            my_layer.chests_cnt = chests_cnt
            my_layer.portals_cnt = portals_cnt

            my_layer.build_rooms()
            my_layer.build_ideal_labyrinth()
            my_layer.tune_labyrinth()
            my_layer.allocate_content()

            self.layers.append(my_layer)


class MyRoom:
    def __init__(self):
        self.col_row: Optional[ColRow] = None
        self.visited = False
        self.content = None
        self.walls: set = set()

    def __str__(self):
        return f"({self.col_row.col}; {self.col_row.row}) {''.join(sorted(list(self.walls)))}"


class MyLayer:
    def __init__(self):
        self.col_row: Optional[ColRow] = None
        self.filled_part = 0
        self.altars_cnt = 0
        self.chests_cnt = 0
        self.portals_cnt = 0
        self.rooms: Dict[ColRow, MyRoom] = dict()

    def get_rooms(self):
        for room in self.rooms.values():
            print(room)

    def build_rooms(self):
        for col in range(self.col_row.col):
            for row in range(self.col_row.row):
                col_row = ColRow(col, row)
                room = MyRoom()
                room.walls = set('BLRT')
                room.col_row = col_row
                room.visited = False
                self.rooms[col_row] = room

    def build_ideal_labyrinth(self):
        initial_col_row = ColRow(0, 0)
        cur_room = self.rooms[initial_col_row]
        stack = []
        loop_flag = True
        while loop_flag:
            cur_room.visited = True
            next_room = self.check_neighbors(cur_room)
            if next_room:
                next_room.visited = True
                stack.append(cur_room)
                self.remove_wall(cur_room, next_room)
                cur_room = next_room
            elif stack:
                cur_room = stack.pop()
            else:
                loop_flag = False

    def check_neighbors(self, cur_room: MyRoom):
        neighbors: List[MyRoom] = []
        top_col_row = ColRow(cur_room.col_row.col, cur_room.col_row.row - 1)
        right_col_row = ColRow(cur_room.col_row.col + 1, cur_room.col_row.row)
        bottom_col_row = ColRow(cur_room.col_row.col, cur_room.col_row.row + 1)
        left_col_row = ColRow(cur_room.col_row.col - 1, cur_room.col_row.row)

        top_room: MyRoom = self.rooms.get(top_col_row, False)
        right_room: MyRoom = self.rooms.get(right_col_row, False)
        bottom_room: MyRoom = self.rooms.get(bottom_col_row, False)
        left_room: MyRoom = self.rooms.get(left_col_row, False)

        if top_room and not top_room.visited:
            neighbors.append(top_room)
        if right_room and not right_room.visited:
            neighbors.append(right_room)
        if bottom_room and not bottom_room.visited:
            neighbors.append(bottom_room)
        if left_room and not left_room.visited:
            neighbors.append(left_room)

        if len(neighbors) == 0:
            return False
        else:
            return choice(neighbors)

    @staticmethod
    def remove_wall(cur_room: MyRoom, next_room: MyRoom):
        dx = cur_room.col_row.col - next_room.col_row.col
        dy = cur_room.col_row.row - next_room.col_row.row

        if dx == 1:
            cur_room.walls.remove('L')
            next_room.walls.remove('R')
        elif dx == - 1:
            cur_room.walls.remove('R')
            next_room.walls.remove('L')
        if dy == 1:
            cur_room.walls.remove('T')
            next_room.walls.remove('B')
        elif dy == -1:
            cur_room.walls.remove('B')
            next_room.walls.remove('T')

    def tune_labyrinth(self):
        optional_walls: List[Pair] = []
        for col in range(self.col_row.col):
            for row in range(self.col_row.row):
                cur_col_row = ColRow(col, row)
                right_col_row = ColRow(col + 1, row)
                down_col_row = ColRow(col, row + 1)
                room = self.rooms[cur_col_row]
                if 'R' in room.walls and cur_col_row.col != self.col_row.col - 1:
                    pair = Pair(cur_col_row, right_col_row)
                    optional_walls.append(pair)
                if 'D' in room.walls and cur_col_row.row != self.col_row.row - 1:
                    pair = Pair(cur_col_row, down_col_row)
                    optional_walls.append(pair)
        shuffle(optional_walls)
        optional_walls_quantity = len(optional_walls)
        walls_quantity_to_remove = optional_walls_quantity - math.ceil(
            optional_walls_quantity * self.filled_part
        )
        while walls_quantity_to_remove != 0:
            wall_to_remove = optional_walls.pop(0)
            one_room = self.rooms[wall_to_remove.first]
            another_room = self.rooms[wall_to_remove.second]
            self.remove_wall(one_room, another_room)
            walls_quantity_to_remove -= 1

    def allocate_content(self):
        rooms_without_content = [room for room in self.rooms.values()]
        shuffle(rooms_without_content)
        rooms_without_content_cnt = len(rooms_without_content)
        altars_cnt = self.altars_cnt
        chests_cnt = self.chests_cnt
        portals_cnt = self.portals_cnt
        while altars_cnt and rooms_without_content_cnt:
            room = rooms_without_content.pop(0)
            room.content = RoomContent.ALTAR
            altars_cnt -= 1
            rooms_without_content_cnt -= 1
        while chests_cnt and rooms_without_content_cnt:
            room = rooms_without_content.pop(0)
            room.content = RoomContent.CHEST
            chests_cnt -= 1
            rooms_without_content_cnt -= 1
        while portals_cnt and rooms_without_content_cnt:
            room = rooms_without_content.pop(0)
            room.content = RoomContent.PORTAL
            portals_cnt -= 1
            rooms_without_content_cnt -= 1
        while rooms_without_content_cnt:
            room = rooms_without_content.pop(0)
            room.content = RoomContent.NO_CONTENT
            rooms_without_content_cnt -= 1


def create_dungeon():
    chests_part = .3
    altars_part = .3
    optional_walls_part = .65
    layers_structure: List[ColRow] = []

    for i in range(4):
        col_row = ColRow(i * 3 + 1, i * 3 + 1)
        layers_structure.append(col_row)

    dungeon = MyDungeon()
    dungeon.layers_structure = layers_structure
    dungeon.optional_walls_part = optional_walls_part
    dungeon.altars_part = altars_part
    dungeon.chests_part = chests_part

    dungeon.build_layers()

    dungeon.layers[1].get_rooms()


if __name__ == '__main__':
    create_dungeon()
