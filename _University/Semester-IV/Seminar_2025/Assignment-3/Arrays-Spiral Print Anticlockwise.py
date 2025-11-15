m, n = map(int, input().split())
matrix = [list(map(int, input().split())) for _ in range(m)]

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
visited = [[False] * n for _ in range(m)]

x, y, d = 0, 0, 0  # Direction index
result = []

for _ in range(m * n):
    result.append(matrix[x][y])  # Add current element to result
    visited[x][y] = True  # Mark as visited

    next_x, next_y = x + directions[d][0], y + directions[d][1]

    # Change direction if out of bounds or already visited
    if not (0 <= next_x < m and 0 <= next_y < n and not visited[next_x][next_y]):
        d = (d + 1) % 4  # Cycle through directions (Down → Right → Up → Left)
        next_x, next_y = x + directions[d][0], y + directions[d][1]

    x, y = next_x, next_y

print(", ".join(map(str, result)) + ", END")
