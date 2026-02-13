from OpenGL.GL import *
import numpy as np
import ctypes

def load_obj(path):
    positions = []
    normals = []

    vertices = []
    indices = []

    unique_map = {}
    index_counter = 0

    with open(path, "r") as f:
        for line in f:
            if line.startswith("v "):
                positions.append(list(map(float, line.split()[1:4])))

            elif line.startswith("vn "):
                normals.append(list(map(float, line.split()[1:4])))

            elif line.startswith("f "):
                face = line.split()[1:]

                # triangulate (fan method)
                for i in range(1, len(face) - 1):
                    tri = [face[0], face[i], face[i + 1]]

                    for vert in tri:
                        parts = vert.split("/")

                        v_idx = int(parts[0]) - 1

                        # detect format safely
                        n_idx = None
                        if len(parts) == 3 and parts[2] != "":
                            n_idx = int(parts[2]) - 1
                        elif len(parts) == 2 and "//" in vert:
                            n_idx = int(parts[1]) - 1

                        key = (v_idx, n_idx)

                        if key not in unique_map:
                            unique_map[key] = index_counter
                            index_counter += 1

                            vertices.extend(positions[v_idx])

                            if n_idx is not None and n_idx < len(normals):
                                vertices.extend(normals[n_idx])
                            else:
                                vertices.extend([0.0, 0.0, 0.0])  # fallback normal

                        indices.append(unique_map[key])


    return (
        np.array(vertices, dtype=np.float32),
        np.array(indices, dtype=np.uint32)
    )


def create_mesh_from_obj(path):
    vertices, indices = load_obj(path)

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    ebo = glGenBuffers(1)

    glBindVertexArray(vao)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    stride = 6 * vertices.itemsize

    # position
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

    # normal
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))

    glBindVertexArray(0)

    return vao, len(indices)
