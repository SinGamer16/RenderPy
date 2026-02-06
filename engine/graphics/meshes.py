from OpenGL.GL import *
import numpy as np
import ctypes


def create_cube():
    vertices = np.array([
        # positions        normals
        -1,-1,-1,  0, 0,-1,
         1,-1,-1,  0, 0,-1,
         1, 1,-1,  0, 0,-1,
        -1, 1,-1,  0, 0,-1,

        -1,-1, 1,  0, 0, 1,
         1,-1, 1,  0, 0, 1,
         1, 1, 1,  0, 0, 1,
        -1, 1, 1,  0, 0, 1,

        -1,-1,-1, -1, 0, 0,
        -1, 1,-1, -1, 0, 0,
        -1, 1, 1, -1, 0, 0,
        -1,-1, 1, -1, 0, 0,

         1,-1,-1,  1, 0, 0,
         1, 1,-1,  1, 0, 0,
         1, 1, 1,  1, 0, 0,
         1,-1, 1,  1, 0, 0,

        -1,-1,-1,  0,-1, 0,
        -1,-1, 1,  0,-1, 0,
         1,-1, 1,  0,-1, 0,
         1,-1,-1,  0,-1, 0,

        -1, 1,-1,  0, 1, 0,
        -1, 1, 1,  0, 1, 0,
         1, 1, 1,  0, 1, 0,
         1, 1,-1,  0, 1, 0,
    ], dtype=np.float32)

    indices = np.array([
         0,  1,  2,  2,  3,  0,
         4,  5,  6,  6,  7,  4,
         8,  9, 10, 10, 11,  8,
        12, 13, 14, 14, 15, 12,
        16, 17, 18, 18, 19, 16,
        20, 21, 22, 22, 23, 20
    ], dtype=np.uint32)

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    ebo = glGenBuffers(1)

    glBindVertexArray(vao)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    stride = 6 * vertices.itemsize

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))

    glBindVertexArray(0)

    return vao, len(indices)
