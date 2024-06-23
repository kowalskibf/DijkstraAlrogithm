import heapq

def load_board(file_name):
    with open(file_name, encoding="utf-8") as file:
        return [list(line) for line in file.read().splitlines()]
    

def dijkstra(board, start, end):
    rows, cols = len(board), len(board[0])
    visited = [[False] * cols for _ in range(rows)]
    distance = [[float('inf')] * cols for _ in range(rows)]
    parent = [[None] * cols for _ in range(rows)]

    heap = [(0, start)]
    distance[start[0]][start[1]] = 0

    while heap:
        current_distance, current_node = heapq.heappop(heap)

        if visited[current_node[0]][current_node[1]]:
            continue

        visited[current_node[0]][current_node[1]] = True

        neighbors = get_neighbors(current_node, rows, cols)
        for neighbor in neighbors:
            cost = get_cost(board, current_node, neighbor)
            new_distance = distance[current_node[0]][current_node[1]] + cost

            if new_distance < distance[neighbor[0]][neighbor[1]]:
                distance[neighbor[0]][neighbor[1]] = new_distance
                parent[neighbor[0]][neighbor[1]] = current_node
                heapq.heappush(heap, (new_distance, neighbor))

    path = reconstruct_path(parent, end)
    return path, distance[end[0]][end[1]]

def get_neighbors(node, rows, cols):
    neighbors = []

    if node[0] > 0:
        neighbors.append((node[0] - 1, node[1]))  # Up
    if node[0] < rows - 1:
        neighbors.append((node[0] + 1, node[1]))  # Down
    if node[1] > 0:
        neighbors.append((node[0], node[1] - 1))  # Left
    if node[1] < cols - 1:
        neighbors.append((node[0], node[1] + 1))  # Right

    return neighbors

def get_cost(board, current_node, neighbor):
    current_char = board[current_node[0]][current_node[1]]
    neighbor_char = board[neighbor[0]][neighbor[1]]

    if current_char == 'J' or neighbor_char == 'J' or neighbor_char == 'X':
        return 0
    return int(neighbor_char)

def reconstruct_path(parent, end):
    path = []
    current_node = end

    while current_node:
        path.append(current_node)
        current_node = parent[current_node[0]][current_node[1]]

    return path[::-1]

def hide_unvisited(board, visited_nodes):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if (i, j) not in visited_nodes:
                board[i][j] = ' '

def print_board(board):
    for row in board:
        print(''.join(row))
    

file_path = "graf6.txt"  # Change this to the desired input file path
board = load_board(file_path)

start = None
end = None

for i in range(len(board)):
    for j in range(len(board[0])):
        if board[i][j] == 'X':
            if start is None:
                start = (i, j)
            else:
                end = (i, j)

path, cost = dijkstra(board, start, end)

hide_unvisited(board, path)
print_board(board)
print("\nKoszt:", cost)