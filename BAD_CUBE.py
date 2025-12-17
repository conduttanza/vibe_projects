import math
import pygame
import numpy as np

# -- Non, je ne parle pas francois, sono italiano. --

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

#once upon a time, there was a blender artist

Yo_will_you_read_this_vertices = np.array([
    [-1, -1, -1],
    [ 1, -1, -1],
    [ 1,  1, -1],
    [-1,  1, -1],
    [-1, -1,  1],
    [ 1, -1,  1],
    [ 1,  1,  1],
    [-1,  1,  1]
])

ctrlc_ctrlv_vertices = Yo_will_you_read_this_vertices.copy()

#he was so inspired by the world, never had he seen such beauty

l_inital_angle = 0 

#he wanted to draw it, model it and know it

Zamn_them_EDGEs = [(0,1), (1,2), (2,3), (3,0),
         (4,5), (5,6), (6,7), (7,4),
         (0,4), (1,5), (2,6), (3,7)]

#that joy was shortly lived, cuz as heth found the Blender...

Draw_them_FACEs = [(0, 1, 2, 3),
    (4, 5, 6, 7),
    (0, 1, 5, 4),
    (2, 3, 7, 6),
    (0, 3, 7, 4),
    (1, 2, 6, 5)]

def make_cube_do_the_jiggle(point, l_initial_angle):
    rotation_upon_the_z_axis = np.array([
        [math.cos(l_initial_angle), -math.sin(l_initial_angle), 0],
        [math.sin(l_initial_angle),  math.cos(l_initial_angle), 0],
        [0, 0, 1]
    ])
    rotation_upon_the_x_axis = np.array([
        [1, 0, 0],
        [0, math.cos(l_initial_angle), -math.sin(l_initial_angle)],
        [0, math.sin(l_initial_angle),  math.cos(l_initial_angle)]
    ])
    zamn_let_it_jiggle_point = point @ rotation_upon_the_z_axis @ rotation_upon_the_x_axis
    return zamn_let_it_jiggle_point

#...he also found the r/helpBlender subreddit.

def CUBE_really_bad_topology_challenge(point):
    factor = 200 / (point[2] + 5)
    Px = point[0] * factor + 400
    Py = point[1] * factor + 400
    return (Px, Py)

jiggle = True

#do the thug shake?

this_value_idk_yet = 1.5

yoyoyo_this_remembers = []

while jiggle:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    rotated_one_houndred_cigarettes = np.array([make_cube_do_the_jiggle(v, l_inital_angle) for v in Yo_will_you_read_this_vertices])
    rotated_dos_double = np.array([make_cube_do_the_jiggle(v, l_inital_angle) for v in ctrlc_ctrlv_vertices])
    
    scaled_them_points = rotated_dos_double * this_value_idk_yet
    
    projected_to_thy_screen = [CUBE_really_bad_topology_challenge(v) for v in rotated_one_houndred_cigarettes]
    projected_the_second_time_to_thy_screen = [CUBE_really_bad_topology_challenge(v) for v in scaled_them_points]
    
    #had this been another universe, blender would have been different, noble, majestic...
    faces_with_depth = []

    camera_z = -5.0
    for this_particular_point in projected_the_second_time_to_thy_screen:
        pygame.draw.circle(screen, (64, 224, 208), (int(this_particular_point[0]), int(this_particular_point[1])), 1)
    for memory_point in yoyoyo_this_remembers:
        pygame.draw.circle(screen, (64, 224, 208), (int(memory_point[0]), int(memory_point[1])), 1)
    
    #but this one? also in this one blender is a canvas for inspiring artists
    
    for face in Draw_them_FACEs:
        i0, i1, i2, i3 = face

        v0 = rotated_one_houndred_cigarettes[i0]
        v1 = rotated_one_houndred_cigarettes[i1]
        v2 = rotated_one_houndred_cigarettes[i2]

        normal = np.cross(v1 - v0, v2 - v0)

        view_vec = np.array([0.0, 0.0, camera_z]) - v0

        avg_z = (v0[2] + rotated_one_houndred_cigarettes[i1][2] +
                rotated_one_houndred_cigarettes[i2][2] +
                rotated_one_houndred_cigarettes[i3][2]) / 4.0

        faces_with_depth.append((avg_z, face))
        
    faces_with_depth.sort(reverse=True)
    
    for _, face in faces_with_depth:
        pts = [projected_to_thy_screen[i] for i in face]
        pts_int = [(int(p[0]), int(p[1])) for p in pts]
        pygame.draw.polygon(screen, (255, 0, 255), pts_int)
    
    #never have i ever 3d modeled before, enjoy math art -->

    for edge in Zamn_them_EDGEs:
        pygame.draw.line(screen, (255,255,255), projected_to_thy_screen[edge[0]], projected_to_thy_screen[edge[1]], 2)

    yoyoyo_this_remembers.extend(projected_the_second_time_to_thy_screen)

    l_inital_angle += 0.02
    this_value_idk_yet += 0.001
    
    pygame.display.flip()
    clock.tick(60)

# Ps. 
# if you read this, wish me luck, i may go study physics in uni 
# i love physics but i know they say its hard

pygame.quit()