import math
import itertools
import time
import random
from collections import deque

class Problem:
    def __init__(self):
        infile = open("tsp299.txt", "r")
        data = infile.read().split()
        infile.close()
        self.tours_iter = None

        data = [eval(x) for x in data]
        self.city_count = data[0]
        data.pop(0)
        self.city_num = []
        self.pos_x = []
        self.pos_y = []
        for i in range(0, self.city_count * 3, 3):
            self.city_num.append(data[i])
            self.pos_x.append(data[i + 1])
            self.pos_y.append(data[i + 2])

        # 도시 사이의 거리
        self.distance = [[0 for j in range(self.city_count)] for i in range(self.city_count)]
        for i in range(self.city_count - 1):
            for j in range(i + 1, self.city_count):
                self.distance[i][j] = int(math.sqrt((self.pos_x[i] - self.pos_x[j]) ** 2 +
                                                (self.pos_y[i] - self.pos_y[j]) ** 2) + 0.5)
                self.distance[j][i] = self.distance[i][j]

        # 추가: 순열 반복자 초기값 None
        self.tours_iter = None

    def getLength(self, tour):
        length = 0
        for i in range(len(tour) - 1):
            length += self.distance[tour[i]][tour[i + 1]]
        length += self.distance[tour[-1]][tour[0]]
        return length

    def ExhaustiveSearch(self, tour):

        global best
        startTime = time.time()
        sum_distance = self.getLength(tour)
        tours = itertools.permutations(range(1, tsp.city_count))

        for perm in tours:
            if time.time() - startTime > 600:
                print("시간 초과")
                return best[1]
            tour = (0,) + perm
            sum_distance = self.getLength(tour)
            
            if sum_distance < best[1]:
                best = [tour, sum_distance]
                print("새로운 최단 거리:", best[1])

        return sum_distance        
    
    def simulated_annealing(self , startTime):
 
        global best
        startTime = time.time()
        T = 1000
        alpha = 0.999999
        initial = list(range(1, self.city_count))
        random.shuffle(initial)
        current =[0] + initial
        current_distance = self.getLength(current)
        
        while True:
            
            i, j = random.sample(range(1, self.city_count), 2)
            new_tour = current[:]
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
            new_distance = self.getLength(new_tour)
            delta = new_distance - current_distance
            
            if delta < 0 or random.random() < math.exp(-delta / T):
                current = new_tour
                current_distance = new_distance
                
                if current_distance < best[1]:
                    best = [tuple(current), current_distance]
                    print("새로운 최단 거리:", best[1])
            
            T *= alpha
            
            if T < 1 or time.time() - startTime > 600:
                break
            
    def steepestAscent(self):
        # (기존 구현과 동일)
        global best
        initial = list(range(1, self.city_count))
        random.shuffle(initial)
        current =[0] + initial
        current_distance = self.getLength(current)
        start_time = time.time()

        while True :
            if time.time() - start_time > 600 :
                print("시간 초과")
                break

            for i in range(1, self.city_count):
                for j in range(i + 1, self.city_count):
                    neighbor = current[:]
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                    neighbor_distance = self.getLength(neighbor)

                    if neighbor_distance < best[1]:
                        best = [tuple(neighbor), neighbor_distance]
                        print("새로운 최단 거리:", best[1])
            
            if best[1] < current_distance:
                best_neighbor = list(best[0])
                current = best_neighbor
                current_distance = best[1]
            else:
                break

        return current, current_distance 
        
    def firstChoiceHillClimbing(self):
        
        global best
        initial = list(range(1, self.city_count))
        random.shuffle(initial)
        current =[0] + initial
        current_distance = self.getLength(current)
        start_time = time.time()
        
        while True:
            if(time.time() - start_time > 600):
                print("시간 초과")
                break
            
            i, j = random.sample(range(1, self.city_count), 2)
            new_tour = current[:]
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
            new_distance = self.getLength(new_tour)
                
            if new_distance < current_distance:
                current = new_tour
                current_distance = new_distance
                improvement_found = True
                    
                if current_distance < best[1]:
                    best = [tuple(current), current_distance]
                    print("새로운 최단 거리:", best[1])
            
                
        return current, current_distance

    def tabuSearch(self, tabu_size=30, time_limit_secs=600):
        global best
        start_time = time.time()

        # 1. 초기 해 생성 (0번 도시 고정)
        initial = list(range(1, self.city_count))
        random.shuffle(initial)
        current_tour = [0] + initial
        current_distance = self.getLength(current_tour)

        # best를 초기 해로 설정
        if current_distance < best[1]:
            best = [tuple(current_tour), current_distance]

        # 2. 타부 리스트(deque) 초기화
        tabu_list = deque(maxlen=tabu_size)
        
        iteration_count = 0
        while True:
            # 시간 제한 체크
            if time.time() - start_time > time_limit_secs:
                print("시간 초과")
                break

            iteration_count += 1
            best_neighbor = None
            best_neighbor_distance = float('inf')
            best_move = None

            # 3. 모든 이웃 탐색
            for i in range(1, self.city_count):
                for j in range(i + 1, self.city_count):
                    move = tuple(sorted((i, j)))
                    
                    # 4. 타부 리스트에 있는 이동(move)이면 건너뜀
                    if move in tabu_list:
                        continue

                    neighbor = current_tour[:]
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                    neighbor_distance = self.getLength(neighbor)

                    # 타부가 아닌 이웃 중 가장 좋은 것을 찾음
                    if neighbor_distance < best_neighbor_distance:
                        best_neighbor = neighbor
                        best_neighbor_distance = neighbor_distance
                        best_move = move
            
            if best_neighbor is None:
                print("탐색할 이웃이 없어 종료합니다.")
                break

            # 5. 가장 좋은 (타부가 아닌) 이웃으로 이동 (더 나빠져도 상관없음)
            current_tour = best_neighbor
            current_distance = best_neighbor_distance
            
            # 6. 이번에 수행한 이동을 타부 리스트에 추가
            tabu_list.append(best_move)

            # 7. 전체 최단 거리(best) 갱신
            if current_distance < best[1]:
                best = [tuple(current_tour), current_distance]
                print("새로운 최단 거리: " , best[1])

        return best
        
tsp = Problem()
best = [None, 10000000]
tours = None

def main():
    global tours, best
    start_time = time.time()    
    tours = itertools.permutations(range(1, tsp.city_count))
    best = [None, 10000000]
    seed = {1 ,2 ,3}

    # --- 실행할 알고리즘 선택 ---
    #tsp.ExhaustiveSearch((0, ) + next(tours)) # 완전탐색
    tsp.steepestAscent() # Steepest Ascent
    #tsp.simulated_annealing(start_time) # Simulated Annealing
    #tsp.firstChoiceHillClimbing() # First Choice Hill Climbing
    #tsp.tabuSearch() # Tabu Search
    # -------------------------

    print("\n최종 결과")
    print("최단 경로 :", best[0])
    print("최단 거리 :", best[1])
    print("경과 시간 :", time.time() - start_time, "초")

if __name__ == "__main__":
    main()