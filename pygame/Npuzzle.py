import pygame as pg
import random , time , heapq
from copy import deepcopy

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
        return distance #휴리스틱 값 반환

    def get_neighbors(self, board):
        neighbors = []
        zero_row, zero_col = [(i, j) for i, row in enumerate(board) for j, val in enumerate(row) if val == 0][0]
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 위, 아래, 왼쪽, 오른쪽
        for dr, dc in directions:
            new_row, new_col = zero_row + dr, zero_col + dc
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                new_board = deepcopy(board)
                new_board[zero_row][zero_col], new_board[new_row][new_col] = new_board[new_row][new_col], new_board[zero_row][zero_col]
                neighbors.append(new_board)
        return neighbors #입력된 보드에서 상하좌우로 이동한 보드를 반환

    def a_star_search(self):
        start_time = time.time()
        
        open_list = [] #우선순위 큐
        closed_set = set() #중복된 보드를 방지
        start_heuristic = self.manhattan_distance(self.start_board) #시작 휴리스틱 값
        heapq.heappush(open_list, (start_heuristic, 0, self.start_board, []))  # (f, g, board, path)

        while open_list:
            f, g, current_board, path = heapq.heappop(open_list) #리스트 존재 시 최저 f값을 가진 요소를 꺼냄
            closed_set.add(tuple(map(tuple, current_board))) #closed_set에 현재 보드를 튜플로 변환하여 추가

            if current_board == self.goal_board:
                end_time = time.time()
                print(f"Solution found in {len(path)} moves")
                print(f"Time elapsed: {end_time - start_time:.2f} seconds")
                return path #최저 f값 보드 경로 반환

            for neighbor in self.get_neighbors(current_board): #이웃한 보드들 대상으로
                if tuple(map(tuple, neighbor)) not in closed_set: #중복되지 않은 보드일 때
                    new_path = path + [neighbor] 
                    new_g = g + 1
                    new_f = new_g + self.manhattan_distance(neighbor)
                    heapq.heappush(open_list, (new_f, new_g, neighbor, new_path))
        
        print("No solution found.")
        return None
    
class MakeBoard:
    def __init__(self):
        self.board = []
        self.goal = []
        self.size = 0

    def inversion_count(self, board):
        # Flatten the board (excluding 0) and count inversions
        flat_board = [num for row in board for num in row if num != 0]
        inversions = 0
        for i in range(len(flat_board)):
            for j in range(i + 1, len(flat_board)):
                if flat_board[i] > flat_board[j]:
                    inversions += 1
        return inversions

    def is_solvable(self, board):
        size = len(board)
        inversions = self.inversion_count(board)

        # Find the blank row from the bottom
        blank_row = next(i for i in range(size - 1, -1, -1) 
                         for j in range(size) if board[i][j] == 0)
        
        # Solvability rule based on the size
        if size % 2 == 1:
            return inversions % 2 == 0
        else:
            return (inversions + blank_row) % 2 == 1

    def find_blank(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return i, j

    def select_difficulty(self, screen):
        screen.fill((255, 255, 255))
        Infotxt = "select difficulty"
        info = pg.font.Font(None, 36).render(Infotxt, True, (0, 0, 0))
        screen.blit(info, (110, 100))
        button_texts = ["3x3", "4x4", "5x5"]
        button_rects = []
        font = pg.font.Font(None, 36)
        
        for i, text in enumerate(button_texts):
            x = 30 + i * 120
            button_rect = pg.Rect(x, 150, 100, 130)
            button_rects.append(button_rect)
            pg.draw.rect(screen, (220, 220, 220), button_rect, 0, 10)
            text_surface = font.render(text, True, (0, 0, 0))
            screen.blit(text_surface, (x + 25, 165))
        
        pg.display.flip()
        
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return None
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    for i, button_rect in enumerate(button_rects):
                        if button_rect.collidepoint(mouse_pos):
                            return i + 3

    def makeBoard(self, size):
        """Generates a solvable board of given size"""
        self.size = size
        # Initialize the board
        self.board = [[i * size + j + 1 for j in range(size)] for i in range(size)]
        self.board[size - 1][size - 1] = 0  # Set the bottom-right corner as the blank space
        self.goal = deepcopy(self.board)  # Save the goal state for comparison
        self.shuffle_board()
        return self.board  # Ensure the board is returned

    def shuffle_board(self):
        """Shuffle the board by making random moves."""
        for _ in range(50):  # Increased shuffle steps for better randomness
            direction = random.choice(['up', 'down', 'left', 'right'])
            self.player_move(direction)

    def player_move(self, direction):
        """Moves the blank tile in the specified direction."""
        x, y = self.find_blank()
        if direction == 'up' and x > 0:
            self.board[x][y], self.board[x - 1][y] = self.board[x - 1][y], self.board[x][y]
        elif direction == 'down' and x < self.size - 1:
            self.board[x][y], self.board[x + 1][y] = self.board[x + 1][y], self.board[x][y]
        elif direction == 'left' and y > 0:
            self.board[x][y], self.board[x][y - 1] = self.board[x][y - 1], self.board[x][y]
        elif direction == 'right' and y < self.size - 1:
            self.board[x][y], self.board[x][y + 1] = self.board[x][y + 1], self.board[x][y]

class Npuzzle:
    def __init__(self, board):
        self.board = board
        self.size = len(board)
        self.goal = [[(i * self.size) + j + 1 for j in range(self.size)] for i in range(self.size)]
        self.goal[self.size - 1][self.size - 1] = 0
        self.start_time = time.time()

    def find_blank(self):
        """Find the blank space (0) in the puzzle."""
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return i, j

    def player_move(self, direction):
        """Moves the blank tile in the specified direction."""
        x, y = self.find_blank()
        if direction == 'up' and x > 0:
            self.board[x][y], self.board[x - 1][y] = self.board[x - 1][y], self.board[x][y]
        elif direction == 'down' and x < self.size - 1:
            self.board[x][y], self.board[x + 1][y] = self.board[x + 1][y], self.board[x][y]
        elif direction == 'left' and y > 0:
            self.board[x][y], self.board[x][y - 1] = self.board[x][y - 1], self.board[x][y]
        elif direction == 'right' and y < self.size - 1:
            self.board[x][y], self.board[x][y + 1] = self.board[x][y + 1], self.board[x][y]

    def is_goal(self):
        """Checks if the current board configuration is the goal state."""
        return self.board == self.goal

    def display(self, screen, move):
        """Displays the current puzzle state and move count on the screen."""
        tile_size = (400 / self.size) - 10
        pg.draw.rect(screen, (220, 220, 220), (5, 5, 390, 440), 0, 10)
        
        # Display moves and elapsed time
        font = pg.font.Font(None, 36)
        move_text = font.render(f"Moves: {move}", True, (0, 0, 0))
        screen.blit(move_text, (10, 10))

        elapsed_time = int(time.time() - self.start_time)
        time_text = font.render(f"Time: {elapsed_time}s", True, (0, 0, 0))
        screen.blit(time_text, (250, 10))

        # Draw tiles
        for i in range(self.size):
            for j in range(self.size):
                value = self.board[i][j]
                if value != 0:
                    font = pg.font.Font(None, 74)
                    text = font.render(str(value), True, (0, 0, 0))
                    x_pos = (j * tile_size) + 8 * (j + 1)
                    y_pos = (i * tile_size) + 58
                    pg.draw.rect(screen, (255, 255, 255), (x_pos, y_pos, tile_size, tile_size), 0, 10)
                    pg.draw.rect(screen, (150, 150, 255), (x_pos, y_pos, tile_size, tile_size), 2, 10)
                    screen.blit(text, (x_pos + tile_size / 2 - text.get_width() // 2,
                                       y_pos + tile_size / 2 - text.get_height() // 2))

    def display_goal(self, screen):
        """Displays the 'Goal!' message on the screen."""
        screen.fill((200, 200, 200))
        font = pg.font.Font(None, 74)
        text = font.render("clear!", True, (0, 0, 0))
        screen.blit(text, (200 - text.get_width() // 2, 200 - text.get_height() // 2))

def main():
    pg.init()
    pg.display.set_caption("N-Puzzle")
    screen = pg.display.set_mode((400, 450))
    clock = pg.time.Clock()
    move_count = 0
    running = True

    # Create the game board and select difficulty
    mb = MakeBoard()
    selected_size = mb.select_difficulty(screen)
    if not selected_size:
        pg.quit()
        return
    board = mb.makeBoard(selected_size)
    """elif selected_size == 3:
        board = [[1, 2, 3],
                [4, 0, 5],
                [6, 7, 8]]
    elif selected_size == 4:
        board = [[1, 2, 3, 4], 
                [5, 6, 7, 8], 
                [9, 10, 11, 12],
                [13, 14, 15, 0]]
    elif selected_size == 5:
        board = [[1, 2, 3, 4, 5], 
                [6, 7, 8, 9, 10], 
                [11, 12, 13, 14, 15],  
                [16, 17, 18, 19, 20], 
                [21, 22, 23, 24, 0]]"""

    puzzle = Npuzzle(board)
    
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    puzzle.player_move('up')
                    move_count += 1
                elif event.key == pg.K_DOWN:
                    puzzle.player_move('down')
                    move_count += 1
                elif event.key == pg.K_LEFT:
                    puzzle.player_move('left')
                    move_count += 1
                elif event.key == pg.K_RIGHT:
                    puzzle.player_move('right')
                    move_count += 1
                elif event.key == pg.K_s:
                    solver = NPuzzleSolver(puzzle.board, puzzle.goal)
                    solution = solver.a_star_search()
                    if solution:
                        for step in solution:
                            puzzle.board = step
                            screen.fill((255, 255, 255))
                            puzzle.display(screen, move_count)
                            pg.display.flip()
                            pg.time.wait(200)
                            move_count += 1
                        pg.time.wait(500)
                        running = False

        screen.fill((255, 255, 255))
        puzzle.display(screen, move_count)
        pg.display.flip()
        clock.tick(30)

        # Check for goal state
        if puzzle.is_goal():
            puzzle.display_goal(screen)
            pg.display.flip()
            pg.time.wait(1000)
            
            selected_size = mb.select_difficulty(screen)
            if not selected_size:
                pg.quit()
                return
            board = mb.makeBoard(selected_size)
            puzzle = Npuzzle(board)
            main()

    pg.quit()

if __name__ == "__main__":
    main()