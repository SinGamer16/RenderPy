import numpy as np
import cv2
from pathlib import Path

def generate_cubemap_from_hdr(hdr_path, output_dir, face_size=512):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Load HDR image
    print(f"Loading HDR image: {hdr_path}")
    hdr_image = cv2.imread(hdr_path, cv2.IMREAD_ANYDEPTH | cv2.IMREAD_COLOR)
    
    if hdr_image is None:
        print(f"Error: Could not load {hdr_path}")
        return
    
    # Check if loaded as grayscale, convert to 3 channels if needed
    if len(hdr_image.shape) == 2:
        print("Warning: HDR image loaded as grayscale, converting to 3 channels")
        hdr_image = cv2.cvtColor(hdr_image, cv2.COLOR_GRAY2BGR)
    
    height, width = hdr_image.shape[:2]
    print(f"HDR image size: {width}x{height}, channels: {hdr_image.shape[2]}")
    
    # Convert BGR to RGB
    if hdr_image.shape[2] == 3:
        hdr_image = cv2.cvtColor(hdr_image, cv2.COLOR_BGR2RGB)
    
    # Apply tone mapping to HDR data
    hdr_image = tone_map(hdr_image)
    
    # Generate cubemap faces
    faces = {
        "right": generate_face(hdr_image, "right", face_size),
        "left": generate_face(hdr_image, "left", face_size),
        "top": generate_face(hdr_image, "top", face_size),
        "bottom": generate_face(hdr_image, "bottom", face_size),
        "front": generate_face(hdr_image, "front", face_size),
        "back": generate_face(hdr_image, "back", face_size),
    }
    
    # Save faces as PNG
    for face_name, face_data in faces.items():
        # Normalize to 8-bit for PNG
        face_uint8 = np.clip(face_data * 255, 0, 255).astype(np.uint8)
        # Convert RGB back to BGR for OpenCV
        face_bgr = cv2.cvtColor(face_uint8, cv2.COLOR_RGB2BGR)
        output_path = Path(output_dir) / f"{face_name}.png"
        cv2.imwrite(str(output_path), face_bgr)
        print(f"Saved: {output_path}")

def tone_map(hdr_image, exposure=1, gamma=1):
    """Apply tone mapping and gamma correction to HDR image."""
    # Ensure float32
    hdr_image = hdr_image.astype(np.float32)
    
    # Simple exposure adjustment
    mapped = hdr_image * exposure
    
    # Use simple tone mapping: sqrt is gentler than Reinhard
    mapped = np.sqrt(mapped)
    
    # Gamma correction
    mapped = np.power(np.maximum(mapped, 0.0), 1.0 / gamma)
    
    return np.clip(mapped, 0, 1)

def generate_face(hdr_image, face, size):
    """Generate a single cubemap face from a panorama."""
    face_data = np.zeros((size, size, 3), dtype=np.float32)
    
    h, w = hdr_image.shape[:2]
    
    for y in range(size):
        for x in range(size):
            # Normalize coordinates to -1..1
            u = (x / size) * 2 - 1
            v = (y / size) * 2 - 1
            
            # Get direction vector based on face
            # Standard OpenGL cubemap face orientations
            if face == "right":
                dx, dy, dz = 1, v, u
            elif face == "left":
                dx, dy, dz = -1, v, -u
            elif face == "top":
                dx, dy, dz = u, 1, v
            elif face == "bottom":
                dx, dy, dz = u, -1, -v
            elif face == "front":
                dx, dy, dz = u, v, -1
            elif face == "back":
                dx, dy, dz = -u, v, 1
            
            # Convert direction to spherical coordinates
            length = np.sqrt(dx*dx + dy*dy + dz*dz)
            dx, dy, dz = dx/length, dy/length, dz/length
            
            # Spherical to panorama
            lon = np.arctan2(dz, dx)
            lat = np.arcsin(dy)
            
            # Map to image coordinates
            px = int(((lon + np.pi) / (2 * np.pi)) * w) % w
            py = int(((lat + np.pi / 2) / np.pi) * h) % h
            py = (h - 1 - py) % h  # Flip Y axis
            
            face_data[y, x] = hdr_image[py, px]
    
    return face_data

if __name__ == "__main__":
    hdr_file = "assets/env/hdr/sky.hdr"
    output_directory = "assets/env/cubemap"
    
    generate_cubemap_from_hdr(hdr_file, output_directory)
    print("Cubemap generation complete!")