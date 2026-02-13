import glm
import pygame as pg

class Camera:
    def __init__(self):
        self.position = glm.vec3(0,0,5)
        self.yaw = -90
        self.pitch = 0
        self.speed = 5
        self.sensitivity = 0.1

    def update(self, dt):
        keys = pg.key.get_pressed()
        front = self.front()
        right = self.right()

        if keys[pg.K_w]: self.position += front * self.speed * dt
        if keys[pg.K_s]: self.position -= front * self.speed * dt
        if keys[pg.K_a]: self.position -= right * self.speed * dt
        if keys[pg.K_d]: self.position += right * self.speed * dt

        if keys[pg.K_ESCAPE]:
            if pg.mouse.get_visible:
                pg.event.set_grab(False)
                pg.mouse.set_visible(True)
        if pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_visible == False:
                pg.event.set_grab(True)
                pg.mouse.set_visible(False)
        


        mx, my = pg.mouse.get_rel()
        self.yaw += mx * self.sensitivity
        self.pitch -= my * self.sensitivity
        self.pitch = max(-89, min(89, self.pitch))

    def front(self):
        return glm.normalize(glm.vec3(
            glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch)),
            glm.sin(glm.radians(self.pitch)),
            glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        ))
    
    def right(self):
        return glm.normalize(glm.cross(self.front(), glm.vec3(0,1,0)))

    def view_matrix(self):
        return glm.lookAt(self.position, self.position + self.front(), glm.vec3(0,1,0))

    def projection_matrix(self):
        return glm.perspective(glm.radians(60), 1280/720, 0.1, 100)
