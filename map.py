from settings import *


MAP = [
    '111111111111',
    '1....2.....1',
    '1.......22.1',
    '1...1...22.1',
    '1..........1',
    '1...1......1',
    '1...1......1',
    '111111111111'
]

world_map = set()
mini_map = set()

for i, row in enumerate(MAP):
    for j, wall in enumerate(row):
        if wall != '.':
            # world_map[(j * SQUARE_SIDE, i * SQUARE_SIDE)] = wall
            world_map.add((j * SQUARE_SIDE, i * SQUARE_SIDE))
            mini_map.add((j * SQUARE_SIDE // MINI_MAP_SCALE, i * SQUARE_SIDE // MINI_MAP_SCALE))