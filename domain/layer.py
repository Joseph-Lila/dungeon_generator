import math
from random import choice
from typing import Dict
from domain.room import Room, RoomContent
from domain.wall import Wall, WallKind
from random import shuffle


class Layer:
    def __init__(
            self,
            cols: int,
            rows: int,
            optional_walls_part: float = 1,
            altars_cnt=0,
            chests_cnt=0,
            portals_cnt=0
    ):
        self.cols: int = cols
        self.rows: int = rows
        self.filled_part = optional_walls_part
        self._altars_cnt = altars_cnt
        self._chests_cnt = chests_cnt
        self._portals_cnt = portals_cnt
        self._rooms: Dict[tuple, Room] = {
            (col, row): Room(col, row)
            for col in range(cols)
            for row in range(rows)
        }
        horizontal_walls: Dict[tuple, Wall] = {
            (WallKind.HORIZONTAL, col, row): Wall(WallKind.HORIZONTAL, col, row)
            for col in range(cols + 1)
            for row in range(rows)
        }
        vertical_walls: Dict[tuple, Wall] = {
            (WallKind.VERTICAL, col, row): Wall(WallKind.VERTICAL, col, row)
            for col in range(cols)
            for row in range(rows + 1)
        }
        self._walls = horizontal_walls | vertical_walls
        self._cur_room = self._rooms[(0, 0)]
        self._stack = []
        self._build_ideal_labyrinth()
        self._tune_labyrinth()
        self._add_content()

    def get_room(self, col, row):
        return self._rooms.get((col, row), None)

    def check_wall_exists(self, kind: WallKind, col, row: int) -> bool:
        return self._walls.get((kind, col, row), None) is not None

    def _add_content(self):
        rooms_without_content = [room for room in self._rooms.values()]
        shuffle(rooms_without_content)
        rooms_without_content_cnt = len(rooms_without_content)
        altars_cnt = self._altars_cnt
        chests_cnt = self._chests_cnt
        portals_cnt = self._portals_cnt
        while altars_cnt and rooms_without_content_cnt:
            room = rooms_without_content.pop(0)
            room.add_content(RoomContent.ALTAR)
            altars_cnt -= 1
            rooms_without_content_cnt -= 1
        while chests_cnt and rooms_without_content_cnt:
            room = rooms_without_content.pop(0)
            room.add_content(RoomContent.CHEST)
            chests_cnt -= 1
            rooms_without_content_cnt -= 1
        while portals_cnt and rooms_without_content_cnt:
            room = rooms_without_content.pop(0)
            room.add_content(RoomContent.PORTAL)
            portals_cnt -= 1
            rooms_without_content_cnt -= 1

    def _check_neighbors(self, cur_room):
        neighbors = []
        top = self._rooms.get((cur_room.col, cur_room.row - 1), False)
        right = self._rooms.get((cur_room.col + 1, cur_room.row), False)
        bottom = self._rooms.get((cur_room.col, cur_room.row + 1), False)
        left = self._rooms.get((cur_room.col - 1, cur_room.row), False)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False

    def _remove_wall(self, cur_room, next_room):
        dx = cur_room.col - next_room.col
        if dx == 1:
            self._walls.pop((WallKind.HORIZONTAL, cur_room.col, cur_room.row))
        elif dx == -1:
            self._walls.pop((WallKind.HORIZONTAL, next_room.col, next_room.row))
        dy = cur_room.row - next_room.row
        if dy == 1:
            self._walls.pop((WallKind.VERTICAL, cur_room.col, cur_room.row))
        elif dy == -1:
            self._walls.pop((WallKind.VERTICAL, next_room.col, next_room.row))

    def _build_ideal_labyrinth(self):
        while True:
            self._cur_room.mark_as_visited()
            next_room = self._check_neighbors(self._cur_room)
            if next_room:
                next_room.mark_as_visited()
                self._stack.append(self._cur_room)
                self._remove_wall(self._cur_room, next_room)
                self._cur_room = next_room
            elif self._stack:
                self._cur_room = self._stack.pop()
            else:
                break

    def _tune_labyrinth(self):
        optional_walls = [
            wall
            for key, wall in self._walls.items()
            if (key[0] == WallKind.HORIZONTAL and key[1] != 0 and key[1] != self.cols) or
               (key[0] == WallKind.VERTICAL and key[2] != 0 and key[2] != self.rows)
        ]
        shuffle(optional_walls)
        optional_walls_quantity = len(optional_walls)
        walls_quantity_to_remove = optional_walls_quantity - math.ceil(optional_walls_quantity * self.filled_part)
        while walls_quantity_to_remove != 0:
            wall_to_remove = optional_walls.pop(0)
            self._walls.pop((wall_to_remove.kind, wall_to_remove.col, wall_to_remove.row))
            walls_quantity_to_remove -= 1
