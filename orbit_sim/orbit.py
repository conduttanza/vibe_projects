#orbital calculator
import math
import numpy as np
from threading import Thread

class Object():
    def sun(self):
        self.mass = 10
        self.radius = 10

        self.position = np.array((
            [0,0]
        ))
        return {'sunmass':self.mass, 'sunradius':self.radius, 'sunposition':self.position}
        
    def planets(self):
        self.masses = [10,20,10]
        self.radiuses = [4,6,2]
        self.positions = np.array((
            [100,0],
            [0,200],
            [50,50]
        ))
        return {'mass':self.masses, 'radius':self.radiuses, 'position':self.positions}
    
class Orbit():
    def __init__(self):
        self.G = 10**3
        obj = Object()
        self.pData = obj.planets()
        self.new_planets = np.copy(self.pData['position']).astype(float)
        self.velocities = np.zeros_like(self.pData['position'], dtype=float)
        self.sun = obj.sun()
        self.dt = 1/60
        self.started = False
        self.running = True
        self.planets = obj.planets()
        for i in range(len(self.planets['mass'])):
            r_vec = self.new_planets[i] - self.sun['sunposition']
            self.velocities[i] = self.calcInitialV(r_vec)
        
        self.orbit_thread = Thread(target=self.update, daemon=True)
        self.orbit_thread.start()
        
    def update(self):
        self.started = True
        while self.running:
            for i in range(len(self.planets['mass'])):
                self.new_planets[i], self.velocities[i] = self.changeCourse(i)
            import time
            time.sleep(self.dt)
            
    def drawPlanets(self):
        return self.new_planets
        
    def calcInitialV(self, r_vec):
        # magnitude for circular orbit
        r_mag = np.linalg.norm(r_vec)
        v_mag = math.sqrt(self.G * self.sun['sunmass'] / r_mag)
        # perpendicular direction for circular orbit
        v_vec = np.array([-r_vec[1], r_vec[0]]) / r_mag * v_mag
        return v_vec
    
    def changeCourse(self, index):
        r_vec = self.new_planets[index] - self.sun['sunposition']
        r_mag = np.linalg.norm(r_vec)
        if r_mag == 0:
            r_mag = 1e-2

        # acceleration toward the sun
        a_vec = -self.G * self.sun['sunmass'] / r_mag**2 * (r_vec / r_mag)

        # symplectic Euler integration
        v_vec = self.velocities[index] + a_vec * self.dt
        new_pos = self.new_planets[index] + v_vec * self.dt

        return new_pos, v_vec