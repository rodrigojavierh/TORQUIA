#Ubica los tornillos en una vista especifica del motor

import cv2
import pandas as pd
#from BD_reading_writing import Num_Vista
import numpy as np

def obt_tornillo(event, x, y, flags, param):
    global listax, listay, N
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
        N=N+1

#guardar lista de coordenadas en excel
Num_Vista= 2
#Num_Vista=int(input('ingrese el número de vista a realizar'))
print (Num_Vista)

datos = pd.read_excel("BD_Motor001.xlsx", sheet_name="InfoBD")

#localizamos los indices correspondientes a la vista 1, estaran ordenados
indices = datos.loc[datos['ID_Vista'] == Num_Vista].index
cantidad_tornillos = len(indices)

if cantidad_tornillos==0:
    print("no se encontró vista")
else:
    datosVista = datos[datos["ID_Vista"] == Num_Vista]
    listaX_excel = datosVista['Ub_x'].tolist()
    listaY_excel = datosVista['Ub_y'].tolist()

    # muestra las listas guardadas en el excel
    print("lista de coordenadas de excel")
    print(listaX_excel)
    print(listaY_excel)

    #imagen = cv2.imread("ID001Seccion1Vista1.png")
    imagen = cv2.imread("V02.png")
    listax=[]
    listay=[]


    cv2.namedWindow("Imagen")
    cv2.setMouseCallback("Imagen", obt_tornillo)
    CANT_TORNILLOS= cantidad_tornillos
    N=1
    while N<=CANT_TORNILLOS:
        cv2.imshow("Imagen", imagen)

        k = cv2.waitKey(1) & 0xFF
        if k==27:
            break
    cv2.destroyAllWindows()

    print("lista de coordendas x,y de imagen")
    print (listax)
    print (listay)

    #Crea imagen modificada con las ubicaciones de tornillos,[metodo de verificacion]
    imagen = cv2.imread("V02_SILU.png") #debe ser la silueta
    imagen_modificada= imagen.copy()
    for i in range(0,len(listax)):
        cv2.circle(imagen_modificada, (listax[i],listay[i]),20, (0,0,255),2)
    #Guardar imágen creada en carpeta
    directory=r"G:\PDM\TORQUIA\PrimerProyecto"
    filename = 'V02_SILU_MOD.png'
    cv2.imwrite(filename,imagen_modificada)



    #Modificamos los datos leidos del excel con la lista obtenida de la selección en imagen
    datos.loc[indices, 'Ub_x'] = listax
    datos.loc[indices, 'Ub_y'] = listay

    #Guardar el DF datos en el excel
    datos.to_excel("BD_Motor001.xlsx", sheet_name="InfoBD", index=False)

    print('success')
