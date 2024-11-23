import cv2
import numpy
from Calibracion import *


parametros = cv2.aruco.DetectorParameters()

diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)

cap = cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4,720)
cont=5

#Calibracion
calibracion = calibracion()
matrix, dist = calibracion.calibracion_cam()
print("Matriz de la camara: ", matrix)
print("Coeficiente de Distorsion: ", dist)

while True:
    ret, frame =cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    esquinas, ids, candidatos_malos = cv2.aruco.detectMarkers(gray, diccionario, parameters=parametros)

    try:

        if np.all(ids != None):

            for i in range(0, len(ids)):

                rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(esquinas[i],0.02, matrix, dist)

                (rvec - tvec).any()

                cv2.aruco.drawDetectedMarkers(frame, esquinas)

                cv2.drawFrameAxes(frame, matrix, dist, rvec, tvec, 0.01)

                c_x = (esquinas[i][0][0][0] + esquinas[i][0][1][0] + esquinas[i][0][2][0] + esquinas[i][0][3][0]) /4

                c_y = (esquinas[i][0][0][1] + esquinas[i][0][1][1] + esquinas[i][0][2][1] + esquinas[i][0][3][1]) /4

                cv2.putText(frame, "id" + str(ids[i]),(int(c_x), int(c_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (50,225,250), 2)

                c1 = (esquinas[0][0][0][0], esquinas[0][0][0][1])
                c2 = (esquinas[0][0][1][0], esquinas[0][0][1][1])
                c3 = (esquinas[0][0][2][0], esquinas[0][0][2][1])
                c4 = (esquinas[0][0][3][0], esquinas[0][0][3][1])
                v1, v2 = c1[0], c1[1]
                v3, v4 = c2[0], c2[1]
                v5, v6 = c3[0], c3[1]
                v7, v8 = c4[0], c4[1]



                #Dibujamos piramide
                #Cara inferior
                cv2.line(frame, (int(v1), int(v2)),(int(v3), int(v4)),(255,0,255),3)
                cv2.line(frame, (int(v5), int(v6)), (int(v7), int(v8)), (255, 0, 255), 3)
                cv2.line(frame, (int(v1), int(v2)), (int(v7), int(v8)), (255, 0, 255), 3)
                cv2.line(frame, (int(v3), int(v4)), (int(v5), int(v6)), (255, 0, 255), 3)
                #Esquinas
                cex1, cey1 = (v1+v5) // 2, (v2+v6) //2
                cex2, cey2 = (v3 + v7) // 2, (v4 + v8) // 2
                cv2.line(frame, (int(v1), int(v2)), (int(cex1), int(cey1 - 200)), (255, 0, 255), 3)
                cv2.line(frame, (int(v5), int(v6)), (int(cex1), int(cey1 - 200)), (255, 0, 255), 3)
                cv2.line(frame, (int(v3), int(v4)), (int(cex1), int(cey2 - 200)), (255, 0, 255), 3)
                cv2.line(frame, (int(v7), int(v8)), (int(cex1), int(cey2 - 200)), (255, 0, 255), 3)

                # Dibujamos Cubo
                # Cara Inferior
                cv2.line(frame, (int(v1), int(v2)), (int(v3), int(v4)), (255, 255, 0), 3)
                cv2.line(frame, (int(v5), int(v6)), (int(v7), int(v8)), (255, 255, 0), 3)
                cv2.line(frame, (int(v1), int(v2)), (int(v7), int(v8)), (255, 255, 0), 3)
                cv2.line(frame, (int(v3), int(v4)), (int(v5), int(v6)), (255, 255, 0), 3)
                # Cara Superior
                cv2.line(frame, (int(v1), int(v2 - 200)), (int(v3), int(v4 - 200)), (255, 255, 0), 3)
                cv2.line(frame, (int(v5), int(v6 - 200)), (int(v7), int(v8 - 200)), (255, 255, 0), 3)
                cv2.line(frame, (int(v1), int(v2 - 200)), (int(v7), int(v8 - 200)), (255, 255, 0), 3)
                cv2.line(frame, (int(v3), int(v4 - 200)), (int(v5), int(v6 - 200)), (255, 255, 0), 3)
                # Caras Laterales
                cv2.line(frame, (int(v1), int(v2 - 200)), (int(v1), int(v2)), (255, 255, 0), 3)
                cv2.line(frame, (int(v3), int(v4 - 200)), (int(v3), int(v4)), (255, 255, 0), 3)
                cv2.line(frame, (int(v5), int(v6 - 200)), (int(v5), int(v6)), (255, 255, 0), 3)
                cv2.line(frame, (int(v7), int(v8 - 200)), (int(v7), int(v8)), (255, 255, 0), 3)

    except:
        if ids is None or len(ids)==0:
            print("***********Marker Detection Failed **********")

    cv2.imshow('Realidad Virtual', frame)
    k= cv2.waitKey(1)

    if k==97:
        print ("Imagen Guardada")
        cv2.imwrite("cali{}.png".format(cont), frame)
        cont = cont + 1

    if k== 27:
        break
cap.release()
cv2.destroyAllWindows()





