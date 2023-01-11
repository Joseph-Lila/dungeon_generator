import enum


class WallKind(enum.Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Wall:
    def __init__(self, kind: WallKind, col: int, row: int):
        self.kind = kind
        self.col = col
        self.row = row
