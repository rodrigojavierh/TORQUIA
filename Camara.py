# Importamos librerias
import cv2
import numpy as np
# Creamos la video captura
cap = cv2.VideoCapture(0) #cambiar a 1 en laptop
a,b=1280,720
cap.set(3,a)
cap.set(4,b)

while True:
    ret, frame = cap.read()
    #frame= cv2.imread()
    print(ret)
    #cv2.imshow("video captura", frame)

    c1 = (a / 4 , b /4 )
    c2 = (3*a / 4 , b / 4)
    c3 = (3*a / 4 , 3*b / 4)
    c4 = (a / 4 , 3*b / 4)
    puntos_ref = np.array([c1, c2, c3, c4])

    copy = frame

    imagen = cv2.imread("ID001Seccion1Vista1.png")
    tamaño = imagen.shape
    puntos_imagen = np.array([
        [0, 0],
        [(tamaño[1] - 1), 0],
        [(tamaño[1] - 1), (tamaño[0] - 1)],
        [0, (tamaño[0] - 1)]
    ], dtype=float)



    h, estado = cv2.findHomography(puntos_imagen, puntos_ref)
    perspectiva = cv2.warpPerspective(imagen, h, (copy.shape[1], copy.shape[0]))
    #cv2.fillConvexPoly(copy, puntos_ref.astype(int), 0, 16)
    copy = cv2.addWeighted(src1=copy,alpha=1,src2=perspectiva, beta=0.55, gamma=0)
    cv2.imshow("Realidad Virtual", copy)

    t=cv2.waitKey(1)
    if t == 27:
        break

cap.release()

cv2.destroyAllWindows()