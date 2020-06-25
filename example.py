import pygame
import random
from particle_system import *

pygame.init()

# Display setup
FPS = 60
clock = pygame.time.Clock()

WIDTH = 1280
HEIGHT = 720

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle System")

# Colors
WHITE = 255, 255, 255,
BLACK = 0, 0, 0,

# Variables
surface = pygame.Surface((10, 10))
surface.fill((255, 150, 0))

area = Area((WIDTH // 2, HEIGHT // 2), (25, 25))
particle_system = ParticleSystem(area, FPS, 200, 1, [0, 0.5], [5, -12.5], 1)
particle_system.start_particles_with_surface(surface)

# Main loop
run = True

while run:
    clock.tick(FPS)

    win.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    mouse_pos = pygame.mouse.get_pos()
    particle_system.set_pos([*mouse_pos])  # Changes the position of the spawn of the particles (area)
    
    particle_system.reverse_all()  # For spread particles in the original direction and the opposite of the original direction | seems like mirroring
    
    particle_system.update()  # Update all the physics
    particle_system.draw(win)
    
    pygame.display.flip()

pygame.quit()
