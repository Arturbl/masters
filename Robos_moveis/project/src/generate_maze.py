import random
import matplotlib.pyplot as plt
import numpy as np
import os
import time


def create_path(row, col, maze):
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(directions)
    for dr, dc in directions:
        next_row, next_col = row + dr, col + dc
        if 0 <= next_row < 2 * rows + 1 and 0 <= next_col < 2 * cols + 1 and maze[next_row, next_col] == 1:
            maze[row + dr // 2, col + dc // 2] = 0
            maze[next_row, next_col] = 0
            create_path(next_row, next_col, maze)


def visualize_maze(maze, save_path=None):
    cmap = plt.cm.colors.ListedColormap(['white', 'black', 'green', 'red'])
    norm = plt.cm.colors.Normalize(vmin=-0.5, vmax=3.5)
    plt.imshow(maze, cmap=cmap, norm=norm)
    plt.xticks([])
    plt.yticks()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        print(f"Maze saved as {save_path}")
        return
    plt.show()


def generate_maze(rows, cols):
    maze = np.ones((2 * rows + 1, 2 * cols + 1), dtype=int)
    create_path(0, 0, maze)
    maze[0, 0] = 2
    maze[2 * rows, 2 * cols] = 3
    return maze


rows, cols = 4, 4
maze_matrix = generate_maze(rows, cols)

print("Generated Maze:")
print(maze_matrix)

save_folder = 'images'
os.makedirs(save_folder, exist_ok=True)
save_path = os.path.join(save_folder, f'maze{time.time()}.png')

visualize_maze(maze_matrix, save_path)