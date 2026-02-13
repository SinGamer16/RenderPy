import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
import sys
import os

# Ensure project root is on sys.path so package imports work when running this file as a script
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

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

from graphics import create_mesh_from_obj, Skybox, Shader
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
    sun_light = DirectionalLight(
        direction=glm.normalize(glm.vec3(-1.0, -1.0, -0.3)),
        color=glm.vec3(1.0, 1.0, 0.9),
        intensity=1.0
    )
    world.add_component(sun, sun_light)

    # ---------- CAMERA ----------
    camera = Camera()
    cam_entity = world.create_entity()
    world.add_component(cam_entity, CameraComponent(camera))

    # ---------- MESH ----------
    mesh_vao, mesh_index_count = create_mesh_from_obj("../assets/objects/Iphone.obj")

    print(mesh_vao, mesh_index_count)

    mesh = world.create_entity()
    world.add_component(mesh, Transform(
        position=glm.vec3(0, 0, 0),
        rotation=glm.vec3(0, 0, 0),
        scale=glm.vec3(0.01)
    ))
    world.add_component(mesh, MeshRenderer(mesh_vao, mesh_index_count))
    

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
    time_elapsed = 0.0
    while True:
        dt = clock.tick(60) / 1000.0
        time_elapsed += dt

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
