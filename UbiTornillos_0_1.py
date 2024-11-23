#Ubica los tornillos en una vista especifica del motor

import cv2
#import numpy as np

def obt_tornillo(event, x, y, flags, param):
    global listax, listay
    if event == 1:
        print('-------------------')
        print('event=', event)
        print('x=',x)
        print('y=',y)
        print('flags=',flags)
        print('parametro=',param )
        listax.append(x)
        listay.append(y)
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(imagen, (x,y),20, (0,0,255),2)

#imagen = cv2.imread("ID001Seccion1Vista1.png")
imagen = cv2.imread("V01.png")
listax=[]
listay=[]
cv2.namedWindow("Imagen")
cv2.setMouseCallback("Imagen", obt_tornillo)

while True:
    cv2.imshow("Imagen", imagen)

    k = cv2.waitKey(1) & 0xFF
    if k==27:
        break
cv2.destroyAllWindows()
print (listax)
print (listay)

#Crea imagen modificada con las ubicaciones de tornillos
imagen = cv2.imread("V01_SILU.png") #debe ser la silueta
imagen_modificada= imagen.copy()
for i in range(0,len(listax)):
    cv2.circle(imagen_modificada, (listax[i],listay[i]),20, (0,0,255),2)

directory=r"G:\PDM\TORQUIA\PrimerProyecto"
filename = 'V01_SILU_MOD.png'
cv2.imwrite(filename,imagen_modificada)
print('success')
