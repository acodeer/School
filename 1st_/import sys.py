import sys
import pygame
from pygame.locals import *

FPS = 30
FramePerSec = pygame.time.Clock()
## pygame 기능 사용을 시작하는 명령어 ##
pygame.init()

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

gamedisplay = pygame.display.set_mode((1024, 768))
gamedisplay.fill(WHITE)

pygame.draw.line(gamedisplay, BLUE, (100, 100), (500, 100), 5)
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    gamedisplay.fill(WHITE)  # 화면을 흰색으로 채움
    pygame.display.update()    # 화면 업데이트
    FramePerSec.tick(FPS)      # FPS에 맞춰 프레임 조정


pygame.quit()
sys.exit()