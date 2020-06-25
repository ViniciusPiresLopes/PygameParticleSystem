import pygame
import random


class Pause:
    STOP = 0
    PROCESS = 1


class Particle:
    def __init__(self, pos=[0, 0], gravity=[0, 0.98], speed=[0, 0], gravity_effect=1):
        self.visible = False
        self.image = None
        self.frame = 0
        self.pos = pos
        self.gravity = gravity
        self.gravity_effect = gravity_effect
        self.speed = speed
        self.started = False
        self._on_start = None
    
    def start(self):
        if self._on_start is not None:
            self._on_start(self)

        self.started = True
        self.show()
    
    def reset(self, pos):
        if self._on_start is not None:
            self._on_start(self)

        self.pos = pos
        self.frame = 0
        self.show()
    
    def on_start(self, func):
        self._on_start = func

    def load_image(self, path):
        self.image = pygame.image.load(path)

    def load_surface(self, surface):
        self.image = surface

    def draw(self, window):
        if self.visible and self.image != None:
            window.blit(self.image, self.pos)

    def update(self):
        if self.started:
            self.pos[0] += self.speed[0] + (self.gravity[0] * self.frame * self.gravity_effect)
            self.pos[1] += self.speed[1] + (self.gravity[1] * self.frame * self.gravity_effect)

            self.frame += 1

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False


class ParticleArray:
    def __init__(self):
        self.array = []

    def add(self, particle):
        self.array.append(particle)

    def pop(self, index=-1):
        self.array.pop(index)

    def draw(self, window):
        for particle in self.array:
            particle.draw(window)

    def update(self):
        for particle in self.array:
            particle.update()


class Area:
    def __init__(self, pos, size, color=(0, 0, 150)):
        self.color = color
        self.pos = pos
        self.size = size


class ParticleSystem(ParticleArray):
    def __init__(self, area: Area, fps, particles, lifetime=1, gravity=[0, 0.98], start_speed=[0, 0], gravity_effect=1, pause_state=Pause().PROCESS, visible=True):
        super().__init__()

        # Area
        self.color = area.color
        self.pos = [*area.pos]
        self.size = [*area.size]
        
        # Particle System
        self.image = None
        self.fps = fps
        self.particles = particles
        self.gravity = gravity
        self.gravity_effect = gravity_effect
        self.speed = start_speed
        self.lifetime = lifetime
        self.generation_time = self.lifetime / self.particles
        self.frames = 0
        self.current_frame = 0
        self.current_particle = 0
        self.pause_state = pause_state
        self.visible = visible

    def draw(self, window):
        if self.visible:
            for particle in self.array:
                particle.draw(window)

    def start_particles(self, img_path):
        if self.image is not None:
            self.image = pygame.image.load(img_path)
        else:
            self.image = None

        for i in range(self.particles):
            pos = self.generate_pos()
            particle = Particle(pos, self.gravity, self.speed, self.gravity_effect)
            self.add(particle)
            self.array[i].load_surface(self.image)
    
    def start_particles_with_surface(self, surface):
        self.image = surface

        for i in range(self.particles):
            pos = self.generate_pos()
            particle = Particle(pos, [0, 0.1])
            self.add(particle)
            self.array[i].load_surface(self.image)
    
    def load_image(self, img_path):
        self.image = pygame.image.load(img_path)

        for particle in self.array:
            particle.load_surface(self.image)
    
    def load_surface(self, surface):
        self.image = surface

        for particle in self.array:
            particle.load_surface(self.image)

    def generate_pos(self):
        return [random.randint(self.pos[0], self.pos[0] + self.size[0]), random.randint(self.pos[1], self.pos[1] + self.size[1])]

    def update(self):
        if self.pause_state == Pause().PROCESS:
            for particle in self.array:
                particle.update()

                if particle.frame == self.sec2frame(self.lifetime):
                    pos = self.generate_pos()

                    particle.hide()
                    particle.reset(pos)

            if self.frames >= self.sec2frame(self.generation_time) * (self.current_particle + 1):
                self.array[self.current_particle].start()
                
                if self.current_particle == self.particles - 1:
                    self.current_particle = 0
                else:
                    self.current_particle += 1
            
            if self.current_frame == self.fps:
                self.current_frame = 0
            else:
                self.current_frame += 1

            self.frames += 1

    def sec2frame(self, sec):
        return sec * self.fps

    def frame2sec(self, frame):
        return frame / self.fps
    
    def on_start(self, func):
        for particle in self.array:
            particle.on_start(func)
    
    def update_variables(self):
        for particle in self.array:
            if particle.visible == False:
                particle.pos = self.generate_pos()
                particle.gravity = self.gravity
                particle.speed = self.speed
                particle.gravity_effect = self.gravity_effect
        
    def set_pos(self, pos):
        self.pos = pos
        self.update_variables()
    
    def get_pos(self, pos):
        self.pos = pos
    
    def set_gravity(self, gravity):
        self.gravity = gravity
        self.update_variables()
    
    def get_gravity(self):
        return self.gravity
    
    def reverse_gravity_y(self):
        self.gravity[1] *= -1
        self.update_variables()

    def reverse_gravity_x(self):
        self.gravity[0] *= -1
        self.update_variables()
    
    def set_speed(self, speed):
        self.speed = speed
        self.update_variables()
    
    def get_speed(self):
        return self.speed
    
    def set_size(self, size):
        self.size = size
    
    def get_size(self):
        return self.size

    def set_pause(self, pause_state):
        self.pause_state = pause_state

    def get_pause(self):
        return self.pause_state

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def reverse_all(self):
        speed = self.get_speed()
        gravity = self.get_gravity()
        
        self.set_speed([speed[0] * -1, speed[1] * -1])
        self.set_gravity([gravity[0] * -1, gravity[1] * -1])
