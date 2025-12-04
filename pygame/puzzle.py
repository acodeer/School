import heapq
import time
from copy import deepcopy

class NPuzzleDijkstra:
    def __init__(self, start_board, goal_board):
        self.start_board = start_board
        self.goal_board = goal_board

    def get_neighbors(self, board):
        # 가능한 상하좌우 움직임을 정의합니다.
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        
        zero_row, zero_col = next((r, c) for r, row in enumerate(board) for c, val in enumerate(row) if val == 0)
        
        for dr, dc in directions:
            new_row, new_col = zero_row + dr, zero_col + dc
            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                # 빈칸을 이동하여 새로운 보드 상태를 생성합니다.
                new_board = [row[:] for row in board]
                new_board[zero_row][zero_col], new_board[new_row][new_col] = new_board[new_row][new_col], new_board[zero_row][zero_col]
                neighbors.append(new_board)
        
        return neighbors

    def solve(self):
        start_time = time.time()
        open_list = []
        closed_set = set()
        
        # 초기 상태를 큐에 삽입합니다 (경로 비용, 보드 상태, 경로)
        heapq.heappush(open_list, (0, self.start_board, []))
        
        while open_list:
            g, current_board, path = heapq.heappop(open_list)
            closed_set.add(tuple(map(tuple, current_board)))
            
            if current_board == self.goal_board:
                end_time = time.time()
                print(f"Dijkstra Solution found in {len(path)} moves")
                print(f"Time elapsed: {end_time - start_time:.10f} seconds")
                return path
            
            for neighbor in self.get_neighbors(current_board):
                if tuple(map(tuple, neighbor)) not in closed_set:
                    new_path = path + [neighbor]
                    new_g = g + 1  # 다익스트라는 g 값만을 사용합니다.
                    heapq.heappush(open_list, (new_g, neighbor, new_path))
        
        print("No solution found.")
        return None

class NPuzzleSolver:
    def __init__(self, board, goal):
        self.start_board = board
        self.goal_board = goal
        self.size = len(board)
        self.goal_position = {val: (i, j) for i, row in enumerate(goal) for j, val in enumerate(row)}

    def manhattan_distance(self, board):
        distance = 0
        for i in range(self.size):
            for j in range(self.size):
                val = board[i][j]
                if val != 0:  # 빈칸(0)은 계산에서 제외
                    goal_i, goal_j = self.goal_position[val]
                    distance += abs(goal_i - i) + abs(goal_j - j)
        return distance

    def get_neighbors(self, board):
        neighbors = []
        zero_row, zero_col = [(i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val == 0][0]
        #빈칸찾기
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 위, 아래, 왼쪽, 오른쪽
        for dr, dc in directions: #dr x축 dc y축
            new_row, new_col = zero_row + dr, zero_col + dc #빈칸 이동
            if 0 <= new_row < self.size and 0 <= new_col < self.size: # 이동한 칸이 보드 안에 있을 때
                new_board = deepcopy(board)
                new_board[zero_row][zero_col], new_board[new_row][new_col] = new_board[new_row][new_col], new_board[zero_row][zero_col]
                neighbors.append(new_board) #상하좌우 이동한 보드를 neighbors에 추가
        return neighbors

    def a_star_search(self):
        start_time = time.time()
        
        open_list = []
        closed_set = set()
        start_heuristic = self.manhattan_distance(self.start_board)
        heapq.heappush(open_list, (start_heuristic, 0, self.start_board, []))  # (f, g, board, path)
        #open_list에 (f, g, board, path)를 넣는다. f = g + h, g = 이동횟수, h = 휴리스틱
        while open_list:
            f, g, current_board, path = heapq.heappop(open_list)
            #open_list에서 (f, g, board, path)를 꺼낸다.
            closed_set.add(tuple(map(tuple, current_board)))
            #closed_set에 board를 튜플로 변환하여 넣는다.
            
            if current_board == self.goal_board:
                end_time = time.time()
                print(f"Solution found in {len(path)} moves")
                print(f"Time elapsed: {end_time - start_time:.10f} seconds")
                return path

            for neighbor in self.get_neighbors(current_board): #이웃한 보드들 대상으로
                if tuple(map(tuple, neighbor)) not in closed_set: #중복되지 않은 보드일 때
                    new_path = path + [neighbor] #이동경로에 이웃한 보드를 추가
                    new_g = g + 1 #이동횟수 증가
                    new_f = new_g + self.manhattan_distance(neighbor)
                    heapq.heappush(open_list, (new_f, new_g, neighbor, new_path))
        
        print("No solution found.")
        return None

start_board = [
        [0, 3, 4, 8],
        [1, 2, 7, 11],
        [5, 6, 15, 10],
        [9, 13, 14, 12]
]

goal_board = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
]

print("Start board")
solver = NPuzzleSolver(start_board, goal_board)
solution = solver.a_star_search()


if solution:
    for step in solution:
        for row in step:
            print(row)
        print()
        
# Dijkstra's algorithm
dSolver = NPuzzleDijkstra(start_board, goal_board)
Dsolution = dSolver.solve()

if Dsolution:
    for step in Dsolution:
        for row in step:
            print(row)
        print()