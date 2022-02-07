from tkinter import *
from settings import *
from player import Player
from drawing import Drawing


# инициализация
root = Tk()
screen = Canvas(root, bg=BLACK, width=WIDTH, height=HEIGHT)
screen.pack()
player = Player(screen)
drawing = Drawing(screen, player)


def main():
    drawing.drawing()
    root.mainloop()


if __name__ == '__main__':
    main()
