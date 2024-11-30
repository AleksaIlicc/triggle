import pygame

def setup_window(board, gap_size=40):
    total_rows = len(board)
    max_dots = max(board)

    if gap_size < 44:
        gap_size = 44

    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    max_gap_width = (screen_width - 250) // max_dots
    max_gap_height = (screen_height - 250) // total_rows
    gap_size = min(gap_size, min(max_gap_width, max_gap_height))

    return  max_dots * gap_size + 100, total_rows * gap_size + 100

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

def draw_board(table, screen, gap_size = 50):
    total_rows = len(table)

    vertical_offset = (screen.get_height() - total_rows * gap_size) // 2

    for i, num_dots in enumerate(table):
        y_pos = vertical_offset + (i * gap_size) + gap_size/2
        x_pos = (screen.get_width() // 2) - (num_dots * gap_size // 2) + gap_size / 2

        for j in range(num_dots):
            pygame.draw.circle(screen, (0,0,0), (x_pos + j * gap_size, y_pos), 10)

def main(n,gap_size=40):
    pygame.init()

    board = create_board(n)
    if board is None:
        print("Nevalidna velicina table. Velicina mora biti izmedju 4 i 8.")
        return

    window_width, window_height = setup_window(board, gap_size)

    screen = pygame.display.set_mode((window_width, window_height))
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Triggle - AkoIspadne")

    draw_board(board, screen, gap_size)

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

main(4)
