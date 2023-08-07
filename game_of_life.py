import curses
import time

def initialize_grid(height, width):
    return [[False for _ in range(width)] for _ in range(height)]

def draw_grid(win, grid):
    height, width = len(grid), len(grid[0])
    for y in range(height):
        for x in range(width):
            char = "█" if grid[y][x] else " "
            try:
                win.addstr(y, x, char)
            except curses.error:
                pass
    win.refresh()

def count_neighbors(grid, y, x):
    height, width = len(grid), len(grid[0])
    neighbors = [
        (y - 1, x - 1), (y - 1, x), (y - 1, x + 1),
        (y, x - 1),                 (y, x + 1),
        (y + 1, x - 1), (y + 1, x), (y + 1, x + 1)
    ]
    count = 0
    for ny, nx in neighbors:
        if 0 <= ny < height and 0 <= nx < width and grid[ny][nx]:
            count += 1
    return count

def evolve_grid(grid):
    height, width = len(grid), len(grid[0])
    new_grid = initialize_grid(height, width)

    for y in range(height):
        for x in range(width):
            neighbors = count_neighbors(grid, y, x)
            if grid[y][x]:  # Cell is alive
                if neighbors == 2 or neighbors == 3:
                    new_grid[y][x] = True  # Cell survives
            else:  # Cell is dead
                if neighbors == 3:
                    new_grid[y][x] = True  # Cell reproduces

    return new_grid

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()
    curses.start_color()

    # Define color pair (foreground, background)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    height, width = curses.LINES, curses.COLS

    grid = initialize_grid(height, width)

    # Example: Glider
    grid[5][5] = True
    grid[6][6] = True
    grid[7][4] = True
    grid[7][5] = True
    grid[7][6] = True

    try:
        while True:
            draw_grid(stdscr, grid)
            grid = evolve_grid(grid)
            time.sleep(0.1)  # Adjust the delay between generations if needed
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    curses.wrapper(main)