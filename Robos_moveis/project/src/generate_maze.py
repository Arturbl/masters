import random
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image

def create_path(row, col, maze):
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(directions)
    for dr, dc in directions:
        next_row, next_col = row + dr, col + dc
        if 0 <= next_row < 2 * rows + 1 and 0 <= next_col < 2 * cols + 1 and maze[next_row, next_col] == 1:
            maze[row + dr // 2, col + dc // 2] = 0
            maze[next_row, next_col] = 0
            create_path(next_row, next_col, maze)

def visualize_maze(maze, start, end, cell_width, marker_size, save_path=None):
    fig, ax = plt.subplots(figsize=(maze.shape[1] * cell_width / 30, maze.shape[0] * cell_width / 30))

    ax.imshow(maze, cmap=plt.cm.binary)

    ax.plot(start[1], start[0], marker='o', color='green', markersize=marker_size, label='Start')
    ax.plot(end[1], end[0], marker='o', color='red', markersize=marker_size, label='End')

    plt.xticks([])
    plt.yticks([])

    print(f"Start Coordinates: {start}")
    print(f"End Coordinates: {end}")
    print(f"Marker Size: {marker_size}")
    print(f"Cell Width: {cell_width}")

    if save_path:
        plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
        print(f"Maze saved and resized as {save_path}")
        return
    plt.show()

def generate_maze(rows, cols, start, end, cell_width):
    maze = np.ones((2 * rows + 1, 2 * cols + 1), dtype=int)
    create_path(0, 0, maze)
    return maze

rows, cols = 5, 5
start = (0, 0)
end = (2 * rows, 2 * cols)
cell_width = 10
maze_matrix = generate_maze(rows, cols, start, end, cell_width)

print("Generated Maze:")
print(maze_matrix)

save_folder = 'images'
os.makedirs(save_folder, exist_ok=True)
save_path = os.path.join(save_folder, f'maze.png')

visualize_maze(maze_matrix, start, end, cell_width, 5, save_path)
