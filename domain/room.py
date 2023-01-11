import enum


class RoomContent(enum.Enum):
    ALTAR = '✨'
    PORTAL = '🌌'
    CHEST = '🧰'
    NO_CONTENT = '❌'


class Room:
    def __init__(self, col, row):
        self.col, self.row = col, row
        self._visited = False
        self._content = RoomContent.NO_CONTENT

    @property
    def content(self):
        return self._content

    @property
    def visited(self):
        return self._visited

    def add_content(self, content: RoomContent):
        self._content = content

    def mark_as_visited(self):
        self._visited = True

    def __str__(self):
        return f"{self.col}:{self.row}"
