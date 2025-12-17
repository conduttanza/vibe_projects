import math
import numpy as np
import pygame

lengthX = 600
lengthY = 600

pygame.init()
screen = pygame.display.set_mode((lengthX, lengthY))
clock = pygame.time.Clock()

center_x = lengthX // 2
center_y = lengthY // 2
center = np.array([center_x, center_y])

angle = 0 
movement = np.array([
    [0,0],
    [0,1],
    [1,0]
])

movementx = movement[2]
movementy = movement[1]

delta_center = np.array([
    [0,100],
    [100,0],
    [0,0]
])

point = np.array([
    [0,0],
    [100,100]
])

point2 = point.copy()
point3 = point.copy()

def move_point_sin_hz(point, angle):
    matrix_rotation = np.array([
        [math.sin(angle), 0],
        [0,0]
    ])
    return point @ matrix_rotation

def move_point_cos_ver(point, angle):
    matrix_rotation = np.array([
        [0,0],
        [0,math.cos(angle)]
    ])
    return point @ matrix_rotation

mem_sin_hz = []
mem_cos_ver = []

#mem_sin_hz = deque(maxlen=100)
#mem_cos_ver = deque(maxlen=1000)

MAX_POINTS = lengthX // 2

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    angle += 0.02
    
    point_sin_hz = np.array([move_point_sin_hz(p, angle) for p in point]) + center
    point_cos_ver = np.array([move_point_cos_ver(p, angle) for p in point2]) + center
    #print("mpoint: ", mpoint)

    screen.fill((0,0,0))
    
    for sin in mem_sin_hz:
        pygame.draw.circle(screen, (255,255,255), (sin[0], sin[1]) + delta_center[0], 1)
    for cos in mem_cos_ver:
        pygame.draw.circle(screen, (255,255,255), (cos[0], cos[1]) + delta_center[1], 1)
    pygame.draw.line(screen, (0, 255, 0), center + delta_center[2], point_sin_hz[1] + delta_center[0], 3)
    pygame.draw.line(screen, (255, 0, 0), center + delta_center[2], point_cos_ver[1] + delta_center[1], 3)
    #pygame.draw.circle(screen, (255,255,255), point3[0] + center, 3)
    #pygame.draw.circle(screen, (255,255,255), point3[1] + center, 3)
        
    mem_sin_hz.append(point_sin_hz[1])
    mem_cos_ver.append(point_cos_ver[1])
    #print(point_sin_hz[1])
    if len(mem_sin_hz) > MAX_POINTS:
        mem_sin_hz.pop(0)
    if len(mem_cos_ver) > MAX_POINTS:
        mem_cos_ver.pop(0)
    
    for i in range(len(mem_sin_hz)):
        mem_sin_hz[i] = mem_sin_hz[i] + movementy
    for i in range(len(mem_cos_ver)):
        mem_cos_ver[i] = mem_cos_ver[i] + movementx
    

    pygame.draw.line(screen, (255,255,255), [lengthX // 2,0] + center, [-(lengthX // 2),0] + center, 1)
    pygame.draw.line(screen, (255,255,255), [0,lengthY // 2] + center, [0,-(lengthY // 2)] + center, 1)
    pygame.display.flip()
    clock.tick(60)