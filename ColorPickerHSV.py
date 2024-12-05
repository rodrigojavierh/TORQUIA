#color picker HSV
import cv2
import numpy as np

# Función para calcular el rango HSV de una imagen
def calcular_rango_hsv(imagen_path):
    # Leer la imagen
    imagen = cv2.imread(imagen_path)
    
    # Convertir la imagen de BGR a HSV
    imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    
    # Calcular el rango de valores en cada canal HSV
    h_min, s_min, v_min = np.min(imagen_hsv, axis=(0, 1))
    h_max, s_max, v_max = np.max(imagen_hsv, axis=(0, 1))
    
    # Mostrar el rango de valores
    print(f"Rango de H: {h_min} - {h_max}")
    print(f"Rango de S: {s_min} - {s_max}")
    print(f"Rango de V: {v_min} - {v_max}")
    
    # Retornar los valores mínimos y máximos en formato (H, S, V)
    return (h_min, h_max), (s_min, s_max), (v_min, v_max)

# Ruta de la imagen
imagen_path = 'D:/00_ONEDRIVE/00_temp\hsv3.png'

# Calcular y mostrar el rango HSV
rango_h, rango_s, rango_v = calcular_rango_hsv(imagen_path)