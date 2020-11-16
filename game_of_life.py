"""
Pygame version for Convey's Game of Life.

Rules:
    - Any live cell with two or three live neighbours survives.
    - Any dead cell with three live neighbours becomes a live cell.
    - All other live cells die in the next generation. Similarly, all other dead cells stay dead.
"""
import random
import pygame


PIXEL_SIZE = 5
LIFE_DECREASER = 7
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
GRID_WIDTH = 640 // PIXEL_SIZE
GRID_HEIGHT = 480 // PIXEL_SIZE
FPS = 40
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class World():
    """
    World grid.
    """

    def __init__(self, *args, **kwargs):
        self.grid = [[0 for i in range(GRID_HEIGHT)] for i in range(GRID_WIDTH)]

    def set_cell(self, x, y, status):
        self.grid[x][y] = status

    def get_cell(self, x, y):
        return self.grid[x][y]

    def count_neighbours(self, x, y):
        neighbour_cells = [
            (x - 1, y - 1), (x - 1, y + 0), (x - 1, y + 1),
            (x + 0, y - 1),                 (x + 0, y + 1),
            (x + 1, y - 1), (x + 1, y + 0), (x + 1, y + 1)
        ]
        count = 0
        for x, y in neighbour_cells:
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                count += self.get_cell(x, y)
        return count


def make_random_life(grid, background):
    """Create the orginal grid patteren randomly"""
    for x in range(0, GRID_WIDTH):
        for y in range(0, GRID_HEIGHT):
            if random.randint(0, LIFE_DECREASER) == 1:
                grid.set_cell(x, y, 1)
                draw_square(background, WHITE, x, y)


def draw_square(background, color, x, y):
    pygame.draw.rect(background, color, (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))


def will_live(grid, x, y):
    alive = True if grid.get_cell(x, y) else False
    neighbours_count = grid.count_neighbours(x, y)
    return True if neighbours_count == 3 or (alive and neighbours_count == 2) else False


def main():

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    play = True
    evolution_steps = 0
    clock = pygame.time.Clock()
    bg = pygame.Surface(screen.get_size())
    bg.convert()
    bg.fill((0, 0, 0))
    grid = World()
    make_random_life(grid, bg)
    screen.blit(bg, (0, 0))
    pygame.display.flip()

    while play:
        clock.tick(FPS)
        evolution_steps += 1
        next_gen = World()
        caption = f"Game of Life. FPS: {FPS}, evolution steps: {evolution_steps}"
        pygame.display.set_caption(caption)

        for x in range(0, GRID_WIDTH):
            for y in range(0, GRID_HEIGHT):
                if will_live(grid, x, y):
                    next_gen.set_cell(x, y, 1)
                    draw_square(bg, WHITE, x, y)
                else:
                    next_gen.set_cell(x, y, 0)
                    draw_square(bg, BLACK, x, y)
        # Handle events
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                play = False

        grid = next_gen
        screen.blit(bg, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    main()
