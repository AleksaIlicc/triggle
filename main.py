import pygame
from utils.colors import *
from utils.paths import *

def setup_window(board, gap_size=44):
    total_rows = len(board)
    max_dots = max(board)

    return max_dots * gap_size + 100, total_rows * gap_size + 100

def draw_triangle(screen, triangle, color):
    pygame.draw.polygon(screen, color, triangle, 0)

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

def draw_text(screen, text, font, color, center, align='center'):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if align == 'center':
        text_rect.center = center
    elif align == 'left':
        text_rect.midleft = center

    screen.blit(text_surface, text_rect)


def pre_game_setup(screen, width, height, base_font):
    pygame.font.init()

    title_font = create_font(font_path, 112)

    n = 4
    player = "X"

    while True:
        screen.fill(WHITE)

        draw_text(screen, "Triggle", title_font, BLACK, (width // 2, height // 4 - 50))

        draw_text(screen, "Izaberite velicinu table (4-8):", base_font, BLACK, (width // 2, height // 3))
        draw_text(screen, f"Trenutno: {n}", base_font, BLACK, (width // 2, height // 3 + 50))

        draw_text(screen, "Izaberite pocetnog igraca (X ili O):", base_font, BLACK, (width // 2, height // 2))
        draw_text(screen, f"Trenutni igrac: {player}", base_font, BLACK, (width // 2, height // 2 + 50))

        draw_text(screen, "Pritisnite Enter za pocetak igre", base_font, BLACK, (width // 2, height // 1.25))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return n, player

                if event.key == pygame.K_UP:
                    n = min(8, n + 1)
                elif event.key == pygame.K_DOWN:
                    n = max(4, n - 1)

                if event.key == pygame.K_x:
                    player = "X"
                elif event.key == pygame.K_o:
                    player = "O"


def draw_board(table, screen, gap_size, selected_dots, lines):
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


def is_valid_move(start, end, gap_size, lines):

    if (start,end) in lines:
        return False

    dx = end[0] - start[0]
    dy = end[1] - start[1]

    if dy == 0 and dx == 3 * gap_size:
        return True

    if dx == gap_size * 1.5 and dy == gap_size * 3:
        return True

    if dx == -gap_size * 1.5 and dy == gap_size * 3:
        return True

    return False


def generate_segments(start, end):
    segments = []
    dx = (end[0] - start[0]) // 3
    dy = (end[1] - start[1]) // 3

    current_point = start
    for i in range(1, 4):
        next_point = (current_point[0] + dx, current_point[1] + dy)
        segments.append((current_point, next_point))
        current_point = next_point

    return segments

def create_triangle(point1, point2, point3):
    triangle = [point1, point2, point3]
    triangle.sort(key=lambda point: (point[0], point[1]))
    return tuple(triangle)

def create_adjacent_list(dot_positions, n):
    adjacent_list = {}
    total_rubber_bands = 0

    for i, row in enumerate(dot_positions):
        for j, dot in enumerate(row):
            adjacent_list[dot] = set()

            if j > 0:
                adjacent_list[dot].add(row[j - 1])
            if j < len(row) - 1:
                adjacent_list[dot].add(row[j + 1])

            if i > 0:
                prev_row = dot_positions[i - 1]
                if j < len(prev_row):
                    adjacent_list[dot].add(prev_row[j])
                if j > 0:
                    adjacent_list[dot].add(prev_row[j - 1])
                if j < len(prev_row) - 1:
                    adjacent_list[dot].add(prev_row[j + 1])

            if i < len(dot_positions) - 1:
                next_row = dot_positions[i + 1]
                if j < len(next_row):
                    adjacent_list[dot].add(next_row[j])
                if j > 0:
                    adjacent_list[dot].add(next_row[j - 1])
                if j < len(next_row) - 1:
                    adjacent_list[dot].add(next_row[j + 1])

            if j + 3 < len(row):
                total_rubber_bands += 1

    total_rubber_bands *= 3

    return adjacent_list, total_rubber_bands

def create_font(path, size):
    return pygame.font.Font(path, size)

def draw_scoreboard(screen, player, font, pointsX, pointsO):
    draw_text(screen, f"Trenutni igrač: {player}", font, BLACK, (10, 15), align='left')
    draw_text(screen, f"X: {pointsX}", font, BLACK, (10, 35), align='left')
    draw_text(screen, f"O: {pointsO}", font, BLACK, (10, 55), align='left')

def main():
    pygame.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Triggle - AkoIspadne")

    font = create_font(font_path,32)
    n, player = pre_game_setup(screen, width, height, font)
    board = create_board(n)

    gap_size = 46
    window_width, window_height = setup_window(board, gap_size)
    screen = pygame.display.set_mode((window_width, window_height))

    selected_dots = []
    lines = set()
    line_segments = set()
    triggles_X = set()
    triggles_O = set()
    dot_positions = draw_board(board, screen, gap_size, selected_dots, lines)
    adjacent_list, total_possible_moves = create_adjacent_list(dot_positions, n)

    print(total_possible_moves)
    running = True
    while running:
        screen.fill(WHITE)

        draw_scoreboard(screen, player, font, len(triggles_X), len(triggles_O))

        for triangle in triggles_X:
            draw_triangle(screen, triangle, X_COLOR)
        for triangle in triggles_O:
            draw_triangle(screen, triangle, O_COLOR)

        dot_positions = draw_board(board, screen, gap_size, selected_dots, lines)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                for row in dot_positions:
                    for dot_pos in row:
                        if not ((mouse_pos[0] - dot_pos[0]) ** 2 + (mouse_pos[1] - dot_pos[1]) ** 2 <= 100):
                            continue

                        if dot_pos in selected_dots:
                            selected_dots.remove(dot_pos)
                        else:
                            selected_dots.append(dot_pos)

                            if not (len(selected_dots) == 2):
                                continue

                            start, end = selected_dots
                            if is_valid_move(start, end, gap_size, lines):
                                lines.add((start, end))

                                segments = generate_segments(start, end)
                                for segment in segments:
                                    line_segments.add(frozenset(segment))

                                    common_neighbors = adjacent_list[segment[0]] & adjacent_list[segment[1]]

                                    for neighbor in common_neighbors:
                                        if frozenset((segment[0], neighbor)) in line_segments and frozenset((segment[1], neighbor)) in line_segments:
                                            triangle = create_triangle(segment[0], segment[1], neighbor)

                                            if triangle not in triggles_X and triangle not in triggles_O:
                                                triggles_X.add(triangle) if player == "X" else triggles_O.add(triangle)

                                player = "O" if player == "X" else "X"

                            selected_dots = []
                        break

    pygame.quit()

main()
