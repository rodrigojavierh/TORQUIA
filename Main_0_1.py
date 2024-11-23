# Programa:
# - Detecta Marcador Aruco y superpone una imagen entregada
import cv2
import numpy as np

parametros = cv2.aruco.DetectorParameters()

diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)

cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    esquinas, ids, candidatos_malos = cv2.aruco.detectMarkers(gray, diccionario, parameters=parametros)

    if np.all(ids != None): #si existe marcadores aruco
        aruco = cv2.aruco.drawDetectedMarkers(frame, esquinas)

        sc = 10 #Escala que se visualizara al superponer un imagen
        c1= (esquinas[0][0][0][0], esquinas[0][0][0][1])
        c2 = (sc*esquinas[0][0][1][0]-(sc-1)*esquinas[0][0][0][0],sc*esquinas[0][0][1][1]-(sc-1)*esquinas[0][0][0][1])
        c3 = (sc*esquinas[0][0][2][0]-(sc-1)*esquinas[0][0][0][0],sc*esquinas[0][0][2][1]-(sc-1)*esquinas[0][0][0][1])
        c4 = (sc*esquinas[0][0][3][0]-(sc-1)*esquinas[0][0][0][0],sc*esquinas[0][0][3][1]-(sc-1)*esquinas[0][0][0][1])

        copy = frame
        #Leer imagen a superponer

        #imagen =cv2.imread("ID001Seccion1Vista1T.png")
        imagen = cv2.imread("SELLO_DE_CULATA_SILU_MOD.png")
        tamanho = imagen.shape
        #print(tamaño)
        puntosRef_aruco = np.array([c1,c2,c3,c4])
        puntos_imagen = np.array([
            [0,0],
            [(tamanho[1] - 1), 0],
            [(tamanho[1] - 1), (tamanho[0] - 1)],
            [0, (tamanho[0]-1)]
        ],dtype = float)

        #Superponer
        h, estado = cv2.findHomography(puntos_imagen, puntosRef_aruco)
        #Transformacion de perspectiva
        perspectiva = cv2.warpPerspective(imagen, h, (copy.shape[1], copy.shape[0]))
        #cv2.fillConvexPoly(copy, puntos_aruco.astype(int), 0, 16)
        copy = cv2.addWeighted(src1=copy, alpha=1, src2=perspectiva, beta=1, gamma=0)
        #copy = copy + perspectiva
        cv2.imshow("Realidad Virtual",copy)

    else:
        cv2.imshow("Realidad Virtual", frame)


    k= cv2.waitKey(1)
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()