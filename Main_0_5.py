# Programa:
# - CREA IMAGEN DINAMICA A SUPERPONER
# - DETECTA UN MARCADOR ARUCO Y SUPERPONE LA IMAGEN DINAMICA
# - AL PRESIONAR ESPACIO, CAMBIA LOS VALORES DE LA LISTA entregada al inicio Y LA IMÁGEN DINÁNICA
# - los valores cambiaran hasta que se culmine la lista.

#IMPORTAR LIBRERIAS
import cv2
import numpy as np
import torch
from ultralytics import YOLO
#import pandas as pd
import os 

model_path = 'D:/00. ONEDRIVE/01. UNIVERSIDAD/2024_2\PDM\TORQUIA_project\TORQUIA/best.pt'

if os.path.exists(model_path):
    try:
        model = YOLO(model_path)
        print("Modelo cargado correctamente.")
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
else:
    print(f"El archivo {model_path} no existe o la ruta es incorrecta.")
#CREAR DICCIONARIO DE BUSQUEDA DE MARCADORES
parametros = cv2.aruco.DetectorParameters()
diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)

#CONFIG. CÁMARA
cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)

#LEER IMAGEN DE SILUETA - Vista 01 - "V01"
im_silueta = cv2.imread("V02_SILU.png")
    # Se podría mejorar cuando se obtiene la info del excel
    # con respecto de la vista en la que se está trabajando


flag_mod_torqueado=0
tornillo_a_ajustar=1 #info que se lee inicialmente del excel
v_estado = [1,0,0,0,0,0,0,0] #2:verde 1:azul 0:rojo #info que se lee inicialmente del excel
while True:
    # LEER EXCEL CON DATOS DE COORDENADAS DE TORNILLOS (X,Y,COLOR,NUM_VISTA)
    # datos=pd.read_excel("BD_Motor001.xlsx", sheet_name="InfoBD")
    # EMULAR DATOS OBTENIDOS DEL EXCEL
    cant_tornillos = 8 #cantidad de tornillos en la vista, se puede obtener del excel
    listaX=[71, 1175, 1175, 67, 804, 807, 438, 440]
    listaY=[101, 460, 101, 462, 105, 455, 103, 460]

    if flag_mod_torqueado==1:
        tornillo_a_ajustar = tornillo_a_ajustar + 1
        v_estado[tornillo_a_ajustar - 2] = 2
        v_estado[tornillo_a_ajustar - 1] = 1
    if flag_mod_torqueado==2:
        v_estado[tornillo_a_ajustar - 1] = 2



    # CREAR IMAGEN negra DE TORNILLOS, CIRCULOS CON COORDENADAS (X,Y,COLOR)

    alto, ancho, canales = im_silueta.shape
    imagen_negra = np.zeros((alto, ancho, canales), dtype=np.uint8)
    for i in range(0,cant_tornillos):
        if v_estado[i] == 2: #verde
            color_circulo=(0,255,0)
        elif v_estado[i] == 1: #azul
            color_circulo =(255, 0, 0)
        elif v_estado[i] == 0: #rojo
            color_circulo=(0,0,255)
        else:
            color_circulo=(0,0,0)
        cv2.circle(imagen_negra, (listaX[i],listaY[i]),30, color_circulo,5)


    # SUMAR IMAGENES CON DATOS DE TORNILLOS Y SILUETA
    im_silu_mod = cv2.add(im_silueta, imagen_negra)


    while True:
        # LEER IMAGENES DE CAMARA Y TRANSFORMAR A ESCALA DE GRISES
        ret, frame = cap.read()
        
        
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #PROCESAMIENTO DE IMAGEN Y OBTIENE LA UBICACIONDE CADA MARCADOR
        esquinas, ids, candidatos_malos = cv2.aruco.detectMarkers(gray, diccionario, parameters=parametros)

        # DIBUJAR EL MARCADOR OBTENIDO
        if np.all(ids != None):  # si existe marcadores aruco
            aruco = cv2.aruco.drawDetectedMarkers(frame, esquinas)

            # SUPRERPONER IMAGEN BRINDADA SEGÚN ESCALADO
            sc_x = 15  # Escala de imagen según marcador
            sc_y = 8
            sc=10
            c1 = (esquinas[0][0][0][0], esquinas[0][0][0][1])
            c2 = (sc_x * esquinas[0][0][1][0] - (sc_x - 1) * esquinas[0][0][0][0],
                  sc_y * esquinas[0][0][1][1] - (sc_y - 1) * esquinas[0][0][0][1])
            c3 = (sc_x * esquinas[0][0][2][0] - (sc_x - 1) * esquinas[0][0][0][0],
                  sc_y * esquinas[0][0][2][1] - (sc_y - 1) * esquinas[0][0][0][1])
            c4 = (sc_x * esquinas[0][0][3][0] - (sc_x - 1) * esquinas[0][0][0][0],
                  sc_y * esquinas[0][0][3][1] - (sc_y - 1) * esquinas[0][0][0][1])
            copy = frame
            # Leer imagen a superponer

            # imagen =cv2.imread("ID001Seccion1Vista1T.png")
            imagen = im_silu_mod
            tamanho = imagen.shape
            # print(tamaño)
            puntosRef_aruco = np.array([c1, c2, c3, c4])
            puntos_imagen = np.array([
                [0, 0],
                [(tamanho[1] - 1), 0],
                [(tamanho[1] - 1), (tamanho[0] - 1)],
                [0, (tamanho[0] - 1)]
            ], dtype=float)

            # Superponer
            h, estado = cv2.findHomography(puntos_imagen, puntosRef_aruco)
            # Transformacion de perspectiva
            perspectiva = cv2.warpPerspective(imagen, h, (copy.shape[1], copy.shape[0]))
            # cv2.fillConvexPoly(copy, puntos_aruco.astype(int), 0, 16)
            copy = cv2.addWeighted(src1=copy, alpha=1, src2=perspectiva, beta=1, gamma=0)
            cv2.imshow("Realidad Virtual", copy)
        # MUESTRA IMAGEN ORIGINAL BRINDAD POR CAMARA
        elif np.all(ids == None):
            results= model(frame)
            annotated_image=results[0].plot()
            
            
            for r in results:
                masks = r.masks  
                if masks is not None:
                # Iterar sobre cada máscara
                    for mask in masks.xy:  
                        contour = np.array(mask, dtype=np.int32)
                        #cv2.polylines(image, [contour], isClosed=True, color=(0, 255, 0), thickness=2)
                        # Aproximar los contornos para obtener las esquinas
                        # Encontrar las esquinas extremas
                        leftmost = contour[contour[:, 0].argmin()]  # Esquina izquierda
                        rightmost = contour[contour[ :, 0].argmax()]  # Esquina derecha
                        topmost = contour[contour[ :, 1].argmin()]  # Esquina superior
                        bottommost = contour[contour[ :, 1].argmax()]  # Esquina inferior

                        # Dibujar las esquinas en la imagen
                        cv2.circle(frame, leftmost, 20, (0, 0, 255), 5)  # Esquina izquierda (rojo)
                        cv2.circle(frame, rightmost, 20, (0, 255, 0), 5)  # Esquina derecha (verde)
                        cv2.circle(frame, topmost, 20, (255, 0, 0), 5)  # Esquina superior (azul)
                        cv2.circle(frame, bottommost, 20, (255, 255, 0), 5)  # Esquina inferior (amarillo)
            cv2.imshow("Realidad Virtual", annotated_image)
            # sc_x = 15  # Escala de imagen según marcador
            # sc_y = 8
            # sc=10
            # c1 = (esquinas[0][0][0][0], esquinas[0][0][0][1])
            # c2 = (sc_x * esquinas[0][0][1][0] - (sc_x - 1) * esquinas[0][0][0][0],
            #       sc_y * esquinas[0][0][1][1] - (sc_y - 1) * esquinas[0][0][0][1])
            # c3 = (sc_x * esquinas[0][0][2][0] - (sc_x - 1) * esquinas[0][0][0][0],
            #       sc_y * esquinas[0][0][2][1] - (sc_y - 1) * esquinas[0][0][0][1])
            # c4 = (sc_x * esquinas[0][0][3][0] - (sc_x - 1) * esquinas[0][0][0][0],
            #       sc_y * esquinas[0][0][3][1] - (sc_y - 1) * esquinas[0][0][0][1])
            
            # copy = frame
            # # Leer imagen a superponer

            # # imagen =cv2.imread("ID001Seccion1Vista1T.png")
            # imagen = im_silu_mod
            # tamanho = imagen.shape
            # # print(tamaño)
            # puntosRef_aruco = np.array([leftmost, rightmost, topmost, bottommost])
            # puntos_imagen = np.array([
            #     [0, 0],
            #     [(tamanho[1] - 1), 0],
            #     [(tamanho[1] - 1), (tamanho[0] - 1)],
            #     [0, (tamanho[0] - 1)]
            # ], dtype=float)

            # # Superponer
            # h, estado = cv2.findHomography(puntos_imagen, puntosRef_aruco)
            # # Transformacion de perspectiva
            # perspectiva = cv2.warpPerspective(imagen, h, (copy.shape[1], copy.shape[0]))
            # # cv2.fillConvexPoly(copy, puntos_aruco.astype(int), 0, 16)
            # copy = cv2.addWeighted(src1=copy, alpha=1, src2=perspectiva, beta=1, gamma=0)
            # cv2.imshow("Realidad Virtual", copy)                  
        
        else:
            cv2.imshow("Realidad Virtual", frame)
        
        # SI SE PRESIONA 'SPACE', ROMPER LOOP. ira a siguiente tornillo
        k = cv2.waitKey(1)
        if k == 32:
            break
        if k == 27:
            break
        
    
    if len(v_estado) == tornillo_a_ajustar:
        flag_mod_torqueado = 2
    else:
        flag_mod_torqueado = 1
# SI SE PRESIONA 'ESC', ROMPER LOOP
    #k = cv2.waitKey(1)
    if k == 27:
        break

# LIBERAR CAMARA
cap.release()

# CERRAR PESTAÑAS
cv2.destroyAllWindows()

# cv2.imshow('Imagen Negra', im_silu_mod)
# cv2.waitKey(0)
# cv2.destroyAllWindows()