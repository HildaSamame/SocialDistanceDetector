# Social Distance Detector

Proyecto de mitad de semestre del curso de _"Computación Gráfica"_ de la Maestría en Informática con mención en Ciencias de la Computación de la Pontificia Universidad Católica del Perú

## Propósito 💡

El presente proyecto tiene como propósito detectar en un video a aquellas personas que cumplen o no las normativas de distanciamento social que se rige por el COVID-19, partiendo de los datos de detección de personas que ha sido procesado anteriormente.

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


<img src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/distancestreet.JPG" data-canonical-src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/distancestreet.JPG" width="400" />

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
  * ___preprocess/frame_0.jpg___: imagen del primer frame del vídeo, utilizado para calcular la transformación del Bird's Eye View.

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
<img src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/warp_01.png" data-canonical-src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/warp_01.png" width="850"  />



<img src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/warp_02.png" data-canonical-src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/warp_02.png" width="480" />

Verificar que se haya creado el archivo __matrix.txt__.

### Procesamiento 🔩
Ejecutar el programa __main_program.py__ a través de la consola. _NOTA: Primero ir al directorio donde está el archivo_. Por ejemplo, en el shell de Anaconda, colocar:

```
python main_program.py
```

Se visualiza el resultado: 


<img src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/result_01.JPG" data-canonical-src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/result_01.JPG" width="1000" />


Cuando sobrepasa el umbral, aparece el mensaje de alerta.


<img src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/result_02.JPG" data-canonical-src="https://github.com/HildaSamame/SocialDistanceGraph/blob/master/images_readme/result_02.JPG" width="1000" />


El vídeo de salida se genera en la carpeta __output__, en el siguiente link hay un vídeo de duración de 2 minutos. (https://youtu.be/io2HgVkbZf4).

### Seteo de variables 🛠️
En el programa __main_program.py__ se setean las variables que serán utilizadas a lo largo del procesamiento del vídeo.
 * Setear la distancia mínima a considerar en la función de cambio de metros a píxels.
 * Setear el máximo porcentaje permitido para el incumplimiento del distanciamiento social.
 * Setear los nombres de los archivos de entrada y salida.
 * Setear los títulos de la visualización.

_Observación:_ Para el presente proyecto, se realizó un resize del vídeo a la mitad, desde el cálculo de la matriz de homografía hasta el procesamiento, es por ello que una de las variables se llama __resize_factor__ y fue seteada con un valor de 2, que representa la mitad para nuestro programa.


### Explicación de la metodología 🛠️

 
1. Calcular la __matriz de homografía__ de la transformación de la imagen original al bird's eye view. 
2. Iniciar la lectura del víde, __frame por frame__ del vídeo.
3. Hallar el __centroide__ del bounding-box de cada persona existente en el frame.
4. Transformar cada __centroide__ usando la __matriz de homografía__.
5. Calcular la __distancia euclideana__ entre todos los centroides, aquellos que superen la distancia mínima son guardados como _bad_distances_ y los que cumplen, como _good_distances_.
6. Los que correspondan a los que cumplen el distanciamiento, se les asigna el color verde para el bounding-box y para el punto en el bird eye view; los que no cumplen, se le asigna el color rojo.
7. Calcular las __estadísticas__: total de personas que no cumplen el distancimiento social, porcentaje de no cumplimiento, total de personas. Utilizando el porcentaje de incumplimiento, mostrar un pop-up cuando se supere el umbral.
8. Crear la __vista__ con ambos gráficos (bounding-boxes y bird's eye view).
9. Mostrar los __resultados__.
10. Guardar el frame resultante en el __vídeo de salida__ y los datos de los infractores en el __csv__.
11. Repetir para todos los frames que se encuentran en el archivo de input.

## Autores ✒️

Los colaboradores del presente proyecto son:

* **Hilda Samamé Jimenez** - [hildasamame](https://github.com/HildaSamame) ☕

## Licencia 📄

 * Este proyecto está bajo... _la Licencia 📢 IT'S FREE ;)_
 * Este proyecto está bajo la Licencia GNU General Public License v3.0 - mira el archivo LICENSE.md para más detalles.


---
⌨️ con ❤️ por Hilda Samamé 😊
