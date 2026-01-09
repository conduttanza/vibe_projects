import time
import math
import pygame


def velocity_funct(vel, acceleration, dtime):
    vx, vy, vz = vel[0] + acceleration[0]*dtime, vel[1] + acceleration[1]*dtime, vel[2] + acceleration[2]*dtime
    return [vx, vy, vz]
def total_acceleration(gravity_masses, position, mass_position):
    
    G = 6.674e-11
    mposX, mposY, mposZ = mass_position[0], mass_position[1], mass_position[2]
    posX, posY, posZ = position[0], position[1], position[2]
    dX, dY, dZ = mposX - posX, mposY - posY, mposZ - posZ
    distance = math.sqrt(dX**2 + dY**2 + dZ**2)
    
    if distance == 0:
            return [0, 0, 0]

    ax, ay, az = 0, 0, 0
    for mass in gravity_masses:
        a_mag = G * mass / distance**2
        ax += a_mag * dX / distance
        ay += a_mag * dY / distance
        az += a_mag * dZ / distance
    acc = math.sqrt(ax**2 + ay**2 + az**2)
    print("gravity : ", acc)
    return [ax, ay, az]

def instant_particle_pos(position, velocity, acceleration, dtime):
    velX, velY, velZ = velocity[0], velocity[1], velocity[2]
    posX, posY, posZ = position[0], position[1], position[2]
    accX, accY, accZ = acceleration[0], acceleration[1], acceleration[2]
    
    dposX, dposY, dposZ = (accX * (dtime**2)) + velX * dtime, (accY * (dtime**2)) + velY * dtime, (accZ * (dtime**2)) + velZ * dtime
    
    newposX, newposY, newposZ = posX + dposX, posY + dposY, posZ + dposZ
    
    return newposX, newposY, newposZ

def draw_simulation(screen, mass_position, particle_position, scale, mass_color=(0,255,0), particle_color=(255,0,0)):
    #CHATGPT this idk pygame
    
    screen.fill((0, 0, 0))  # clear screen

    # Mass (draw at bottom center if z ignored)
    # Mass at center of screen
    mass_px = (screen.get_width()//2,
           screen.get_height()//2)
    pygame.draw.circle(screen, mass_color, mass_px, 150)

    # Particle
    particle_px = (mass_px[0] + int(particle_position[0]*scale),
               mass_px[1] - int(particle_position[1]*scale))

    pygame.draw.circle(screen, particle_color, particle_px, 5)

    pygame.display.flip()
    
def main():
    pygame.init()
    WIDTH, HEIGHT = 500, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    scale = HEIGHT / 20e6  # for example
    position = [0, 6.3714e6, 0]
    mass = 1
    vel = [7800, 0, 0]
    #acceleration = [0, 0, 0]
    gravity_masses = [5.972e24]
    mass_position = [0, 0, 0]
    dtime = 1
    timecount = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        aX, aY, aZ = total_acceleration(gravity_masses, position, mass_position)
        acceleration = [aX, aY, aZ]

        vx, vy, vz = velocity_funct(vel, acceleration, dtime)
        vel = [vx, vy, vz]
        tot_vel = math.sqrt(vx**2 + vy**2 + vz**2)
        print("velocity: ", tot_vel)
        
        x, y, z= instant_particle_pos(position, vel, acceleration, dtime)
        newX, newY, newZ = x, y, z
        position = [newX, newY, newZ]
        tot_distance = math.sqrt(newX**2 + newY**2 + newZ**2)
        print("distance: ", tot_distance)
        timecount += 1
        timepassed = timecount * dtime
        print("t passed: ", timepassed, " seconds")
        print("--------------------------")
        draw_simulation(screen, mass_position, position, scale)
        clock.tick(60)  # limit FPS
        time.sleep(dtime)

main()