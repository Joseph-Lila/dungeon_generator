import math

from domain.layer import Layer
from rich.table import Table

from domain.wall import WallKind

DEFAULT_LAYERS_STRUCTURE = (
    (10, 10),
    (7, 7),
    (4, 4),
    (1, 1),
)


class Dungeon:
    def __init__(
            self,
            layers_structure=DEFAULT_LAYERS_STRUCTURE,
            optional_walls_part: float = 1,
            altars_part=.1,
            chests_part=.3,
            console=None
    ):
        self._layers_structure = layers_structure
        self._layers = []
        for i, layer_structure in enumerate(self._layers_structure):
            cols, rows = layer_structure
            altars_cnt = math.floor(altars_part * cols * rows)
            chests_cnt = math.floor(chests_part * cols * rows)
            portals_cnt = 1 if i == (len(layers_structure) - 1) else 2
            layer = Layer(cols, rows, optional_walls_part, altars_cnt, chests_cnt, portals_cnt)
            self._layers.append(layer)
        self._console = console
        self._secret_symbol = '+'
        self._inner_width = 5

    def _print_top_construction(self, col, row, layer_ind):
        wall = f'{self._secret_symbol}{"-" * self._inner_width}{self._secret_symbol}' \
            if col == 0 \
            else f'{"-" * self._inner_width}{self._secret_symbol}'
        without_wall = f'{self._secret_symbol}{" " * self._inner_width}{self._secret_symbol}' \
            if col == 0 \
            else f'{" " * self._inner_width}{self._secret_symbol}'
        top_wall_exists = self._layers[layer_ind].check_wall_exists(WallKind.VERTICAL, col, row)
        ans = wall if top_wall_exists else without_wall
        self._console.print(ans, end='')

    def _print_middle_construction(self, col, row, layer_ind):
        content_symbol = self._layers[layer_ind].get_room(col, row).content.value
        two_walls = f'|{content_symbol:^{self._inner_width}}|' \
            if col == 0 \
            else f'{content_symbol:^{self._inner_width - 1}}|'
        left_wall = f'|{content_symbol:^{self._inner_width}} ' \
            if col == 0 \
            else f'{content_symbol:^{self._inner_width - 1}} '
        right_wall = f' {content_symbol:^{self._inner_width - 1}}|' \
            if col == 0 \
            else f'{content_symbol:^{self._inner_width - 1}}|'
        no_walls = f' {content_symbol:^{self._inner_width - 1}} ' \
            if col == 0 \
            else f'{content_symbol:^{self._inner_width - 1}} '
        left_wall_exists = self._layers[layer_ind].check_wall_exists(WallKind.HORIZONTAL, col, row)
        right_wall_exists = self._layers[layer_ind].check_wall_exists(WallKind.HORIZONTAL, col + 1, row)
        ans = two_walls if \
            left_wall_exists and right_wall_exists \
            else left_wall \
            if left_wall_exists \
            else right_wall \
            if right_wall_exists \
            else no_walls
        self._console.print(ans, end='')

    def _print_bottom_construction(self, col, row, layer_ind):
        wall = f'{self._secret_symbol}{"-" * self._inner_width}{self._secret_symbol}' \
            if col == 0 \
            else f'{"-" * self._inner_width}{self._secret_symbol}'
        without_wall = f'{self._secret_symbol}{" " * self._inner_width}{self._secret_symbol}' \
            if col == 0 \
            else f'{" " * self._inner_width}{self._secret_symbol}'
        top_wall_exists = self._layers[layer_ind].check_wall_exists(WallKind.VERTICAL, col, row + 1)
        ans = wall if top_wall_exists else without_wall
        self._console.print(ans, end='')

    def print_info(self):
        table = Table(title='Dungeon')

        table.add_column("Layer No.", style='red', no_wrap=True)
        table.add_column("Rows", style='cyan', no_wrap=True)
        table.add_column("Cols", style='magenta', no_wrap=True)
        table.add_column("Walls %", style='green', justify="right")

        for i, layer in enumerate(self._layers, start=1):
            table.add_row(
                str(i),
                str(layer.rows),
                str(layer.cols),
                str(layer.filled_part),
            )
        self._console.print(table)

    def print_layers(self):
        if self._console:
            for i, layer in enumerate(self._layers, start=1):
                self._console.rule(f"[orange] Layer {i}")

                cols, rows = self._layers_structure[i-1]
                for row in range(rows):
                    if row == 0:
                        for col in range(cols):
                            self._print_top_construction(col, row, i - 1)
                        self._console.print('', end='\n')
                    for col in range(cols):
                        self._print_middle_construction(col, row, i - 1)
                    self._console.print('', end='\n')
                    for col in range(cols):
                        self._print_bottom_construction(col, row, i - 1)
                    self._console.print('', end='\n')
