import sys
import time
from collections import defaultdict
from copy import deepcopy

import pygame
from models import Grid, cell, dimension, neighbours
# from example_patterns import glider_explosion

COLOUR_GRID = (40, 40, 40)
COLOUR_ALIVE = (255, 0, 0)
TIME_SLEEP = 0.1
BORDER_SIZE = 1
# Display size
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
# BOARD size
BOARD_WIDTH = 50
BOARD_HEIGHT = 50
# Cell size
CELL_WIDTH = DISPLAY_WIDTH / BOARD_HEIGHT
CELL_HEIGHT = DISPLAY_HEIGHT / BOARD_HEIGHT

cells = set()


def get_neighbours(grid: Grid, x: int, y: int) -> neighbours:
    """Returns all neighbours of a given cell and their status

    @param grid: the grid which contains the cell we are checking the neighbours for
    @param x: the x coordinate of the cell
    @param y: the y coordinate of the cell
    @return: the neighbours of the given cell
    """
    # offset to get possible neighbours
    offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    # Use offset to get coordinates of all possible neighbours
    possible_neighbours = {(x + x_add, y + y_add) for x_add, y_add in offsets}

    # Find alive cells
    alive = {(pos[0], pos[1]) for pos in possible_neighbours if pos in grid.cells}
    return neighbours(alive, possible_neighbours - alive)


def update_grid(grid: Grid) -> Grid:
    """Updates the grid for the next generation

    @param grid: the current iteration of the grid
    @return: the grid after applying the game rules
    """
    new_cells = deepcopy(grid.cells)
    undead = defaultdict(int)
    # Get the neighbours for each cell in the grid
    for (x, y) in grid.cells:
        alive_neighbours, dead_neighbours = get_neighbours(grid=grid, x=x, y=y)
        # who stays alive
        if len(alive_neighbours) not in [2, 3]:
            new_cells.remove((x, y))
        for pos in dead_neighbours:
            undead[pos] += 1
    # who is born
    for pos, _ in filter(lambda elem: elem[1] == 3, undead.items()):
        new_cells.add(cell(pos[0], pos[1]))

    return Grid(grid.dim, new_cells)


def draw_grid(screen: pygame.Surface, grid: Grid) -> None:
    """Draws the grid of living cells

    @param screen: the pygame surface to draw on
    @param grid: the grid to draw
    """

    for (x, y) in grid.cells:
        pygame.draw.rect(
            screen,
            COLOUR_ALIVE,
            (
                x * CELL_WIDTH + BORDER_SIZE,
                y * CELL_HEIGHT + BORDER_SIZE,
                CELL_WIDTH - BORDER_SIZE,
                CELL_HEIGHT - BORDER_SIZE,
            ),
        )
        pygame.display.update()


def main():
    # set up the grid with initial values
    grid = Grid(dimension(BOARD_WIDTH, BOARD_HEIGHT), cells)
    # grid = glider_explosion

    try:
        pygame.init()
        screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("Game of Life")
        screen.fill(COLOUR_GRID)
        pygame.display.update()

        is_running = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                # toggle between game is running and paused
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        is_running = not is_running
                        pygame.display.update()
                # add selected cell to the grid
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    grid.cells.add(cell(pos[0] // CELL_WIDTH, pos[1] // CELL_HEIGHT))
                    draw_grid(screen=screen, grid=grid)
                    pygame.display.update()

            if is_running:
                screen.fill(COLOUR_GRID)
                # Draw grid
                draw_grid(screen=screen, grid=grid)
                # Update grid
                grid = update_grid(grid=grid)
                pygame.display.update()
                time.sleep(TIME_SLEEP)
    except BaseException as e:
        print(e)
        pygame.quit()


if __name__ == "__main__":
    main()
