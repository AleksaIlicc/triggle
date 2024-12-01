import pygame
from colors import *

def setup_window(board, gap_size=44):
    total_rows = len(board)
    max_dots = max(board)

    return max_dots * gap_size + 100, total_rows * gap_size + 100

def create_board(n):
    if n < 4 or n > 8:
        return None

    table = []

    for i in range(n):
        num_dots = n + i
        table.append(num_dots)

    for i in range(n - 2, -1, -1):
        num_dots = n + i
        table.append(num_dots)

    return table

def draw_board(table, screen, gap_size, selected_dots, lines):
    screen.fill(WHITE)

    total_rows = len(table)
    vertical_offset = (screen.get_height() - total_rows * gap_size) // 2

    for line in lines:
        pygame.draw.line(screen, LINE_COLOR, line[0], line[1], 3)

    dot_positions = []
    for i, num_dots in enumerate(table):
        y_pos = vertical_offset + (i * gap_size) + gap_size / 2
        x_pos = (screen.get_width() // 2) - (num_dots * gap_size // 2) + gap_size / 2

        row_positions = []
        for j in range(num_dots):
            dot_pos = (int(x_pos + j * gap_size), int(y_pos))
            row_positions.append(dot_pos)

            if dot_pos in selected_dots:
                pygame.draw.circle(screen, DOT_SELECTED_COLOR, dot_pos, 10)
            else:
                pygame.draw.circle(screen, DOT_COLOR, dot_pos, 10)

        dot_positions.append(row_positions)

    return dot_positions

def is_valid_move(start, end, gap_size):
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    if dy == 0 and dx == 3 * gap_size:
        return True

    if dx == gap_size * 1.5 and dy == gap_size * 3:
        return True

    if dx == -gap_size * 1.5 and dy == gap_size * 3:
        return True

    return False

def main(n):
    pygame.init()

    board = create_board(n)
    if board is None:
        print("Nevalidna veličina table. Veličina mora biti između 4 i 8.")
        return
    gap_size = 46
    window_width, window_height = setup_window(board, gap_size)
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Triggle - AkoIspadne")

    selected_dots = []
    lines = []

    running = True
    while running:
        dot_positions = draw_board(board, screen, gap_size, selected_dots, lines)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                for row in dot_positions:
                    for dot_pos in row:
                        if (mouse_pos[0] - dot_pos[0]) ** 2 + (mouse_pos[1] - dot_pos[1]) ** 2 <= 100:
                            if dot_pos in selected_dots:
                                selected_dots.remove(dot_pos)
                            else:
                                selected_dots.append(dot_pos)

                                if len(selected_dots) == 2:
                                    start, end = selected_dots
                                    if is_valid_move(start, end, gap_size):
                                        lines.append((start, end))
                                    selected_dots = []
                            break

    pygame.quit()

main(8)
