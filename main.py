import random
import time
import pygame
from utils.colors import *
from utils.paths import *
from utils.next_player import *

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
    game_mode = "PvP"
    first_player = "X"

    offset = 100
    arrow_size = 15
    arrow_gap = 250
    running = True

    def draw_arrows(left_arrow, right_arrow):
        pygame.draw.polygon(screen, BLACK, [(left_arrow.x, left_arrow.y + arrow_size // 2),(left_arrow.x + arrow_size, left_arrow.y),(left_arrow.x + arrow_size, left_arrow.y + arrow_size)])
        pygame.draw.polygon(screen, BLACK, [(right_arrow.x, right_arrow.y),(right_arrow.x + arrow_size, right_arrow.y + arrow_size // 2),(right_arrow.x, right_arrow.y + arrow_size)])

    while running:
        screen.fill(WHITE)

        draw_text(screen, "Triggle", title_font, BLACK, (width // 2, height // 5 - 50))

        draw_text(screen, "Izaberite mod igre:", base_font, BLACK, (width // 2, height // 3.5))
        draw_text(screen, "Player vs Player" if game_mode == "PvP" else "Player vs Computer", base_font, BLACK, (width // 2, height // 3.5 + 30))
        mode_left_arrow = pygame.Rect(width // 2 - arrow_gap, height // 3.5 + 23, arrow_size, arrow_size)
        mode_right_arrow = pygame.Rect(width // 2 + arrow_gap - arrow_size, height // 3.5 + 23, arrow_size, arrow_size)
        draw_arrows(mode_left_arrow, mode_right_arrow)

        draw_text(screen, "Izaberite velicinu table (4-8):", base_font, BLACK, (width // 2, height // 3.5 + offset))
        draw_text(screen, f"Trenutno: {n}", base_font, BLACK, (width // 2, height // 3.5 + 30 + offset))
        size_left_arrow = pygame.Rect(width // 2 - arrow_gap, height // 3.5 + 23 + offset, arrow_size, arrow_size)
        size_right_arrow = pygame.Rect(width // 2 + arrow_gap - arrow_size, height // 3.5 + 23 + offset, arrow_size, arrow_size)
        draw_arrows(size_left_arrow, size_right_arrow)

        draw_text(screen, "Izaberite ko igra prvi (X ili O):", base_font, BLACK, (width // 2, height // 3.5 + 2 * offset))
        draw_text(screen, f"Trenutno: {first_player}", base_font, BLACK, (width // 2, height // 3.5 + 30 + 2 * offset))
        first_player_left_arrow = pygame.Rect(width // 2 - arrow_gap, height // 3.5 + 23 + 2 * offset, arrow_size, arrow_size)
        first_player_right_arrow = pygame.Rect(width // 2 + arrow_gap - arrow_size, height // 3.5 + 23 + 2 * offset, arrow_size, arrow_size)
        draw_arrows(first_player_left_arrow, first_player_right_arrow)

        if game_mode == "PvAI":
            draw_text(screen, "Izaberite vaseg igraca (X ili O):", base_font, BLACK, (width // 2, height // 3.5 + 3 * offset))
            draw_text(screen, f"Trenutni vas igrac: {player}", base_font, BLACK, (width // 2, height // 3.5 + 30 + 3 * offset))
            player_left_arrow = pygame.Rect(width // 2 - arrow_gap, height // 3.5 + 23 + 3 * offset, arrow_size, arrow_size)
            player_right_arrow = pygame.Rect(width // 2 + arrow_gap - arrow_size, height // 3.5 + 23 + 3 * offset, arrow_size, arrow_size)
            draw_arrows(player_left_arrow, player_right_arrow)

        draw_text(screen, "Pritisnite Enter za pocetak igre", base_font, BLACK, (width // 2, height // 1.15))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return n, first_player, player , game_mode

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if mode_left_arrow.collidepoint(mouse_pos) or mode_right_arrow.collidepoint(mouse_pos):
                    game_mode = "PvP" if game_mode == "PvAI" else "PvAI"
                    offset = 80 if offset == 100 else 100
                elif size_left_arrow.collidepoint(mouse_pos):
                    n = max(4, n - 1)
                elif size_right_arrow.collidepoint(mouse_pos):
                    n = min(8, n + 1)
                elif first_player_left_arrow.collidepoint(mouse_pos) or first_player_right_arrow.collidepoint(mouse_pos):
                    first_player = next_player[first_player]
                elif game_mode == "PvAI" and (player_left_arrow.collidepoint(mouse_pos) or player_right_arrow.collidepoint(mouse_pos)):
                    player = next_player[player]


def show_dialog(screen, message, font, options):
    screen.fill(WHITE)

    message_lines = message.split('\n')
    line_height = font.get_height()
    y_offset = (screen.get_height() - len(message_lines) * line_height - (len(message_lines) - 1) * 10) // 3

    for line in message_lines:
        draw_text(screen, line, font, BLACK, (screen.get_width() // 2, y_offset), align='center')
        y_offset += line_height + 10

    button_width, button_height = 100, 40
    gap = 16
    buttons = []

    total_button_width = len(options) * button_width + (len(options) - 1) * gap
    for i, option in enumerate(options):
        x = (screen.get_width() - total_button_width) // 2 + i * (button_width + gap)
        y = screen.get_height() // 2 + 120
        button_rect = pygame.Rect(x, y, button_width, button_height)
        buttons.append((button_rect, option))
        pygame.draw.rect(screen, LIGHT_GRAY, button_rect)
        draw_text(screen, option, font, BLACK, button_rect.center, align='center')

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, option in buttons:
                    if button.collidepoint(event.pos):
                        return option

def draw_board(table, screen, gap_size, selected_dots, game_state):
    lines = game_state["lines"]
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

def is_valid_move(start, end, gap_size, game_state):
    lines = game_state["lines"]
    if (start, end) in lines:
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

def create_adjacent_list(dot_positions):
    adjacent_list = {}

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
    return adjacent_list

def create_font(path, size):
    return pygame.font.Font(path, size)

def draw_scoreboard(screen, font, game_state):
    pointsX = len(game_state["triggles_X"])
    pointsO = len(game_state["triggles_O"])
    player = game_state["current_player"]

    scoreX_text = font.render(f"X: {pointsX}", True, BLACK)
    scoreO_text = font.render(f"O: {pointsO}", True, BLACK)

    scoreX_width = scoreX_text.get_width()
    scoreO_width = scoreO_text.get_width()

    draw_text(screen, f"Trenutni igrač: {player}", font, BLACK, (10, 15), align='left')
    screen.blit(scoreX_text, (10, 35))
    screen.blit(scoreO_text, (10, 55))

    x_triangle = [(12 + scoreX_width, 50), (19 + scoreX_width, 42), (25 + scoreX_width, 50)]
    o_triangle = [(12 + scoreO_width, 70), (19 + scoreO_width, 62), (25 + scoreO_width, 70)]

    draw_triangle(screen, x_triangle, X_COLOR)
    draw_triangle(screen, o_triangle, O_COLOR)

def compute_game_metrics(dot_positions, n):
    total_possible_moves = 0
    triggles_needed_for_win = 0

    for i, row in enumerate(dot_positions):
        if i < n - 1:
            triggles_needed_for_win += len(row) * 2 - 1
        for j, dot in enumerate(row):
            if j + 3 < len(row):
                total_possible_moves += 1

    total_possible_moves *= 3
    return total_possible_moves, triggles_needed_for_win

def is_goal_state(game_state, total_possible_moves, triggles_needed_for_win):
    triggles_X = game_state["triggles_X"]
    triggles_O = game_state["triggles_O"]
    total_moves = len(game_state['lines'])
    milestone_reached = game_state["milestone_reached"]

    if total_moves >= total_possible_moves or len(triggles_X) + len(triggles_O) >= triggles_needed_for_win * 2:
        if len(triggles_X) > len(triggles_O):
            return True, "Igra zavrsena!\nPobednik je igrac X.", False
        elif len(triggles_O) > len(triggles_X):
            return True, "Igra zavrsena!\nPobednik je igrac O.", False
        else:
            return True, "Igra zavrsena!\nNeresen rezultat.", False

    if not milestone_reached and (len(triggles_X) > triggles_needed_for_win or len(triggles_O) > triggles_needed_for_win):
        winner = "X" if len(triggles_X) > len(triggles_O) else "O"
        game_state["milestone_reached"] = True
        return False, f"Igrac {winner} je pobedio. \nDa li zelite ipak da nastavite?", True

    return False, "", False

def generate_possible_moves(dot_positions, game_state, gap_size):
    all_points = [dot for row in dot_positions for dot in row]
    potential_moves = []

    for start in all_points:
        x1, y1 = start
        offsets = [
            (gap_size * 3, 0),
            (gap_size * 1.5, gap_size * 3),
            (-gap_size * 1.5, gap_size * 3)
        ]
        for dx, dy in offsets:
            end = (x1 + dx, y1 + dy)
            if end in all_points and is_valid_move(start, end, gap_size, game_state):
                potential_moves.append((start, end))

    return potential_moves

def evaluate_game_state(game_state):
    return len(game_state["triggles_X"]) - len(game_state["triggles_O"])


def minmax(game_state, depth, maximizing_player, dot_positions, gap_size, adjacent_list, total_possible_moves, triggles_needed_for_win, alpha, beta):
    if depth == 0 or is_goal_state(game_state, total_possible_moves, triggles_needed_for_win)[0]:
        return evaluate_game_state(game_state), None

    possible_states = generate_possible_states(dot_positions, gap_size, adjacent_list, game_state)
    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for state in possible_states:
            eval_score, _ = minmax(state, depth - 1, False, dot_positions, gap_size, adjacent_list, total_possible_moves, triggles_needed_for_win, alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = state["lines"] - game_state["lines"]
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move.pop() if best_move else None
    else:
        min_eval = float('inf')
        for state in possible_states:
            eval_score, _ = minmax(state, depth - 1, True, dot_positions, gap_size, adjacent_list, total_possible_moves, triggles_needed_for_win, alpha, beta)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = state["lines"] - game_state["lines"]
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move.pop() if best_move else None


def get_ai_move(dot_positions, game_state, gap_size, adjacent_list, total_possible_moves, triggles_needed_for_win, depth = 3):
    _, best_move = minmax(game_state, depth, True, dot_positions, gap_size, adjacent_list, total_possible_moves, triggles_needed_for_win, float('-inf'), float('inf'))
    return best_move

def generate_possible_states(dot_positions, gap_size, adjacent_list, game_state):
    lines = game_state["lines"]
    triggles_X = game_state["triggles_X"]
    triggles_O = game_state["triggles_O"]
    line_segments = game_state["line_segments"]
    current_player = game_state["current_player"]
    milestone_reached = game_state["milestone_reached"]
    possible_moves = generate_possible_moves(dot_positions, game_state, gap_size)
    possible_states = []

    for move in possible_moves:
        new_game_state = {
        "lines": lines.copy(),
        "line_segments": line_segments.copy(),
        "triggles_X": triggles_X.copy(),
        "triggles_O": triggles_O.copy(),
        "current_player": next_player[current_player],
        "milestone_reached": milestone_reached
        }
        start, end = move
        new_game_state["lines"].add((start, end))
        add_triggles_if_valid(start, end, adjacent_list, new_game_state)
        possible_states.append(new_game_state)

    return possible_states


def add_triggles_if_valid(start, end, adjacent_list, game_state):
    triggles_O = game_state["triggles_O"]
    triggles_X = game_state["triggles_X"]
    lines = game_state["lines"]
    line_segments = game_state["line_segments"]
    player = game_state["current_player"]
    lines.add((start, end))
    line_segments.add(frozenset((start, end)))

    segments = generate_segments(start, end)

    for segment in segments:
        line_segments.add(frozenset(segment))

        common_neighbors = adjacent_list[segment[0]] & adjacent_list[segment[1]]

        for neighbor in common_neighbors:
            if frozenset((segment[0], neighbor)) in line_segments and frozenset((segment[1], neighbor)) in line_segments:
                triangle = create_triangle(segment[0], segment[1], neighbor)

                if triangle not in triggles_X and triangle not in triggles_O:
                    triggles_X.add(triangle) if player == "X" else triggles_O.add(triangle)

def handle_end_of_turn(screen, font, game_state, total_possible_moves, triggles_needed_for_win):
    game_over, message, can_continue = is_goal_state(game_state, total_possible_moves, triggles_needed_for_win)

    if game_over:
        show_dialog(screen, message, font, ["Zatvori"])
        return False

    if can_continue:
        user_choice = show_dialog(screen, message, font, ["Da", "Ne"])
        if user_choice != "Da":
            return False

    game_state["current_player"] = next_player[game_state["current_player"]]
    return True

def main():
    pygame.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Triggle - AkoIspadne")

    font = create_font(font_path, 32)
    n, first_player, player, game_mode = pre_game_setup(screen, width, height, font)
    board = create_board(n)

    gap_size = 46
    window_width, window_height = setup_window(board, gap_size)
    screen = pygame.display.set_mode((window_width, window_height))

    game_state = {
        "lines": set(),
        "line_segments": set(),
        "triggles_X": set(),
        "triggles_O": set(),
        "current_player": first_player,
        "milestone_reached": False
    }

    selected_dots = []
    dot_positions = draw_board(board, screen, gap_size, selected_dots, game_state)
    total_possible_moves, triggles_needed_for_win = compute_game_metrics(dot_positions, n)
    adjacent_list = create_adjacent_list(dot_positions)

    valid_move = True

    running = True
    while running:
        screen.fill(WHITE)

        draw_scoreboard(screen, font, game_state)
        for triangle in game_state['triggles_X']:
            draw_triangle(screen, triangle, X_COLOR)
        for triangle in game_state['triggles_O']:
            draw_triangle(screen, triangle, O_COLOR)
        dot_positions = draw_board(board, screen, gap_size, selected_dots, game_state)

        if not valid_move:
            draw_text(screen, "Potez nije validan", font, BLACK, (screen.get_width() - 220, screen.get_height() - 20),"left")
        pygame.display.flip()

        if game_mode == "PvAI" and game_state["current_player"] != player:
            ai_move = get_ai_move(dot_positions, game_state, gap_size, adjacent_list, total_possible_moves, triggles_needed_for_win)
            if ai_move:
                start, end = ai_move
                add_triggles_if_valid(start, end, adjacent_list, game_state)
                if not handle_end_of_turn(screen, font, game_state, total_possible_moves, triggles_needed_for_win):
                    running = False
            continue

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

                            if not(len(selected_dots)) == 2:
                                continue
                            start, end = selected_dots
                            valid_move = is_valid_move(start, end, gap_size, game_state)
                            if valid_move:
                                add_triggles_if_valid(start, end, adjacent_list, game_state)
                                if not handle_end_of_turn(screen, font, game_state, total_possible_moves, triggles_needed_for_win):
                                    running = False
                            selected_dots = []
                        break
    pygame.quit()


main()