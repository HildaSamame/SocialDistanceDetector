
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

def import_dataset(filename, separator):
    """
    Objetivo: guardar los datos el archivo en un dataframe. 

    Parámetros:
        filename: nombre del archivo
        separator: tipo de separador utilizado
        
    Salida:
        Retorna el dataframe            
    """
    data = pd.read_csv(filename, sep=separator, header=None)
    data.columns = ["numPersona", "numFrame", "headValid", "bodyValid",
                "headLeft","headTop","headRight","headBottom",
                "bodyLeft","bodyTop","bodyRight","bodyBottom"]
    df = pd.DataFrame(data)
    
    return df

def resize_dataframe(df, factor):
    """
    Objetivo: escalar los valores de los bounding boxes. 

    Parámetros:
        df: dataframe con los valores de los bounding boxes
        factor: escala utilizada. Por ejemplo, si es 2, se escalará a la mitad.
        
    Salida:
        Retorna el dataframe            
    """    
    df['bodyLeft'] = df['bodyLeft']//factor
    df['bodyTop'] = df['bodyTop']//factor
    df['bodyRight'] = df['bodyRight']//factor
    df['bodyBottom'] = df['bodyBottom']//factor
    
    return df


def minimum_distance_pixels(min_distance):
    """
    Objetivo: transformar el valor de la mínima distancia en metros a píxels. 

    Parámetros:
        min_distance: valor de la mínima distancia que debe cumplirse en metros.
        
    Salida:
        Retorna el valor mínimo a cumplir en pixels         
    """    
    x = 49.5 * min_distance / 5.51
    return x
    
    
def eye_bird_view_matrix(filename):
    """
    Objetivo: cargar en una variable la matriz de homografía. 

    Parámetros:
        filename: archivo con los valores de la matriz      
        
    Salida:
        Retorna la matriz         
    """    
    return np.loadtxt(open(filename,"rb"),delimiter=",",skiprows=0)


def calculate_centroid(px_1, py_1, px_2, py_2):
    """
    Objetivo: calcular el centroide de los bounding boxes.

    Parámetros:
        px_1: abscisa del punto 1
        py_1: ordenada del punto 1
        px_2: abscisa del punto 2
        py_2: ordenada del punto 2
        
    Salida:
        Retorna el frame con borde y título            
    """
    cx= int((px_1 + px_2)/2)
    cy= int((py_1 + py_2)/2)
    
    return cx, cy

def transformation_centroid(M, cx, cy):
    """
    Objetivo: calcular el centroide de los bounding boxes.

    Parámetros:
        M: matriz de homografía
        cx: abscisa del centroide original
        cy: ordenada del centroide original        
        
    Salida:
        Retorna el centroide transformado por la matriz de homografía. 
    """
    arr = np.array([cx,cy,], np.float32)
    points = arr.reshape(-1,1,2).astype(np.float32)
    transform_centroid = cv2.perspectiveTransform(points, M)

    return transform_centroid      
    

def __euclidean_distance(p0, p1):
    """
    Objetivo: calcular la distancia euclideana entre dos puntos.

    Parámetros:
        p0: coordenadas del primer punto
        p1: coordenadas del segundo punto
        
    Salida:
        Retorna la distancia euclideana.           
    """
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)


def get_max_frame(df):
    """
    Objetivo: obtener el último frame del dataset.

    Parámetros:
        df: dataframe de datos
        
    Salida:
        Retorna el valor máximo de los frames.           
    """
    max_value = int(df['numFrame'].max())
    return max_value
    

def get_lists_transform_centroids(list_transform_centroids, min_distance):
    """
    Objetivo: guardar las listas con los valores correspondientes a los que cumplen el distanciamento y los que no cumplen.

    Parámetros:
        list_transform_centroids: lista con los valores de los centroides después de la homografía.
        min_distance: mínima distancia (en pixels) para comprobar si se está cumpliendo el distanciamento social.
    Salida:
        Retorna la lista de aquellos que cumplen (good_distances) y los que no cumplen (bad_distances).           
    """
    good_distances = []
    bad_distances = []
    bad_distances_0 = []
    bad_distances_1 = []
    
    for i in range(0, len(list_transform_centroids)-1):
        v=1
        for j in range(i+1, len(list_transform_centroids)):            
            distance = __euclidean_distance(list_transform_centroids[i], list_transform_centroids[j])           
            if distance < min_distance:
                bad_distances_0.append(list_transform_centroids[i])
                bad_distances_1.append(list_transform_centroids[j])
                bad_distances.append(list_transform_centroids[i])
                bad_distances.append(list_transform_centroids[j])              
        good_distances = list(set(tuple(row) for row in list_transform_centroids) - set(tuple(row) for row in bad_distances))

    return good_distances, bad_distances, bad_distances_0, bad_distances_1


def filter_df_good_bad(df_frame, good_distances, bad_distances):
    """
    Objetivo: crear dos dataframe diferenciando a los que cumplen y los que NO cumplen la distancia mínima.

    Parámetros:
        df_frame: dataframe con los datos del frame actual.
        good_distances: lista con los centroides y id de persona que cumplen.
        bad_distances: lista con los centroides y id de persona que NO cumplen.
    
    Salida:
        Retorna el dataframe de los que cumplen y de los que NO cumplen.
    """

    good_people = [item[-1] for item in good_distances] 
    bad_people = [item[-1] for item in bad_distances]
    df_aux_good = df_frame[df_frame['numPersona'].isin(good_people)]
    df_aux_bad = df_frame[df_frame['numPersona'].isin(bad_people)]

    return df_aux_good, df_aux_bad
 

def get_infractors(aux_infractors, infractors_list):
    """
    Objetivo: obtener la lista de infractores a través de su id.

    Parámetros:
        aux_infractors: lista auxiliar de infractores de cada frame.
        infractors_list: lista final de los infractores.
    
    Salida:
        Retorna la lista total de los infractores.
    """
    for idPerson in aux_infractors:       
        if idPerson not in infractors_list:
            infractors_list.append(idPerson)
    
    return infractors_list

def append_list_as_row(file_name, list_of_elem):
    """
    Objetivo: añadir líneas a un archivo csv.

    Parámetros:
        file_name: nombre de archivo csv.
        list_of_elem: elementos para añadir.
    
    Salida:
        Actualiza el archivo csv.
    """
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)
        