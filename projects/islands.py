# Write a function that takes a 2D binary array and
# returns the number of 1 islands.
# An island consists of 1s that are connected to the 
# north, south, east or west. For example:

islands = [[0, 1, 0, 1, 0],
           [1, 1, 0, 1, 1],
           [0, 0, 1, 0, 0],
           [1, 0, 1, 0, 0],
           [1, 1, 0, 0, 0],
           [0, 0, 0, 0, 0]]

# island_counter(islands) -> returns 4

# 1. Translate the problem into graph terminology
# 2. Build your graph
# 3. Traverse your graph


def islands_counter(matrix):
    # Traverse nodes
    visited = []
    island_counter = 0
    for i in range(len(matrix)):
        visited.append([False] * len(matrix[0]))

    for col in range(len(matrix[0])):
        for row in range(len(matrix)):
            # if node not visited
            if not visited[row][col]:
                # if we hit a 1:
                if matrix[row][col] == 1:
                    # mark visited
                    # increment visited count
                    visited = dft(row, col, matrix, visited)
                    # traverse all connected nodes, mark as visited
                    island_count += 1
