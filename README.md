# Social Distance Detector

Proyecto de mitad de semestre del curso de _"Computación Gráfica"_ de la Maestría en Informática con mención en Ciencias de la Computación de la Pontificia Universidad Católica del Perú

## Propósito 💡

El presente proyecto tiene como propósito detectar en un video a aquellas personas que cumplen o no las normativas de distanciamento social que se rige por el COVID-19, partiendo de los datos detección de personas que ha sido procesado anteriormente.

## Base del proyecto 📓

Para el desarrollo del proyecto se tiene en cuenta la siguiente información:
* Vídeo (https://www.robots.ox.ac.uk/ActiveVision/Research/Projects/2009bbenfold_headpose/Datasets/TownCentreXVID.avi)
* Datos relacionados al bounding box de cada persona en cada frame del video (https://www.robots.ox.ac.uk/ActiveVision/Research/Projects/2009bbenfold_headpose/Datasets/TownCentre-groundtruth.top)
Estos datos están en formato CSV, donde cada línea contiene la siguiente información:
  * numPersona: es un único identificador para cada persona
  * numFrame: es el número de frame (contado desde cero)
  * headValid,bodyValid: indica si los bounding boxes de la cabeza y el cuerpo son válidos
  * headLeft,headTop,headRight,headBottom: es el bounding box de la cabeza
  * bodyLeft,bofyTop,bodyRight,bodyBottom: es el bounding box del cuerpo

_Teniendo esto en cuenta... ¡sigamos!._

### Construido con 🛠️

El presente trabajo fue implementado utilizando:
* Python - 3.7.6
* OpenCV – 4.2.0
* Spyder - 4.0.1 (IDE de desarrollo)

### Consideraciones Previas 🔧
La calle del vídeo a analizar corresponde a Cornmarket and Market St. in Oxford, England. (https://megapixels.cc/oxford_town_centre/). 


<img src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/cornmaker.JPG" data-canonical-src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/cornmaker.JPG" width="350" height="300" />

A través de Google Earth, se obtuvo la distancia de la pista de dicha calle, que corresponde a 5.51 m. _Esto nos ayudará para determinar la distancia mínima a cumplir!_.


<img src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/distancestreet.JPG" data-canonical-src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/distancestreet.JPG" width="400" height="400" />

### Explicación de la metodología 🛠️

1. 
2. 
3.
4.


## Ejecutando las pruebas ⚙️

### Archivos necesarios
* 📋 __INPUT__:
  * En la carpeta ___input___ colocar los archivos de entrada que corresponde al vídeo TownCentreXVID.avi y al csv TownCentre-groundtruth.top con los datos.
  
* 📋 __UTILITARIOS__:
  * ___utils/functions.py___: archivo .py donde están las funciones utilizadas en el programa principal, estas funciones abarcan el procesamiento del vídeo para obtener quiénes cumplen o no cumplen el distanciamiento social. 
  * ___utils/view.py___: archivo .py donde están las funciones que permiten implementar la generación de la vista.

* 📋 __PRE PROCESAMIENTO__:
  * ___preprocess/preprocessing.py___: archivo .py que permite obtener la matriz de homografía en un archivo txt, para ser utilizada en el programa principal. Además, se realiza el cálculo del ancho de la pista en píxels.
  * ___preprocess/matrix.txt___: archivo txt donde se guarda la matriz de homografía para luego ser utilizada en el programa principal
  * ___preprocess/frame_0.jpg__: imagen del primer frame del vídeo, utilizado para calcular la transformación del Bird's Eye View.

* 📋 __PROGRAMA PRINCIPAL__:
  * ___main_program.py___: archivo .py que ejecuta las funciones de detección de cumplimiento del distanciamiento social, genera una vista del vídeo original con el Bird's Eye View.

* 📋 __ARCHIVOS DE SALIDA__:
  * ___output/resultado.avi___: archivo de vídeo con el procesamiento ejecutado, se muestra los bounding boxes, el eye's bird view y las estadísticas generadas por cada frame.
  * ___output/infractors.csv___: archivo csv que contiene los ids de las personas que no cumplieron con el distanciamiento social, incluye el número de frame y el tiempo (minutos y segundos) de detección.

### Pre procesamiento 🔩
Ejecutar el programa __preprocess.py__ a través de la consola. _NOTA: Primero ir al directorio donde está el archivo_. Por ejemplo, en el shell de Anaconda, colocar:
 

```
python preprocess.py
```

Verificar que se haya creado el archivo __matrix.txt__.

### Procesamiento 🔩
Ejecutar el programa __main_program.py__ a través de la consola. _NOTA: Primero ir al directorio donde está el archivo_. Por ejemplo, en el shell de Anaconda, colocar:

```
python main_program.py
```

Se visualiza el resultado: 


<img src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/result_01.JPG" data-canonical-src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/result_01.JPG" width="990" height="540" />


Cuando sobrepasa el umbral, aparece el mensaje de alerta.


<img src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/result_02.JPG" data-canonical-src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/result_02.JPG" width="990" height="540" />


El vídeo de salida se genera en la carpeta __output__, en el siguiente link hay un vídeo de duración de 1 minuto. (https://youtu.be/HrlJvIiEqzg).

## Autores ✒️

Los colaboradores del presente proyecto son:

* **Hilda Samamé Jimenez** - [hildasamame](https://github.com/HildaSamame) ☕

## Licencia 📄

Este proyecto está bajo... _la Licencia 📢 IT'S FREE ;)_



---
⌨️ con ❤️ por Hilda Samamé 😊
