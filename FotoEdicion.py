# Importamos librerias
import cv2
import numpy as np

imagen = cv2.imread("ID001Seccion1Vista1T.png")
print(imagen[:,400])

imagen2 =cv2.imread("ID001Seccion1Vista1.png")
print(imagen2.shape)
while True:
    cv2.imshow("Realidad Virtual", imagen2)
    t=cv2.waitKey(1)
    if t == 27:
        break

cv2.destroyAllWindows()