# leer datos de excel y graficar la imagen a superponer

#IMPORTAR LIBRERIAS
import cv2
import numpy as np
import pandas as pd

#from Main_0_2 import cant_tornillos

#LEER IMAGEN DE SILUETA - Vista 01 - "V01"
#im_silueta = cv2.imread("V01_SILU.png")
    # Se podría mejorar cuando se obtiene la info del excel
    # con respecto de la vista en la que se está trabajando


tornillo_a_ajustar=1 #info que se lee inicialmente del excel
v_estado = [1,0,0,0,0,0,0,0] #2:verde 1:azul 0:rojo #info que se lee inicialmente del excel

# LEER EXCEL CON DATOS DE COORDENADAS DE TORNILLOS (X,Y,COLOR,NUM_VISTA)
datos = pd.read_excel("BD_Motor001.xlsx", sheet_name="InfoBD")
Num_Vista=3
datosVista = datos[datos["ID_Vista"]==Num_Vista]
listaX= datosVista['Ub_x'].tolist()
listaY= datosVista['Ub_y'].tolist()
cant_tornillos = len(listaX)

#muestra las listas guardadas en el excel
print(listaX)
print(listaY)

#emular obtencion de datos de UbiTornillos_0_1.py
listaX_Mod=[76, 246, 411, 578, 91, 250, 418, 583]
listaY_Mod=[65, 65, 62, 63, 258, 230, 225, 225]

#modificamos las listas
listaX = listaX_Mod
listaY = listaY_Mod
print(listaX)
print(listaY)

#localizamos los indices correspondientes a la vista 1, estaran ordenados
indices_v01 = datos.loc[datos['ID_Vista'] == Num_Vista].index
if len(indices_v01)==0:
    print("no se encontró vista")
else:
    #Modificamos los datos leidos del excel con la lista obtenida de UbiTornillos_0_1.py
    datos.loc[indices_v01, 'Ub_x'] = listaX_Mod
    datos.loc[indices_v01, 'Ub_y'] = listaY_Mod

#Guardar el DF datos en el excel
datos.to_excel("BD_Motor001.xlsx", sheet_name="InfoBD", index=False)
