import glm


class Transform:
    def __init__(self, position=glm.vec3(0), rotation=glm.vec3(0), scale=glm.vec3(1)):
        self.position = position
        self.rotation = rotation
        self.scale = scale

    def matrix(self):
        m = glm.mat4(1.0)
        m = glm.translate(m, self.position)
        m = glm.rotate(m, self.rotation.x, glm.vec3(1, 0, 0))
        m = glm.rotate(m, self.rotation.y, glm.vec3(0, 1, 0))
        m = glm.rotate(m, self.rotation.z, glm.vec3(0, 0, 1))
        m = glm.scale(m, self.scale)
        return m


class CameraComponent:
    def __init__(self, camera):
        self.camera = camera


class MeshRenderer:
    def __init__(self, vao, index_count):
        self.vao = vao
        self.index_count = index_count


class SkyboxComponent:
    def __init__(self, cubemap, vao):
        self.cubemap = cubemap
        self.vao = vao
        

class DirectionalLight:
    def __init__(self, direction, color=glm.vec3(1), intensity=1.0):
        self.direction = glm.normalize(direction)
        self.color = color
        self.intensity = intensity
