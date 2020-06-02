
# -*- coding: utf-8 -*-
"""
@author: Hilda Ana Samamé Jimenez
@code: 20194015
"""
import cv2
import numpy as np
import pandas as pd
import math
from csv import writer



def create_header_title(frame, title, color_header, color_border, logo):
    """
    Objetivo: colocar el header y título al frame. 

    Parámetros:
        frame: frame a colocar el marco
        title: título para el frame
        color_header: color de la cabecera en formato RGB
        color_border: color del marco en formato RGB
        
    Salida:
        Retorna el frame con borde y título            
    """
    
    font = cv2.FONT_HERSHEY_DUPLEX
    frame = cv2.copyMakeBorder(frame, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=color_border)
    
    header = np.zeros((80, frame.shape[1], 3), np.uint8)
    header[:] = color_header
    
    if(logo):
        #cv2.resize(image, (0,0), fx=0.5, fy=0.5) 
        s_img = cv2.resize(cv2.imread("pucp.jpg"), (0,0), fx=0.2, fy=0.2) 
        l_img = header
        x_offset= 800
        y_offset= 20
        l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
        header = l_img    
    
    #Concatenar verticalmente el header con el frame
    vcat = cv2.vconcat((header, frame))
   
    cv2.putText(vcat, title, (20,50), font, 1, (0,0,0), 2, 0)
    
    return vcat


def create_footer(frame, color):
    """
    Objetivo: colocar el footer frame. 

    Parámetros:
        frame: frame a colocar el footer
        color: color del footer en formato RGB
        
    Salida:
        Retorna el frame con footer           
    """
    
    font = cv2.FONT_HERSHEY_SIMPLEX

    footer = np.zeros((30, frame.shape[1], 3), np.uint8)
    footer[:] = color
   
    cv2.putText(footer, "CURSO DE COMPUTACION GRAFICA // REALIZADO POR: HILDA SAMAME JIMENEZ ** CODIGO: 20194015", (15,20), font, 0.4, (0,0,0), 1, 0)
    
    final = cv2.vconcat((frame, footer))
    return final
	
def map_good_distances(original, result, good_distances, df_aux_good, color, radius, border_rectangle):
    """
    Objetivo: mapear en el video original y el Bird's Eye View a los que cumplen la distancia mínima.

    Parámetros:
        original: frame sobre el cual se colocará los rectángulos.
        result: frame del bird eye view sobre el cual se colocará los puntos.
        good_distances: lista con los centroides a mapear
        df_aux_good: dataframe con los datos de las personas que sí cumplen
        color: color de los círculos
        radius: radio de los círculos
        border_rectangle: grosor del rectángulo de los boxes.
    """
    
    for index, row in df_aux_good.iterrows():
        x_point1 = int(row['bodyLeft'])
        y_point1 = int(row['bodyTop'])
        x_point2 = int(row['bodyRight'])
        y_point2 = int(row['bodyBottom'])
        cx = int(row['cx'])
        cy = int(row['cy'])
        
        cv2.circle(original,(cx,cy), 1, color, -1)
        cv2.rectangle(original,(x_point1,y_point1),(x_point2,y_point2), color, border_rectangle)
        cv2.putText(original,"Id "+ str(int(row['numPersona'])), (x_point1, y_point1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
       
        
    for f in good_distances:
        cv2.circle(result, tuple(f[:2]), radius, color, -1)

def map_bad_distances(original, result, bad_distances_0, bad_distances_1, df_aux_bad, drawLine, color, radius_circle, border_rectangle):
    """
    Objetivo: mapear en el video original y el Bird's Eye View a los que  NO cumplen la distancia mínima.

    Parámetros:
        original: frame sobre el cual se colocará los rectángulos.
        result: frame del bird eye view sobre el cual se colocará los puntos.
        bad_distances: lista con los centroides a mapear
        df_aux_bad: dataframe con los datos de las personas que NO cumplen
        color: color de los círculos
        radius: radio de los círculos
        border_rectangle: grosor del rectángulo de los boxes.
    """
    for index, row in df_aux_bad.iterrows():
       x_point1 = int(row['bodyLeft'])
       y_point1 = int(row['bodyTop'])
       x_point2 = int(row['bodyRight'])
       y_point2 = int(row['bodyBottom'])       
       
       cx = int(row['cx'])
       cy = int(row['cy'])
       
       cv2.circle(original,(cx,cy), 1, color, -1)
       cv2.rectangle(original,(x_point1,y_point1),(x_point2,y_point2), color, border_rectangle)
       cv2.putText(original,"Id "+ str(int(row['numPersona'])), (x_point1, y_point1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
       
    #Uno a unno (de cada lista) se dibuja el centroide y la línea que los une
    for f, b in zip(bad_distances_0, bad_distances_1):
        cv2.circle(result, tuple(f[:2]), radius_circle, color, -1)
        cv2.circle(result, tuple(b[:2]), radius_circle, color, -1)
        index_i = f[-1]
        index_j = b[-1]
        
        cx_1 = int(df_aux_bad.loc[df_aux_bad['numPersona'] == index_i, 'cx'])
        cy_1 = int(df_aux_bad.loc[df_aux_bad['numPersona'] == index_i, 'cy'])
        
        cx_2 = int(df_aux_bad.loc[df_aux_bad['numPersona'] == index_j, 'cx'])
        cy_2 = int(df_aux_bad.loc[df_aux_bad['numPersona'] == index_j, 'cy'])
        
        if(drawLine):
            cv2.line(result,tuple(f[:2]) , tuple(b[:2]), color, 2) 
            cv2.line(original,(cx_1,cy_1) , (cx_2,cy_2), color, 2) 



def print_text(frame, text, x, y, font_scale, color, thickness):
    
    """
    Objetivo: añadir texto en el frame.

    Parámetros:
        frame: frame sobre el cual se colocará el texto
        text: texto a colocar
        x, y: posición del texto
        font_scale: tamaño del texto
        color: color del texto
        thickness: grosor de la letra       
    
    """
    cv2.putText(frame, text, (x,y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)



def save_video(out, frame, filename):
    """
    Objetivo: añadir texto en el frame.

    Parámetros:
        frame: frame a guardar
        filename: nombre de archivo de vídeo de salida
    
    """
    width, height, _ = frame.shape
    if out is None:
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(filename, fourcc, 25, (int(height), int(width)))
    out.write(frame)
    
    return out