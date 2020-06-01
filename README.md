# Social Distance Plotter

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

## Ejecutando las pruebas ⚙️

_Explica como ejecutar las pruebas automatizadas para este sistema_

### Pero antes... necesitamos la matriz de transformación 🔩

_Explica que verifican estas pruebas y por qué_

```
Da un ejemplo
```

### Y las pruebas de estilo de codificación ⌨️

_Explica que verifican estas pruebas y por qué_

```
Da un ejemplo
```

## Despliegue 📦

_Agrega notas adicionales sobre como hacer deploy_

## Construido con 📋

_Menciona las herramientas que utilizaste para crear tu proyecto_

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - El framework web usado
* [Maven](https://maven.apache.org/) - Manejador de dependencias
* [ROME](https://rometools.github.io/rome/) - Usado para generar RSS

## Contribuyendo 🖇️

Por favor lee el [CONTRIBUTING.md](https://gist.github.com/villanuevand/xxxxxx) para detalles de nuestro código de conducta, y el proceso para enviarnos pull requests.

## Wiki 📖

Puedes encontrar mucho más de cómo utilizar este proyecto en nuestra [Wiki](https://github.com/tu/proyecto/wiki)

## Versionado 📌

Usamos [SemVer](http://semver.org/) para el versionado. Para todas las versiones disponibles, mira los [tags en este repositorio](https://github.com/tu/proyecto/tags).

## Autores ✒️

Los colaboradores del presente proyecto son:

* **Hilda Samamé Jimenez** - [hildasamame](https://github.com/HildaSamame)

## Licencia 📄

Este proyecto está bajo... _la Licencia IT'S FREE ;)_

## Expresiones de Gratitud 🎁

* Comenta a otros sobre este proyecto 📢
* Invita una cerveza 🍺 o un café ☕ a alguien del equipo. 
* Da las gracias públicamente 🤓.
* etc.



---
⌨️ con ❤️ por [Villanuevand](https://github.com/Villanuevand) 😊
