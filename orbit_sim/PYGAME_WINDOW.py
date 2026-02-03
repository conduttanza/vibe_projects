#PYGAME WINDOW
import pygame
from threading import Thread
from orbit import Orbit
import numpy as np

class view():
    def __init__(self):
        self.side_x = 600
        self.side_y = self.side_x
        self.running = True
        self.orbit = Orbit()
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.side_x, self.side_y))
        self.orbit_thread = Thread(target=self.update, daemon=False)
        self.orbit_thread.start()
            
    def update(self):
        self.main()
    
    def main(self):
        center = np.array([self.side_x/2,self.side_y/2])
        try:
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.orbit.running = False
                        pygame.quit()
                self.screen.fill((0,0,0))
                
                #center as a test
                pygame.draw.circle(self.screen, (255,0,0), center, 5)
                planets = self.orbit.drawPlanets()
                for p in range(len(planets)):
                    #print(planets[p])
                    pygame.draw.circle(self.screen, (0,0,255), (int(planets[p][0]),int(planets[p][1]))+center, 5)
                pygame.display.flip()
                self.clock.tick(60)
        except KeyboardInterrupt:
            self.running = False
            self.orbit.running = False
            pygame.quit()

view()