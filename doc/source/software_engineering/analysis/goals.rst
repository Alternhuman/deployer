Objetivos
=========

La aplicación debe cumplir los siguientes objetivos a alto nivel:

OBJ-1: Despliegue de ejecutables
--------------------------------

- **Versión**: 2
- **Autores**: Diego Martín
- **Fuentes**: Diseño preliminar de la aplicación
- **Descripción**: El *software* deberá realizar operaciones de despliegue sobre un conjunto de nodos especificado por el usuario, con una serie de parámetros que modificarán los efectos de dicha acción. No deberá existir un conjunto limitado de software compatible, sino que la herramienta deberá ser de carácter general, admitiendo en casos particulares ser extendida para dar mejor soporte a un propósito particular, atendiendo a las demandas del público objetivo.
- **Importancia**: Muy alta
- **Urgencia**: Elevada
- **Estado**: Completo
- **Estabilidad**: Estable
- **Comentarios**: El sistema debe soportar el despliegue de ejecutables y ficheros de configuración de forma indistinta.


OBJ-2: Monitorización del sistema
---------------------------------

- **Versión**: 1.5
- **Autores**: Diego Martín y Rodrigo Santamaría
- **Fuentes**: Diseño preliminar de la aplicación y reuniones de equipo
- **Descripción**: A través de la herramienta, los usuarios podrán consultar diferentes valores sobre el estado de los diferentes nodos que conforman el sistema distribuido en directo. Los valores se mostrarán a través de herramientas de visualización.
- **Importancia**: Muy alta
- **Urgencia**: Elevada
- **Estado**: Completo
- **Estabilidad**: Estable
- **Comentarios**: La monitorización deberá realizarse de forma asíncrona y evitando "cuellos de botella", debido a la gran cantidad de información transmitida en periódicamente con intervalos entre cada operación envío muy pequeños.


OBJ-3: Operaciones de depuración y control
-----------------------------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Entrevistas
- **Descripción**: A través de diferentes interfaces los usuarios del sistema pueden evaluar el comportamiento de un programa desplegado.
- **Importancia**: Alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable

OBJ-4: Órdenes
-------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Diseño preliminar de la aplicación
- **Descripción**: Junto a una operación de despliegue o de forma independiente, los usuarios pueden realizar diferentes acciones a través de llamadas al sistema mediante la misma interfaz.
- **Importancia**: Media
- **Urgencia**: Media
- **Estado**: Completo
- **Estabilidad**: Estable

.. 
    - **Versión**
    - **Autores**
    - **Fuentes**
    - **Descripción**
    - **Subobjetivos**
    - **Importancia**
    - **Urgencia**
    - **Estado**
    - **Estabilidad**
    - **Comentarios**