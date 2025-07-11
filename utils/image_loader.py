import cv2
import os

def cargar_overlay(path="img.png", escala=0.18):
    if not os.path.exists(path):
        print(f"Advertencia: No se encontró {path}. Continuando sin imagen overlay.")
        return None

    img = cv2.imread(path)
    if img is not None:
        try:
            img = cv2.resize(img, (0, 0), None, escala, escala)
            print(f"✓ Imagen {path} cargada correctamente")
            return img
        except Exception as e:
            print(f"Error al redimensionar imagen: {e}")
    else:
        print(f"Error: No se pudo cargar la imagen {path}")
    return None
