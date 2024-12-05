#ColorPickerHSV_v2

import cv2
import numpy as np

# Lista para almacenar los rangos de HSV de las selecciones
rangos_hsv = []

# Función para manejar los eventos de mouse
def seleccionar_region(event, x, y, flags, param):
    global x_inicial, y_inicial, seleccionando, imagen

    if event == cv2.EVENT_LBUTTONDOWN:
        # Inicio de la selección
        x_inicial, y_inicial = x, y
        seleccionando = True

    elif event == cv2.EVENT_MOUSEMOVE:
        # Actualizar el rectángulo a medida que el mouse se mueve
        if seleccionando:
            imagen_temp = imagen.copy()
            cv2.rectangle(imagen_temp, (x_inicial, y_inicial), (x, y), (0, 255, 0), 2)
            cv2.imshow("Camera", imagen_temp)

    elif event == cv2.EVENT_LBUTTONUP:
        # Fin de la selección
        seleccionando = False
        cv2.rectangle(imagen, (x_inicial, y_inicial), (x, y), (0, 255, 0), 2)
        # Extraer la región seleccionada
        region = imagen[y_inicial:y, x_inicial:x]
        # Convertir la región seleccionada a HSV
        hsv_region = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        # Obtener el rango de valores HSV
        h_min, s_min, v_min = np.min(hsv_region, axis=(0, 1))
        h_max, s_max, v_max = np.max(hsv_region, axis=(0, 1))
        # Guardar el rango en la lista
        rangos_hsv.append(((h_min, s_min, v_min), (h_max, s_max, v_max)))
        print(f"Rango seleccionado: Min={h_min, s_min, v_min}, Max={h_max, s_max, v_max}")

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Definir las variables globales
x_inicial, y_inicial = -1, -1
seleccionando = False

# Configurar la ventana y los eventos del mouse
cv2.namedWindow("Camera")
cv2.setMouseCallback("Camera", seleccionar_region)

while True:
    # Capturar el frame de la cámara
    ret, imagen = cap.read()
    if not ret:
        break
    
    # Mostrar el frame en tiempo real
    cv2.imshow("Camera", imagen)
    
    # Esperar una tecla
    key = cv2.waitKey(1) & 0xFF
    
    # Si presionamos ESC, salimos y calculamos el rango global
    if key == 27:  # 27 es el código de la tecla ESC
        if rangos_hsv:
            # Calcular el rango global (min y max de todos los rangos)
            h_min_global = min([rango[0][0] for rango in rangos_hsv])
            s_min_global = min([rango[0][1] for rango in rangos_hsv])
            v_min_global = min([rango[0][2] for rango in rangos_hsv])
            h_max_global = max([rango[1][0] for rango in rangos_hsv])
            s_max_global = max([rango[1][1] for rango in rangos_hsv])
            v_max_global = max([rango[1][2] for rango in rangos_hsv])

            print(f"Rango global HSV: Min=({h_min_global}, {s_min_global}, {v_min_global}), "
                  f"Max=({h_max_global}, {s_max_global}, {v_max_global})")
        
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()

