# -*- coding: utf-8 -*-
"""
@author: Hilda Ana Samamé Jimenez
@code: 20194015

PROGRAMA PARA CALCULAR LA MATRIZ DE HOMOGRAFIA UTILIZADA EN LA IMPLEMENTACION DEL BIRD EYE VIEW
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

"""
Importar el archivo que corresponde al primer frame de la imagen.
"""
file_frame = 'frame_0.jpg'
img = cv2.cvtColor(cv2.imread(file_frame), cv2.COLOR_BGR2RGB)

dst_size=(550,540)
imgDibujo = img.copy()

"""
Colocar los puntos que corresponden a la imagen fuente y coinciden con 4 puntos en la pista obtenidas con https://yangcha.github.io/iview/iview.html
"""
src = np.float32([[600, 84],[791, 107],[481, 422],[210,326]])

"""
Puntos de destino como una proporción de la imagen de destino
"""
dst=np.float32([(0.61,0.4), (0.7, 0.4), (0.7,0.82), (0.61,0.82)])
dst = dst * np.float32(dst_size)

"""
Graficar los puntos src en la imagen
"""
print("\n** Graficando los puntos en el archivo de origen.")
for pt in src:
    cv2.circle(img, tuple(pt.astype(np.int)), 7, (0,0,255), -1)

points = src.reshape((-1,1,2)).astype(np.int32)
cv2.polylines(img, [points], True, (0,255,0), thickness=2)

plt.figure(figsize=(12, 12))
plt.imshow(img)
plt.show()

"""
Matriz de homografía
"""
print("\n** Calculando la matriz de homografía.")
M = cv2.getPerspectiveTransform(src, dst)
print(M)
"""
Transformar la imagen fuente con la matriz de homografia M, guardar en el archivo warp.jpg
"""
print("\n** Transformando la imagen fuente con la matriz M.")
result = cv2.warpPerspective(imgDibujo, M, dst_size)
cv2.imwrite('warp.jpg',result)

"""
Plotear la imagen resultante
"""
print("\n** Ploteando la imagen resultante.")
plt.figure(figsize=(12, 12))
plt.imshow(result)
plt.xticks(np.arange(0, result.shape[1], step=20))
plt.yticks(np.arange(0, result.shape[0], step=20))
plt.grid(True, color='g', linestyle='-', linewidth=0.9)
plt.show()

"""
Guardar la matriz de homografia en un archivo TXT que será utilizado en el programa principal.
"""
print("\n** Guardando la matriz de homografia en un archivo txt.")
np.savetxt('matrix.txt', M, delimiter = ',')  
my_matrix = np.loadtxt(open("matrix.txt","rb"),delimiter=",",skiprows=0)

"""
Calcular la distancia entre dos puntos de la pista.
"""
print("\n** Calculando la distancia en pixels del ancho de la pista, esto corresponde a 5.51 metros, obtenidos con anterioridad.")
difference = math.sqrt((dst[0][0] - dst[1][0])**2 + (dst[0][1] - dst[1][1])**2)
print(">>>>>>> Ancho de la pista: " + str(difference)+ " pixels.")


"""
Metros a pixels para calcular el distanciamiento mínimo
"""
print("\n** Convirtiendo metros a pixels, por ejemplo, un valor de 10 metros corresponde a:")
minimum_distance_meters = 10
x = difference * minimum_distance_meters / 5.51
print (">>>>>>>" + str(minimum_distance_meters) + " metros corresponde a " + str(round(x,2)) + " pixels.")




