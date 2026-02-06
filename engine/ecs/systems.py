from OpenGL.GL import *
import glm

from ecs.components import (
    Transform,
    CameraComponent,
    MeshRenderer,
    DirectionalLight
)

from graphics.shader import Shader
from graphics.skybox import Skybox


# =========================================================
# Camera System
# =========================================================

class CameraSystem:
    def __init__(self):
        self.world = None

    def update(self, dt):
        for _, cam in self.world.get(CameraComponent):
            cam.camera.update(dt)


# =========================================================
# Render System
# =========================================================

class RenderSystem:
    def __init__(self):
        self.world = None

        self.object_shader = Shader(
            "./assets/shaders/object.vert",
            "./assets/shaders/object.frag"
        )

        self.skybox = Skybox()

        # Global GL state (safe)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # -------------------------------------------------
        # Camera
        # -------------------------------------------------
        camera = next(iter(self.world.get(CameraComponent)))[1].camera
        view = camera.view_matrix()
        projection = camera.projection_matrix()

        # -------------------------------------------------
        # SKYBOX PASS
        # -------------------------------------------------
        skybox_view = glm.mat4(glm.mat3(view))

        glDepthMask(GL_FALSE)
        glDepthFunc(GL_LEQUAL)
        glDisable(GL_CULL_FACE)

        self.skybox.draw(skybox_view, projection)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glDepthFunc(GL_LESS)
        glDepthMask(GL_TRUE)

        # -------------------------------------------------
        # SUN (Directional Light)
        # -------------------------------------------------
        sun = None
        for _, light in self.world.get(DirectionalLight):
            sun = light
            break

        if sun is None:
            sun_dir = glm.vec3(-1, -1, -1)
            sun_color = glm.vec3(1, 1, 1)
            sun_intensity = 1.0
        else:
            sun_dir = sun.direction
            sun_color = sun.color
            sun_intensity = sun.intensity


        # -------------------------------------------------
        # OBJECT PASS
        # -------------------------------------------------
        self.object_shader.use()

        self.object_shader.set_mat4("view", view)
        self.object_shader.set_mat4("projection", projection)
        self.object_shader.set_vec3("viewPos", camera.position)

        self.object_shader.set_vec3("sunDirection", sun.direction)
        self.object_shader.set_vec3("sunColor", sun.color)
        self.object_shader.set_float("sunIntensity", sun.intensity)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.skybox.texture)
        self.object_shader.set_int("skybox", 0)

        for ent, transform in self.world.get(Transform):
            mesh = self.world.try_get(ent, MeshRenderer)
            if not mesh:
                continue

            self.object_shader.set_mat4("model", transform.matrix())

            glBindVertexArray(mesh.vao)
            glDrawElements(
                GL_TRIANGLES,
                mesh.index_count,
                GL_UNSIGNED_INT,
                None
            )

        glBindVertexArray(0)
