import numpy as np
import math
import pygame


class Screen:
    screen_side = 600
    screen_x = screen_side
    screen_y = screen_side
    Center = np.array(([screen_x/2, screen_y/2]))
    inverseAdd = 2*Center
    coordinateZero = np.array(([0,0]))
    Invert = -1
    Angle = 0
    isRunning = True
     #sInverseAdd = inverseAdd+sqCoords+Center
     

    
class Contents(Screen):
    def __init__(self):
        self.squareCoords = None
        self.sideLength = None
        self.squareCenter = None

        
class ShapeConfig(Contents):
    def ShapeOneConfig(self):
        self.squareCoords = np.array((
            self.Center/2
            ))
        self.sideLength = 200
        self.squareCenter = np.array((
            [self.sideLength/2,self.sideLength/2]
            ))
        self.triangleTop = np.array(([0,self.sideLength*math.sqrt(3)/4]))

class Shapes(ShapeConfig):
    def Point(self, topLeftCoords, **kwargs):
        point = np.array(
            (
                topLeftCoords
            )
        )
        return point
    
    def line(self, sideLength, topLeftCoords, angle, **kwargs):
        line = np.array((
            topLeftCoords,
            topLeftCoords+[math.cos(angle),math.sin(angle)]*sideLength
        ))
        return line
    
    def Square(self, sideLength, topLeftCoords, angle, **kwargs):
        #print(topLeftCoords)
        x,y = topLeftCoords[0], topLeftCoords[1]
        square = np.array((
            [x,y],
            [x+sideLength,y],
            [x+sideLength,y+sideLength],
            [x,y+sideLength]
        ))
        return square
    
    
    
    def Triangle(self, sideLength, topCoords, angle, **kwargs):
        triangle = np.array((
            topCoords,
            topCoords+[sideLength/2,-sideLength*(math.sqrt(3)/2)],
            topCoords+[-sideLength/2,-sideLength*(math.sqrt(3)/2)]
        ))
        return triangle