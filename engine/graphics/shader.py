from OpenGL.GL import *
import glm
from OpenGL import GL as gl
import numpy as np
import os


def _resolve_path(path: str) -> str:
    """Resolve a possibly-relative path against the project root.

    If `path` is absolute, return it unchanged. Otherwise assume it's relative to
    the repository root (two directories above this file's parent) and return
    the absolute path.
    """
    if os.path.isabs(path):
        return path
    # shader.py is in <root>/engine/graphics/shader.py -> root is three levels up
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(root, path)


class Shader:
    def __init__(self, vs_path, fs_path):
        vs_path = _resolve_path(vs_path)
        fs_path = _resolve_path(fs_path)

        with open(vs_path, "r") as f:
            vs_source = f.read()
        with open(fs_path, "r") as f:
            fs_source = f.read()

        self.program = glCreateProgram()

        vs = self._compile(vs_source, GL_VERTEX_SHADER)
        fs = self._compile(fs_source, GL_FRAGMENT_SHADER)

        glAttachShader(self.program, vs)
        glAttachShader(self.program, fs)
        glLinkProgram(self.program)

        # ---- Link check ----
        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            error = glGetProgramInfoLog(self.program).decode()
            raise RuntimeError(f"Shader link error:\n{error}")

        glDeleteShader(vs)
        glDeleteShader(fs)

    def _compile(self, source, shader_type):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)

        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(shader).decode()
            stype = "VERTEX" if shader_type == GL_VERTEX_SHADER else "FRAGMENT"
            raise RuntimeError(f"{stype} shader compile error:\n{error}")

        return shader

    def use(self):
        glUseProgram(self.program)

    # ---------- Uniform helpers ----------

    def set_mat4(self, name, mat):
        loc = glGetUniformLocation(self.program, name)
        if loc != -1:
            glUniformMatrix4fv(loc, 1, GL_FALSE, glm.value_ptr(mat))

    def set_vec3(self, name, v):
        loc = glGetUniformLocation(self.program, name)
        if loc != -1:
            glUniform3f(loc, v.x, v.y, v.z)

    def set_float(self, name, value):
        loc = glGetUniformLocation(self.program, name)
        if loc != -1:
            glUniform1f(loc, value)

    def set_int(self, name, value):
        loc = glGetUniformLocation(self.program, name)
        if loc != -1:
            glUniform1i(loc, value)


# cubemap Renderer

def _normalize(v):
    v = np.array(v, dtype=np.float32)
    n = np.linalg.norm(v)
    if n == 0:
        return v
    return v / n


def look_at(eye, center, up):
    eye = np.array(eye, dtype=np.float32)
    center = np.array(center, dtype=np.float32)
    up = np.array(up, dtype=np.float32)

    f = _normalize(center - eye)
    s = _normalize(np.cross(f, up))
    u = np.cross(s, f)

    # Column-major (OpenGL)
    M = np.identity(4, dtype=np.float32)
    M[0, 0:3] = s
    M[1, 0:3] = u
    M[2, 0:3] = -f
    T = np.identity(4, dtype=np.float32)
    T[0:3, 3] = -eye
    return M @ T


def perspective(fovy_deg, aspect, near, far):
    fovy = np.deg2rad(fovy_deg)
    f = 1.0 / np.tan(fovy / 2.0)
    M = np.zeros((4, 4), dtype=np.float32)
    M[0, 0] = f / aspect
    M[1, 1] = f
    M[2, 2] = (far + near) / (near - far)
    M[2, 3] = (2.0 * far * near) / (near - far)
    M[3, 2] = -1.0
    return M