from rich.console import Console
from rich.terminal_theme import MONOKAI

from domain.dungeon import Dungeon


def main(console_instance):
    dungeon = Dungeon(
        console=console_instance,
        optional_walls_part=.65,
    )
    dungeon.print_info()
    dungeon.print_layers()


if __name__ == "__main__":
    console = Console(record=True)
    main(console)
    console.save_svg("example.svg", theme=MONOKAI)
