#este programa nos permitira encontrar el centroide de un marcador circular de un color determinado
import cv2
import numpy as np
def dibujar(mask,color):
    contornos,_= cv2.findContours(maskGreen, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(frame,contornos, -1, (255,0,0), 3)
    for c in contornos:
        area=cv2.contourArea(c)
        print(area)
        if area>40:
            M=cv2.moments(c)
            if (M["m00"]==0): M["m00"]=1
            x=int(M["m10"]/M["m00"])
            y=int(M['m01']/M["m00"])
            nuevoContorno=cv2.convexHull(c)
            cv2.circle(frame,(x,y),7,(0,255,0),-1)
            cv2.putText(frame,'{},{}'.format(x,y),(x+10,y),font,0.75,(0,0,255),1,cv2.LINE_AA)
            cv2.drawContours(frame,[nuevoContorno], 0, color, 3)
        

cap=cv2.VideoCapture(0)

GreenBajo=np.array([30,60,200],np.uint8)
GreenAlto=np.array([70,255,255], np.uint8)

BlueBajo=np.array([80,100,20],np.uint8)
BlueAlto=np.array([140,255,255], np.uint8)

font=cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret,frame=cap.read()
    if ret==True:
        frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV )
        maskGreen=cv2.inRange(frameHSV,GreenBajo,GreenAlto)
        maskBlue=cv2.inRange(frameHSV,BlueBajo,BlueAlto)
        
        dibujar(maskGreen,(255,0,0))
        #dibujar(maskBlue,(0,0,255))
        #maskBlue=cv2.inRange(frameHSV,BlueBajo,BlueAlto)
        #maskTot=cv2.add(maskGreen,maskBlue)
        #maskRes=cv2.bitwise_and(frame,frame, mask= maskGreen)
        #cv2.imshow('maskRes', maskRes)
        #cv2.imshow('maskTot', maskGreen)
        cv2.imshow('frame',frame)
    k = cv2.waitKey(1)
    if k == 27:
        break
        
        
cap.release()
cv2.destroyAllWindows()