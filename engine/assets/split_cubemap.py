from PIL import Image
import os

# INPUT
input_image = "assets/cubemap.png"
output_dir = "assets/skybox"

os.makedirs(output_dir, exist_ok=True)

img = Image.open(input_image).convert("RGB")
w, h = img.size

# Horizontal cross must be 4:3
if w % 4 != 0 or h % 3 != 0:
    raise ValueError("Invalid horizontal cross dimensions")

face = w // 4
if h != face * 3:
    raise ValueError("Image is not a 4x3 horizontal cross")

# Crop boxes (x1, y1, x2, y2)
faces = {
    "right":  (2*face, 1*face, 3*face, 2*face),  # +X
    "left":   (0*face, 1*face, 1*face, 2*face),  # -X
    "top":    (1*face, 0*face, 2*face, 1*face),  # +Y
    "bottom": (1*face, 2*face, 2*face, 3*face),  # -Y
    "front":  (1*face, 1*face, 2*face, 2*face),  # +Z
    "back":   (3*face, 1*face, 4*face, 2*face),  # -Z
}

for name, box in faces.items():
    face_img = img.crop(box)

    # Flip vertically for OpenGL
    face_img = face_img.transpose(Image.FLIP_TOP_BOTTOM)



    face_img.save(os.path.join(output_dir, f"{name}.png"))

print("Cubemap split correctly for OpenGL!")
