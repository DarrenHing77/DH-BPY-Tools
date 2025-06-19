import bpy
import os

# Directories to search
search_dirs = [
    r"C:\Users\Darren\OneDrive\Pictures",
    r"E:\BackupTextures",
]

# Recursively collect all image files from search_dirs
def index_texture_files():
    texture_map = dict()
    for base_dir in search_dirs:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                filepath = os.path.join(root, file)
                texture_map[file.lower()] = filepath
    return texture_map


texture_files = index_texture_files()

# Iterate over Blender images
for image in bpy.data.images:
    if image.source != 'FILE':
        continue  # Skip packed/generated images

    original_path = bpy.path.abspath(image.filepath)
    if os.path.exists(original_path):
        continue  # This one is fine

    filename = os.path.basename(image.filepath).lower()

    if filename in texture_files:
        found_path = texture_files[filename]
        print(f"Fixing {image.name} -> {found_path}")
        image.filepath = bpy.path.relpath(found_path)
        image.reload()
    else:
        print(f"Missing: {image.name} ({filename}) not found")

print("Done fixing shit!")
