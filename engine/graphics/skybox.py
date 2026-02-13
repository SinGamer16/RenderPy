from OpenGL.GL import *
import pygame as pg
from .shader import Shader
import numpy as np
import os


def _resolve_path(path: str) -> str:
    if os.path.isabs(path):
        return path
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(root, path)

class Skybox:
    def __init__(self):
        self.shader = Shader(
            "assets/shaders/skybox.vert",
            "assets/shaders/skybox.frag"
        )
        self.texture = self.load_cubemap()
        self.cube_vao = self.create_cube()

    def load_cubemap(self):
        faces = ["right","left","top","bottom","front","back"]
        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, tex)

        for i, face in enumerate(faces):
            img_path = _resolve_path(f"assets/env/cubemap/{face}.png")
            img = pg.image.load(img_path)
            data = pg.image.tostring(img, "RGB", True)
            w, h = img.get_size()
            glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X+i,
                         0, GL_RGB, w, h, 0,
                         GL_RGB, GL_UNSIGNED_BYTE, data)

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        return tex

    def create_cube(self):
        vertices = np.array([
            # back
            -1,-1,-1,  1,-1,-1,  1, 1,-1,
            1, 1,-1, -1, 1,-1, -1,-1,-1,

            # front
            -1,-1, 1,  1,-1, 1,  1, 1, 1,
            1, 1, 1, -1, 1, 1, -1,-1, 1,

            # left
            -1, 1, 1, -1, 1,-1, -1,-1,-1,
            -1,-1,-1, -1,-1, 1, -1, 1, 1,

            # right
            1, 1, 1,  1, 1,-1,  1,-1,-1,
            1,-1,-1,  1,-1, 1,  1, 1, 1,

            # bottom
            -1,-1,-1,  1,-1,-1,  1,-1, 1,
            1,-1, 1, -1,-1, 1, -1,-1,-1,

            # top
            -1, 1,-1,  1, 1,-1,  1, 1, 1,
            1, 1, 1, -1, 1, 1, -1, 1,-1,
        ], dtype=np.float32)

        vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)

        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)

        return vao


    def draw(self, view, projection):
        glDepthFunc(GL_LEQUAL)
        self.shader.use()
        self.shader.set_mat4("view", view)
        self.shader.set_mat4("projection", projection)
        glBindVertexArray(self.cube_vao)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        glDepthFunc(GL_LESS)
