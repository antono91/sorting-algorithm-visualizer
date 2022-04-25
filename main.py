from turtle import pos
from numpy import sort
import pygame
import random


pygame.init()


class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GRAYS = [(125, 125, 125), (160, 160, 160), (192, 192, 192)]
    BG_COLOR = WHITE
    SIDE_PADDING = 100
    TOP_PADDING = 200
    FONT = pygame.font.SysFont("Monaco", 16)
    L_FONT = pygame.font.SysFont("Monaco", 24)

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.set_list(lst)

        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.bar_width = round(
            (self.width - self.SIDE_PADDING) // len(self.lst))
        self.bar_height_factor = round(
            (self.height - self.TOP_PADDING) / (self.max_val - self.min_val))

# ----------------------------------------------------------------
# Help Functions

def generate_list(count, start, end):
    return [random.randint(start, end) for _ in range(count)]


def draw(di, ascending, algorithm_name):
    di.win.fill(di.BG_COLOR)

    sorting_type = di.L_FONT.render(
        f'{algorithm_name} {"ascending" if ascending else "descending"}', 1, di.RED)
    di.win.blit(sorting_type, (di.width // 2 -
                (sorting_type.get_width() // 2), 10))

    controls = di.FONT.render(
        "R - Reset | SPACE - Start sorting | A - Ascending | D - Descending", 1, di.BLACK)
    di.win.blit(controls, (di.width // 2 - (controls.get_width() // 2), 50))

    algorithms = di.FONT.render(
        "B - Bubble Sort | I - Insertion Sort", 1, di.BLACK)
    di.win.blit(algorithms, (di.width // 2 -
                (algorithms.get_width() // 2), 80))

    draw_bars(di)

    pygame.display.update()


def draw_bars(di, color_positions={}, clear_bg=False):
    if clear_bg:
        clear_rect = (di.SIDE_PADDING // 2, di.TOP_PADDING,
                      di.width - di.SIDE_PADDING, di.height - di.TOP_PADDING)
        pygame.draw.rect(di.win, di.BG_COLOR, clear_rect)

    for i, number in enumerate(di.lst):
        bar = pygame.Rect(0, 0, di.bar_width, di.bar_height_factor * number)
        bar.bottom = di.height
        bar.left = (di.SIDE_PADDING // 2) + (i * di.bar_width)
        color = di.GRAYS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(di.win, color, bar)

    if clear_bg:
        pygame.display.update()

# ----------------------------------------------------------------
# Sorting Algorithms


def bubble_sort(di, ascending=True):
    for i in range(len(di.lst) - 1):
        for j in range(len(di.lst) - 1 - i):
            num1 = di.lst[j]
            num2 = di.lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                di.lst[j], di.lst[j + 1] = di.lst[j + 1], di.lst[j]
                draw_bars(di, {j: di.GREEN, j + 1: di.RED}, True)
                yield True
    return di.lst


def insertion_sort(di, ascending=True):
    for i in range(1, len(di.lst)):
        key = di.lst[i]
        j = i - 1
        while (j >= 0 and di.lst[j] > key and ascending) or (j >= 0 and di.lst[j] < key and not ascending):
            di.lst[j + 1] = di.lst[j]
            j -= 1
            di.lst[j + 1] = key
            draw_bars(di, {j+1: di.GREEN, i: di.RED}, True)
            yield True
# ----------------------------------------------------------------

# Main Function


def main():
    n = 100
    min_v = 1
    max_v = 100

    sorting = False
    ascending = True

    algorithm = bubble_sort
    algorithm_name = "Bubble Sort"
    algorithm_genertor = None

    di = DrawInformation(800, 500, generate_list(n, min_v, max_v))
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    di.set_list(generate_list(n, min_v, max_v))
                    sorting = False
                if event.key == pygame.K_SPACE and not sorting:
                    sorting = True
                    algorithm_genertor = algorithm(di, ascending)
                if event.key == pygame.K_a and not sorting:
                    ascending = True
                if event.key == pygame.K_d and not sorting:
                    ascending = False
                if event.key == pygame.K_b:
                    algorithm = bubble_sort
                    algorithm_name = "Bubble Sort"
                if event.key == pygame.K_i:
                    algorithm = insertion_sort
                    algorithm_name = "Insertion Sort"
        if sorting:
            try:
                next(algorithm_genertor)
            except StopIteration:
                sorting = False
        else:
            draw(di, ascending, algorithm_name)

    pygame.quit()
# ----------------------------------------------------------------


if __name__ == "__main__":
    main()
