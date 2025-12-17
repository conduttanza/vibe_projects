import pygame
import numpy as np
import dinamic_scene
s = dinamic_scene.Shapes()
c = dinamic_scene.Contents()
sConfig = dinamic_scene.ShapeConfig()
defaultScreen = dinamic_scene.Screen()
sConfig.ShapeOneConfig()

import math

pygame.init()
pygame.display.set_caption('Perspective')

#Constants from dinamic_scene.Screen

running = defaultScreen.isRunning
screen_side = defaultScreen.screen_side
screen_x = defaultScreen.screen_x
screen_y = defaultScreen.screen_y
center = defaultScreen.Center
inverseAdd = defaultScreen.inverseAdd
origin = defaultScreen.coordinateZero
invert = defaultScreen.Invert
angle = defaultScreen.Angle
triangleFixCoords = np.array((
        [-sConfig.sideLength/2, -sConfig.sideLength/2]
        ))

screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()

def mousePosition():
    Mx, My = pygame.mouse.get_pos()
    mousePos = np.array((
        [Mx,My]
    ))
    return mousePos

def distanceScaling(distance, maxDist):
    scale = 1 - distance/(maxDist*4)
    #print(scale)
    scale = max(0.1, scale)
    return scale

def drawWindow():
    mousePos = mousePosition()
    
    distance = math.sqrt(
            ((sConfig.squareCenter[0]+mousePos[0]-sConfig.sideLength/2)-center[0])**2+
            ((sConfig.squareCenter[1]+mousePos[1]-sConfig.sideLength/2)-center[1])**2
            ) 
    #print(squareDistance)
    
    scale = distanceScaling(
            distance, screen_side*math.sqrt(2)/2
            )
    screen.fill(
            (0,0,0)
            )
    
    sqSize = sConfig.sideLength*scale
    Center = sConfig.squareCenter*scale
    
    sqCoords = sConfig.squareCoords
    
#-----------------------------------------------------------------------------------------
#                                      LINE
#-----------------------------------------------------------------------------------------
    #this will move the circle along with the cursor
    if inverseCursorPoint == True:
        pygame.draw.circle(
                            screen,(255,255,255),(s.Point(origin)+mousePos)*(-1)+inverseAdd, 5
                            )
    if CursorPoint == True:
        pygame.draw.circle(
                            screen,(255,255,255),s.Point(origin)+mousePos, 5
                            )
        
    #simple movement line
    if inverseCursorLine == True:
        pygame.draw.line(
                            screen,(0,255,0), center,(s.Point(origin)+mousePos)*(-1)+inverseAdd, 2
                            )
    if CursorLine == True:
        pygame.draw.line(
                            screen,(0,255,0), center,s.Point(origin)+mousePos, 2
                            )
#-----------------------------------------------------------------------------------------
#                                      SQUARE
#-----------------------------------------------------------------------------------------
    
    centerSquareSize = sConfig.sideLength/2
    centerSquare = s.Square(centerSquareSize, center-centerSquareSize/2, angle)
    squareInverseAdd = inverseAdd+sqCoords+Center
    squareAdd = -(sqCoords+Center)
    
    #move a simple square
    
    squareBuild = s.Square(sqSize, sqCoords, angle)
    
    if inverseSquare == True:
        pygame.draw.polygon(screen,(0,0,255), (squareBuild+mousePos)*invert+squareInverseAdd, 5)
        for v in range(len(squareBuild)):
            pygame.draw.line(screen,(255,255,255), (squareBuild[v]+mousePos)*invert+squareInverseAdd, centerSquare[v-2], 1)
    if Square == True:
        pygame.draw.polygon(screen,(0,0,255), (squareBuild+mousePos)+squareAdd, 5)
        for v in range(len(squareBuild)):
            pygame.draw.line(screen,(255,255,255), (squareBuild[v]+mousePos)+squareAdd, centerSquare[v], 1)
    
#-----------------------------------------------------------------------------------------
#                                      Triangle
#-----------------------------------------------------------------------------------------
    
    triangleInverseAdd = inverseAdd+Center+triangleFixCoords*scale
    triangleTop = sConfig.triangleTop
    triangleSide = sConfig.sideLength
    triangleSize = triangleSide*scale
    triangleBuild = s.Triangle(triangleSize, triangleTop, angle)
    
    if inverseTriangle == True:
        pygame.draw.polygon(screen,(255,255,255), (triangleBuild+mousePos)*invert+triangleInverseAdd, 5)
    if Triangle == True:
        pygame.draw.polygon(screen,(255,255,255), triangleBuild+mousePos, 5)

try:
    while running:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                print('pygame quit successfully')
                running = False
        #POINT 
        inverseCursorPoint = False
        inverseCursorLine = False
        CursorPoint = True
        CursorLine = True
        #SQUARE
        inverseSquare = False
        Square = True
        #TRIANGLE
        inverseTriangle = False
        Triangle = True
        drawWindow()
        
        pygame.display.flip()
        clock.tick(60)
        
except KeyboardInterrupt:
    print('keyboard interrupt, quitting...')
    pygame.quit()
    print('pygame quit successfully')
    running = False
