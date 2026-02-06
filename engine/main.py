import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
import sys

from ecs import (
    World,
    Transform,
    MeshRenderer,
    CameraComponent,
    SkyboxComponent,
    RenderSystem,
    CameraSystem,
    DirectionalLight
)

from graphics import create_cube, Skybox, Shader
from maths import Camera
import glm


def main():
    pg.init()
    pg.display.set_mode((1280, 720), DOUBLEBUF | OPENGL)
    pg.event.set_grab(True)
    pg.mouse.set_visible(False)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_CUBE_MAP_SEAMLESS)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # ---------- ECS WORLD ----------
    world = World()

    # ------------ Sun ------------
    sun = world.create_entity()
    world.add_component(
        sun,
        DirectionalLight(
            direction=glm.normalize(glm.vec3(-1.0, -1.0, -0.3)),
            color=glm.vec3(1.0, 1.0, 0.9),
            intensity=1.0
        )
    )

    # ---------- CAMERA ----------
    camera = Camera()
    cam_entity = world.create_entity()
    world.add_component(cam_entity, CameraComponent(camera))

    # ---------- MESH ----------
    cube_vao, cube_index_count = create_cube()

    cube = world.create_entity()
    world.add_component(cube, Transform())
    world.add_component(cube, MeshRenderer(cube_vao, cube_index_count))

    # ---------- SKYBOX ----------
    sky = Skybox()

    sky_entity = world.create_entity()
    world.add_component(
        sky_entity,
        SkyboxComponent(
            cubemap=sky.texture,
            vao=sky.cube_vao
        )
    )

    # ---------- SYSTEMS ----------
    world.add_system(CameraSystem())
    world.add_system(RenderSystem())

    clock = pg.time.Clock()

    # ---------- MAIN LOOP ----------
    while True:
        dt = clock.tick(60) / 1000.0

        for e in pg.event.get():
            if e.type == QUIT:
                pg.quit()
                sys.exit()

        world.update(dt)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        world.render()

        pg.display.flip()


if __name__ == "__main__":
    main()
