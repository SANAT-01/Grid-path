import tkinter as tk
import heapq
import math
import numpy as np

def heuristic_cost_estimate(start, goal):
    return math.sqrt(abs(start[0] - goal[0]) + abs(start[1] - goal[1]))

def is_valid(grid, x, y):
    rows, cols = len(grid), len(grid[0])
    return 0 <= x < rows and 0 <= y < cols and grid[x][y] != 1

def get_neighbors(grid, x, y):
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # RIGHT, DOWN, LEFT, UP
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if is_valid(grid, new_x, new_y):
            neighbors.append((new_x, new_y))
    return neighbors

def a_star_search(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    heap = [(0, start)]
    heapq.heapify(heap)
    g_score = {start: 0}
    f_score = {start: heuristic_cost_estimate(start, goal)}

    while heap:
        _, current = heapq.heappop(heap)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        visited.add(current)
        for neighbor in get_neighbors(grid, current[0], current[1]):
            tentative_g_score = g_score[current] + 1

            if neighbor in visited and tentative_g_score >= g_score.get(neighbor, float('inf')):
                continue

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic_cost_estimate(neighbor, goal)
                heapq.heappush(heap, (f_score[neighbor], neighbor))

    return None

def draw_grid(grid, path):
    rows, cols = len(grid), len(grid[0])
    cell_size = 40

    root = tk.Tk()
    root.title("A* Search Visualization")
    canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size)
    canvas.pack()

    for i in range(rows):
        for j in range(cols):
            x0, y0 = j * cell_size, i * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            color = "white" if grid[i][j] == 0 else "black"
            canvas.create_rectangle(x0, y0, x1, y1, fill=color)

            if (i, j) in path:
                canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="red")

    root.mainloop()

if __name__ == "__main__":
    grid = np.round(np.random.random((5,5)))
    
    grid[0][0] = 0
    grid[4][4] = 0
    start = (0, 0)
    goal = (4,4)
    print(grid)
    
    came_from = {}
    path = a_star_search(grid, start, goal)

    if path:
        print("Path:", path)
        print("Number of steps:", len(path) - 1)
        draw_grid(grid, path)
    else:
        print("No valid path found!")
