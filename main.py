import pygame as pg
import numpy as np
import sys
import time


# initialization
pg.init()
clock = pg.time.Clock()

# set the main surface size
w, h = 1000, 1000
print(f"w: {w}, h: {h}")

scr = pg.display.set_mode((w, h))
pg.display.set_caption("GOL")

# set the background color
bg = (25, 25, 25)
print(f"bg: {bg}")

# set the number of cells along x and y axis
nx_c, ny_c = 100, 100
print(f"nx_c: {nx_c}, ny_c: {ny_c}")

# set the pixel length of cell along each axis
dim_w_c, dim_h_c = w / nx_c, h / ny_c
print(f"dim_w_c: {dim_w_c}, dim_h_c: {dim_h_c}")

# set the initial cell state, alive = 1, dead = 0
game_state = np.zeros((nx_c, ny_c))

# define basic automatas initial state
game_state[5, 3] = 1
game_state[5, 4] = 1
game_state[5, 5] = 1

game_state[21, 21] = 1
game_state[22, 22] = 1
game_state[22, 23] = 1
game_state[21, 23] = 1
game_state[20, 23] = 1

# set pause var
pause = False

while True:
    new_game_state = np.copy(game_state)
    scr.fill(bg)
    time.sleep(0.1)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            pause = not pause

        click = pg.mouse.get_pressed()
        if sum(click) > 0:
            px, py = pg.mouse.get_pos()
            cx, cy = int(np.floor(px / dim_w_c)), int(np.floor(py / dim_h_c))
            new_game_state[cx, cy] = int(not click[2])


    for y in range(0, nx_c):
        for x in range(0, ny_c):
            # compute the number for current cell close neighbors
            n_neigh =   game_state[(x-1) % nx_c, (y-1) % ny_c] + \
                        game_state[x     % nx_c, (y-1) % ny_c] + \
                        game_state[(x+1) % nx_c, (y-1) % ny_c] + \
                        game_state[(x-1) % nx_c,     y % ny_c] + \
                        game_state[(x+1) % nx_c,     y % ny_c] + \
                        game_state[(x-1) % nx_c, (y+1) % ny_c] + \
                        game_state[x     % nx_c, (y+1) % ny_c] + \
                        game_state[(x+1) % nx_c, (y+1) % ny_c]

            # cell poliygon 
            poly = [
                (x       * dim_w_c, y       * dim_h_c), 
                ((x + 1) * dim_w_c, y       * dim_h_c), 
                ((x + 1) * dim_w_c, (y + 1) * dim_h_c), 
                (x       * dim_w_c, (y + 1) * dim_h_c)
                ]

            if not pause:

                # 1. Any live cell with two or three live neighbours lives on to the next generation.
                if game_state[x, y] == 1 and n_neigh in [2, 3]:
                    new_game_state[x, y] = 1

                # 2. Any live cell with more than three live neighbours dies, as if by overpopulation.
                #if game_state[x, y] == 1 and n_neigh > 3:
                #    new_game_state[x, y] = 0

                # 3. Any dead cell with exactly three live neighbours becomes a live cell, reproduction
                if game_state[x, y] == 0 and n_neigh == 3:
                    new_game_state[x, y] = 1

                # 4. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                if game_state[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    new_game_state[x, y] = 0

            if new_game_state[x, y] == 0:
                pg.draw.polygon(scr, (0, 80, 0), poly, 1)
            else:
                pg.draw.polygon(scr, (0, 200, 0), poly, 0)

    game_state = np.copy(new_game_state)
                
    pg.display.flip()
        
            
