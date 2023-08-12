import os


def generateImagePath(current_dir, folder, filename):
    #return os.path.join(current_dir, '..', '..', 'recursos', 'imagenes', folder, filename)
    # Subir dos directorios desde base_path
    root_path = os.path.join(current_dir, '..', '..')
    # Ahora construye la ruta a la imagen
    image_path = os.path.join(root_path, 'recursos', 'imagenes', folder, filename)
    return os.path.normpath(image_path)