from tkinter import *
from settings import *
from player import Player
from game import Game
from mini_map import MiniMap


# инициализация
def main():
    root = Tk()
    root.geometry(f'{WIDTH}x{HEIGHT}')
    root.config(bg=BLACK)

    main_canvas = Canvas(root, bg=BLACK, width=WIDTH, height=HEIGHT)
    main_canvas.place(x=0, y=0)

    player = Player()

    mini_map_canvas = Canvas(root, bg=BLACK, width=MINI_MAP_WIDTH, height=MINI_MAP_HEIGHT)
    mini_map_canvas.place(x=MINI_MAP_POS[0], y=MINI_MAP_POS[1])

    mini_map = MiniMap(mini_map_canvas, player)
    game = Game(main_canvas, player, mini_map)

    game.drawing()
    root.mainloop()


if __name__ == '__main__':
    main()
