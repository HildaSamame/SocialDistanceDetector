# -*- coding: utf-8 -*-
"""
Programa Principal del Distance Social Grapher

@author: Hilda Ana Samamé Jimenez
@code: 20194015
"""
from imutils.video import FPS
import numpy as np
import imutils
import cv2
import os
import pandas as pd
from utils import functions  as ut
from utils import view  as vi
import os
import ctypes  # An included library with Python install.   


"""
Ruta y nombre de los archivos utilizados en el programa
    DATA_FILE: archivo que tiene la información de los frame y bounding-boxes
    VIDEO_FILE: archivo fuente de video
    MATRIX_FILE: archivo con la matriz de homografía previamente calculada
    CSV_FILE: archivo csv que guarda los datos de los infractores
"""
DATA_FILE   = 'input/TownCentre-groundtruth.top'
VIDEO_FILE  = 'input/TownCentreXVID.avi'
MATRIX_FILE = 'preprocess/matrix.txt'
CSV_FILE    = 'output/infractors.csv'
OUTPUT_FILE = 'output/resultado.avi'

"""
Variables utilizadas en el programa para el procesamiento y visualización
"""
resize_factor   = 2
num_frame       = 0 #Inicialización del conteo de frames en 0.
green           = [0,255,0]
red             = [0,0,255]
black           = [0,0,0]
white           = [255,255,255]
color_border    = [105,105,105]
color_header    = [255,255,255]
color_footer    = [169,169,169]
main_title      = 'Social Distance Plotter'
eye_title       = 'Birds Eye View'
flag_window     = False

"""
Importar el dataset del archivo DATA_FILE en un dataframe.
Dado que se hará un resize del video a la mitad, de igual forma se escalará los valores de los bounding boxes a la mitad. Es por ello que el RESIZE_FACTOR es 2.
"""
df = ut.import_dataset(DATA_FILE, ',')
df = ut.resize_dataframe(df, resize_factor)


"""
Iniciar la captura del archivo VIDEO_FILE.
"""
cap = cv2.VideoCapture(VIDEO_FILE)
out = None #Variable donde se guardará el video resultante.
fps = FPS().start()

"""
Importar la matriz de homografía.
"""
M = ut.eye_bird_view_matrix(MATRIX_FILE)
infractors_list = []
infractor_count = 0

header_contents = ['Frame','Person_Id','Time']


if os.path.exists(CSV_FILE):
  os.remove(CSV_FILE)

ut.append_list_as_row(CSV_FILE, header_contents)


while(True):
    """
    Setear la mínima distancia en pixels.
    """
    min_distance = ut.minimum_distance_pixels(2)
    maximum_var     = 50
    
    """
    Realizar resize al video a la mitad (RESIZE_FACTOR).
    """
    grabbed, frame = cap.read()
    frame = imutils.resize(frame, width = int(cap.get(3)/resize_factor))       
    if not grabbed:
        break
    
    """
    Reiniciar la reproducción del video cuando se llega al último frame.
    """
    final_frame = ut.get_max_frame(df)  #Cantidad de frames en el dataset de DATA_FILE.
    if num_frame == final_frame:
        num_frame = 0 
        cap = cv2.VideoCapture(VIDEO_FILE)
    
    """
    Guardar en df_frame los datos correspondientes al valor de numFrame = num_frame.
    """
    df_frame = df[df['numFrame'] == num_frame]
  
    
    """
    Inicializar las listas que servirán para guardar la información de los que cumplen o no la distancia.
    """
    list_transform_centroids = []
    bad_distances = []
    good_distances = []
    bad_distances_0 = []
    bad_distances_1 = []
    aux_infractors = []
     
    timer = cv2.getTickCount()
    
    
    """
    Iniciar procesamiento de cada frame para obtener los bounding-boxes diferenciados por color y el bird's eye view.
    """
    for index, row in df_frame.iterrows():
        
        numPersona = int(row['numPersona'])
        x_point1 = int(row['bodyLeft'])
        y_point1 = int(row['bodyTop'])
        x_point2 = int(row['bodyRight'])
        y_point2 = int(row['bodyBottom'])
        
        """
        Calcular y guardar en df_frame los valores del centroide calculado.
        """
        cx, cy = ut.calculate_centroid(x_point1, y_point1, x_point2, y_point2)
        df_frame.loc[index, 'cx'] = cx
        df_frame.loc[index, 'cy'] = cy
        
        """
        Calcular y guardar el valor del centroide transformado por la matriz de homografía.
        Guardar en una variable auxiliar el centroide transformado y el id de la persona que le corresponde.
        """      
        transform_centroid = ut.transformation_centroid(M, cx, cy)             
        temp_trans_centroid = [int(transform_centroid.item(0)), int(transform_centroid.item(1)), numPersona]
        list_transform_centroids.append(temp_trans_centroid)
        
        
    """    
    Iniciar cálculo de las distancias entre los centroides transformados y guardarlos en sus respectivas listas.
    """ 
    good_distances, bad_distances, bad_distances_0, bad_distances_1 = ut.get_lists_transform_centroids(list_transform_centroids, min_distance)
    
    """    
    Filtrar en dos dataframes los datos de las personas que cumplen y que no cumplen el distancimiento social.
    """ 
   
    df_aux_good, df_aux_bad = ut.filter_df_good_bad(df_frame, good_distances, bad_distances)
        
    """"""""""""
    """ Dibujo de los Bounding Boxes y Creación del frame correspondiente al Bird's Eye View """
    """"""""""""
    
    """
    Transformar el frame original con la matriz de homografía para obtener la perspectiva de top-down view y colorear el frame resultante de color negro (cada pixel es seteado a negro).
    """
    result = cv2.warpPerspective(frame, M, (550,540))  
    result[:] = black   
    
    """
    Dibujar los círculos en el Eye Bird View y los rectángulos en el video original de las personas que cumplen el distanciamiento social.
    """
    vi.map_good_distances(frame, result, good_distances, df_aux_good, green, 5, 2)  
   
    """
    Dibujar los círculos en el Eye Bird View y los rectángulos en el video original de las personas que NO cumplen el distanciamiento social.
    """
    vi.map_bad_distances(frame, result, bad_distances_0, bad_distances_1, df_aux_bad, True, red, 5, 2)
    
    
    """
    Obtener el listado de los infractores, el cual servirá para conocer la cantidad de personas que no cumplen y mostrar dicho número
    """
    temp = infractors_list
    aux_infractors = df_aux_bad["numPersona"].tolist()
    infractors_list = ut.get_infractors(aux_infractors, temp)
    
    y=0
    x=180
    h=540
    w=430
    result = result[y:y+h, x:x+w]
    
    """
    Obtener el minuto y segundo del video
    """    
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = num_frame/fps    
    minutes = int(duration/60)
    seconds = duration%60
    #print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))
    
    df_temp = df[df['numFrame']<= num_frame]
    total_people = df_temp['numPersona'].unique().shape[0]
    
    percentage_infractor = len(infractors_list)/total_people*100
    percentage_infractor = round(percentage_infractor,2)
    
    if percentage_infractor > maximum_var and not flag_window:
        ctypes.windll.user32.MessageBoxW(0, "Se ha superado el umbral de incumplimiento del distanciamiento social.", "ALERTA!!", 1)
        flag_window = True
    
    """
    Agregar una etiqueta que indique el número de frame procesado, el tiempo y la cantidad de personas infractoras.
    """
    vi.print_text(frame, "Frame: " + str(num_frame), 10, 20, 0.6, black, 1)
    vi.print_text(frame, "Tiempo: " + str(minutes) + ':' + str(seconds), 10, 40, 0.6, black, 1)
    vi.print_text(result, "Frame: " + str(num_frame), 10, 20, 0.5, white, 1)
    vi.print_text(result, "Total de personas transitando: " + str(total_people), 10, 40, 0.5, white, 1)
    vi.print_text(result, "Total de personas infractoras: " + str(len(infractors_list)), 10, 60, 0.5, white, 1)
    vi.print_text(result, "Porcentaje de infraccion: " + str(percentage_infractor)+ " %", 10, 80, 0.5, white, 1)
  
    """
    Añadir un borde y título al video original y a la vista de ave, finalmente concatenar y mostrar.
    """
    vcat = vi.create_header_title(frame, main_title, color_header, color_border, True)
    vcat2 = vi.create_header_title(result, eye_title, color_header, color_border, False)
    f_frame = cv2.hconcat((vcat, vcat2))
    final_frame = vi.create_footer(f_frame, color_footer)
    cv2.imshow('Social Distance Plotter',final_frame)
    
    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    
    
    
    
    for aux_inf in aux_infractors:
        content = [num_frame, aux_inf, str(minutes) + ':' + str(seconds)]
        ut.append_list_as_row(CSV_FILE, content)    
    
    
    """
    Guardar video en formato AVI con los resultados
    """
    out = vi.save_video(out, final_frame, OUTPUT_FILE)
    
    """
    Aumentar el contador de frame
    """
    num_frame = num_frame + 1 
    
    if cv2.waitKey(1) & 0xFF == ord('q') :
        break

# Cuando todo esté listo, liberar la variable cap
cap.release()
out.release()
cv2.destroyAllWindows()