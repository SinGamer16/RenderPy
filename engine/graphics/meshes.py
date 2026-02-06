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
    # BACK (-Z)
     0,  2,  1,
     0,  3,  2,

    # FRONT (+Z)
     4,  5,  6,
     4,  6,  7,

    # LEFT (-X)
     8,  10, 9,
     8, 11, 10,

    # RIGHT (+X)
    12, 13, 14,
    12, 14, 15,

    # BOTTOM (-Y)
    16, 18, 17,
    16, 19, 18,

    # TOP (+Y)
    20, 21, 22,
    20, 22, 23,
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
