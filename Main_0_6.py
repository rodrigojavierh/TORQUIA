# Programa:
# - CREA IMAGEN DINAMICA A SUPERPONER
# - DETECTA UN MARCADOR ARUCO y marcadores verdes Y SUPERPONE LA IMAGEN DINAMICA
# - AL PRESIONAR ESPACIO, CAMBIA LOS VALORES DE LA LISTA entregada al inicio Y LA IMÁGEN DINÁNICA
# - los valores cambiaran hasta que se culmine la lista.

#IMPORTAR LIBRERIAS
import cv2
import numpy as np

import math

def mover_punto_arbitrario(puntos, punto_arbitrario):
    # Encontramos el índice del punto arbitrario
    idx = puntos.index(punto_arbitrario)

    # Dividimos la lista en dos partes: antes y después del punto arbitrario
    parte_antes = puntos[:idx]
    parte_despues = puntos[idx+1:]

    # Movemos los puntos antes del punto arbitrario al final de la lista
    nueva_lista = [punto_arbitrario] + parte_despues + parte_antes 

    return nueva_lista
# Función para calcular el centroide de un cuadrilátero
def calcular_centroid(puntos):
    x_c = sum([p[0] for p in puntos]) / len(puntos)
    y_c = sum([p[1] for p in puntos]) / len(puntos)
    return (x_c, y_c)

# Función para calcular el ángulo con respecto al centroide
def calcular_angulo(punto, centroid):
    return math.atan2(punto[1] - centroid[1], punto[0] - centroid[0])

# Función principal para ordenar las coordenadas
def ordenar_puntos(puntos):
    centroid = calcular_centroid(puntos)  # Calcular el centroide
    # Calcular los ángulos para cada punto
    puntos_ordenados = sorted(puntos, key=lambda p: calcular_angulo(p, centroid))
    return puntos_ordenados

# Función para asignar las posiciones del cuadrilátero
def asignar_posiciones(puntos):
    puntos_ordenados = ordenar_puntos(puntos)
    posiciones = {
        "Arriba a la izquierda": puntos_ordenados[0],
        "Arriba a la derecha": puntos_ordenados[1],
        "Abajo a la derecha": puntos_ordenados[2],
        "Abajo a la izquierda": puntos_ordenados[3]
    }
    return posiciones

# Función para calcular el rectángulo paralelo a los lados del cuadrado
def calcular_rectangulo(cuadrado, punto_exterior):
    # Los puntos del cuadrado son las 4 esquinas
    # Encontramos el punto más alejado
    punto_cuadrado = cuadrado[0]

    # El rectángulo tiene los lados paralelos a los del cuadrado, por lo que necesitamos
    # los vectores de los lados del cuadrado. Tomamos dos vectores de lados adyacentes.
    vector_1 = np.array(cuadrado[1]) - np.array(cuadrado[0])
    vector_2 = np.array(cuadrado[3]) - np.array(cuadrado[0])
    vector_3 = np.array(punto_exterior) - np.array(cuadrado[0])

    # Coeficientes de las ecuaciones
    A = np.array([[vector_1[0], vector_2[0]], [vector_1[1], vector_2[1]]])
    #print(A)

    # Constantes
    B = vector_3

    # Resolver el sistema
    soluciones = np.linalg.solve(A, B)

    # Mostrar los resultados
    a, b = soluciones
    #print(f"La solución es: x = {a}, y = {b}")

    # Calculamos el punto del rectángulo que corresponde al punto exterior
    rectangulo_punto_1 = np.round(punto_cuadrado).astype(int)
    rectangulo_punto_3 = np.round(punto_exterior).astype(int)

    # Los otros dos puntos del rectángulo se pueden calcular usando los vectores
    rectangulo_punto_2 = np.round(rectangulo_punto_1 + vector_1*a).astype(int)
    rectangulo_punto_4 = np.round(rectangulo_punto_1 + vector_2*b).astype(int)

    # Devolvemos los 4 puntos del rectángulo
    return [rectangulo_punto_1, rectangulo_punto_2, rectangulo_punto_3,rectangulo_punto_4]

#CREAR DICCIONARIO DE BUSQUEDA DE MARCADORES
parametros = cv2.aruco.DetectorParameters()
diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)

GreenBajo=np.array([60,75,170],np.uint8)
GreenAlto=np.array([80,220,255], np.uint8)


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
        frameHSV= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV )
        maskGreen=cv2.inRange(frameHSV,GreenBajo,GreenAlto)
        # PROCESAMIENTO DE IMAGEN Y OBTIENE LA UBICACIONDE CADA MARCADOR
        esquinas, ids, candidatos_malos = cv2.aruco.detectMarkers(gray, diccionario, parameters=parametros)
        
        # DIBUJAR EL MARCADOR OBTENIDO
        if np.all(ids != None):  # si existe marcadores aruco
            aruco = cv2.aruco.drawDetectedMarkers(frame, esquinas)
            contornos,_= cv2.findContours(maskGreen, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            coordenadas= []
            for c in contornos:
                area=cv2.contourArea(c)
                #print(area)
                if area>40:
                    M=cv2.moments(c)
                    if (M["m00"]==0): M["m00"]=1
                    x=int(M["m10"]/M["m00"])
                    y=int(M['m01']/M["m00"])
                    coordenadas.append((x,y))
                    nuevoContorno=cv2.convexHull(c)
                    cv2.circle(frame,(x,y),7,(0,255,0),-1)
                    cv2.putText(frame,'{},{}'.format(x,y),(x+10,y),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),1,cv2.LINE_AA)
                    cv2.drawContours(frame,[nuevoContorno], 0, (255,0,0), 3)
                # SUPRERPONER IMAGEN BRINDADA SEGÚN ESCALADO
            sc_x = 15  # Escala de imagen según marcador
            sc_y = 8
            sc=10
            ar1 = (esquinas[0][0][0][0], esquinas[0][0][0][1])
            ar2 = (esquinas[0][0][1][0], esquinas[0][0][1][1])
            ar3 = (esquinas[0][0][2][0], esquinas[0][0][2][1])
            ar4 = (esquinas[0][0][3][0], esquinas[0][0][3][1])
            ar=[ar1,ar2,ar3,ar4] #puntos del cuadrado aruco
            c1=ar1
            
            if len(coordenadas)==1:
                c3 = coordenadas[0] #punto exterior al cuadrado
                puntos_rectangulo = calcular_rectangulo(ar, c3)

                c1  = puntos_rectangulo[0]
                c2  = puntos_rectangulo[1]
                c3  = puntos_rectangulo[2]
                c4  = puntos_rectangulo[3]
            
            elif len(coordenadas)==3:
                coordenadas_mod=[c1,coordenadas[0],coordenadas[1],coordenadas[2]]
                coordenadas_ordenadas = ordenar_puntos(coordenadas_mod)
                coordenadas_ordenadas_mod = mover_punto_arbitrario(coordenadas_ordenadas,c1)
                c1  = coordenadas_ordenadas_mod[0]
                c2  = coordenadas_ordenadas_mod[1]
                c3  = coordenadas_ordenadas_mod[2]
                c4  = coordenadas_ordenadas_mod[3]
                  
            else:
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
        else:
            cv2.imshow("Realidad Virtual", frame)

        # SI SE PRESIONA 'SPACE', ROMPER LOOP. ira a siguiente tornillo
        k = cv2.waitKey(1)
        if k == 32:
            break
        if k == 27:
            break
    
    if k == 27:
        break
    if len(v_estado) == tornillo_a_ajustar:
        flag_mod_torqueado = 2
    else:
        flag_mod_torqueado = 1
# SI SE PRESIONA 'ESC', ROMPER LOOP
    

# LIBERAR CAMARA
cap.release()

# CERRAR PESTAÑAS
cv2.destroyAllWindows()

# cv2.imshow('Imagen Negra', im_silu_mod)
# cv2.waitKey(0)
# cv2.destroyAllWindows()