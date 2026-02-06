from OpenGL.GL import *
import glm


class Shader:
    def __init__(self, vs_path, fs_path):
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
