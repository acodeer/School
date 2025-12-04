import pygame as pg
import time
import random

class MakeBoard:
    def __init__(self):
        self.board = []
        self.size = 0

    def inversion_count(self, board):
        # Flatten the board (exclude 0)
        flat_board = [num for row in board for num in row if num != 0]
        inversions = sum(
            1 for i in range(len(flat_board)) for j in range(i + 1, len(flat_board))
            if flat_board[i] > flat_board[j]
        )
        return inversions

    def is_solvable(self, board):
        size = len(board)
        inversions = self.inversion_count(board)

        # Find blank row from the bottom
        blank_row = next(size - i for i in range(size) for j in range(size) if board[i][j] == 0)
        
        # Check solvability
        if size % 2 == 1:
            return inversions % 2 == 0
        else:
            return (inversions % 2 == 1) if (blank_row % 2 == 0) else (inversions % 2 == 0)

    def find_blank(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return i, j

    def select_difficulty(self, screen):
        button_texts = ["3x3", "4x4", "5x5"]
        button_rects = []
        font = pg.font.Font(None, 36)
        
        for i, text in enumerate(button_texts):
            x = 30 + i * 120
            button_rect = pg.Rect(x, 150, 100, 50)
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

    def generate_solvable_board(self, size, shuffle_moves=100):
        self.size = size
        # 목표 상태를 기본 보드로 설정
        self.board = [[i * size + j + 1 for j in range(size)] for i in range(size)]
        self.board[size - 1][size - 1] = 0  # 빈 공간 설정
        
        # 목표 상태에서 무작위 이동을 통해 보드 섞기
        for _ in range(shuffle_moves):
            self.shuffle_move()
        
        # 마지막에 가용성 확인 후 불가용 상태면 타일 교환
        if not self.is_solvable(self.board):
            if self.board[0][0] != 0 and self.board[0][1] != 0:
                # 첫 두 타일을 교환하여 풀 수 있는 상태로 만듦
                self.board[0][0], self.board[0][1] = self.board[0][1], self.board[0][0]
            else:
                # 첫 두 타일이 0이면 다음 두 타일을 교환
                self.board[1][0], self.board[1][1] = self.board[1][1], self.board[1][0]
        
        return self.board


    def shuffle_move(self):
        x, y = self.find_blank()
        moves = []
        if x > 0:
            moves.append('up')
        if x < self.size - 1:
            moves.append('down')
        if y > 0:
            moves.append('left')
        if y < self.size - 1:
            moves.append('right')
        
        # 가능한 움직임 중 하나를 무작위로 선택하여 수행
        direction = random.choice(moves)
        if direction == 'up':
            self.board[x][y], self.board[x - 1][y] = self.board[x - 1][y], self.board[x][y]
        elif direction == 'down':
            self.board[x][y], self.board[x + 1][y] = self.board[x + 1][y], self.board[x][y]
        elif direction == 'left':
            self.board[x][y], self.board[x][y - 1] = self.board[x][y - 1], self.board[x][y]
        elif direction == 'right':
            self.board[x][y], self.board[x][y + 1] = self.board[x][y + 1], self.board[x][y]

            if not self.is_solvable(self.board):
                # Ensure board is solvable by performing a final swap if necessary
                if self.board[0][0] != 0 and self.board[0][1] != 0:
                    self.board[0][0], self.board[0][1] = self.board[0][1], self.board[0][0]
                else:
                    self.board[1][0], self.board[1][1] = self.board[1][1], self.board[1][0]

            return self.board
        
class Npuzzle:
    def __init__(self, board):
        self.board = board
        self.size = len(board)
        self.goal = [[j * self.size + i + 1 for i in range(self.size)] for j in range(self.size)]
        self.goal[self.size - 1][self.size - 1] = 0
        self.start_time = time.time()

    def Astar(self):
        g = 0 
        h = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != self.goal[i][j] and self.board[i][j] != 0:
                    h += 1
        return g + h
        
    def solve(self , move  , screen):
        route = ['up', 'down', 'left', 'right']
        best_move = None
        while not self.is_goal:
            temp_board = [row[:] for row in self.board]
            best_heuristic = float('inf')
            for direction in route:
                self.player_move(direction)
                temp_heuristic = self.Astar()
                if temp_heuristic < best_heuristic:
                    best_heuristic = temp_heuristic
                    best_move = direction
                self.board = [row[:] for row in temp_board]
            
            if best_move:
                self.player_move(best_move)
                move += 1
            

    def find_blank(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return i, j

    def player_move(self, direction):
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
        return self.board == self.goal

    def display(self, screen, move):
        tile_size = (400 / self.size) - 10

        pg.draw.rect(screen, (220, 220, 220), (5, 5, 390, 440), 0, 10)
        
        font = pg.font.Font(None, 36)
        move_text = font.render(f"Moves: {move}", True, (0, 0, 0))
        screen.blit(move_text, (10, 10))

        elapsed_time = int(time.time() - self.start_time)
        time_text = font.render(f"Time: {elapsed_time}s", True, (0, 0, 0))
        screen.blit(time_text, (250, 10))

        for i in range(self.size):
            for j in range(self.size):
                value = self.board[i][j]
                if value != 0:
                    font = pg.font.Font(None, 74)
                    text = font.render(str(value), True, (0, 0, 0))

                    pg.draw.rect(screen, (255, 255, 255), ((j * tile_size) + 8 * (j + 1), (i * tile_size) + 58, tile_size, tile_size), 0, 10)
                    pg.draw.rect(screen, (150, 150, 255), ((j * tile_size) + 8 * (j + 1), (i * tile_size) + 58, tile_size, tile_size), 2, 10)
                    screen.blit(text, ((j * tile_size + 8 * (j + 1) + tile_size / 2) - text.get_width() // 2,
                                       (i * tile_size + 58 + tile_size / 2) - text.get_height() // 2))

    def display_goal(self, screen):
        font = pg.font.Font(None, 74)
        text = font.render("Goal!", True, (0, 0, 0))
        screen.blit(text, (200 - text.get_width() // 2, 200 - text.get_height() // 2))

def main():
    pg.init()
    pg.display.set_caption("N-Puzzle")
    screen = pg.display.set_mode((400, 450))
    clock = pg.time.Clock()
    move_count = 0
    running = True

    mb = MakeBoard()
    selected_size = mb.select_difficulty(screen)
    if not selected_size:
        pg.quit()
        return
    elif selected_size == 3:
        board = [[1, 2, 3],
                [4, 0, 5],
                [6, 7, 8]]
    elif selected_size == 4:
        board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
    elif selected_size == 5:
        board = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 0]]

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
                    puzzle.solve(move_count , screen)

        screen.fill((255, 255, 255))
        puzzle.display(screen, move_count)
        pg.display.flip()
        clock.tick(30)

        if puzzle.is_goal():
            puzzle.display_goal(screen)
            pg.display.flip()
            pg.time.wait(3000)
            running = False

    pg.quit()

if __name__ == "__main__":
    main()