Requisitos funcionales
======================

RF-1: Ordenar despliegue
------------------------

- **Versión**: 2
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar del sistema
- **Objetivos asociados**: 1
- **Requisitos asociados**: RF4
- **Descripción**: Diferentes usuarios solicitan al sistema la realización de operaciones de despliegue con una serie de parámetros de configuración.
- **Precondición**: El usuario deberá estar autenticado en el sistema.
- **Secuencia normal**:

    1. El usuario solicita realizar una operación de despliegue.
    2. El sistema muestra la información sobre los diferentes nodos que admiten operaciones de despliegue.
    3. El usuario selecciona los nodos donde desea ubicar los ficheros.
    4. El usuario elige un fichero ejecutable e indica los diferentes parámetros de despliegue.
    5. Para cada uno de los ficheros a desplegar realizará esta acción.
    6. Una vez que termine de añadir ficheros, el despliegue comenzará.
    7. Si se indica un comando en uno o varios de los ficheros, el usuario recibe la salida de estos en la vista dispuesta a tal efecto.  Se ejecuta el caso de uso RF-4
    
- **Poscondición**: El usuario recibe la confirmación de éxito o un mensaje de error en su defecto.
- **Excepciones**:

    + Si el usuario no dispone de los permisos de ejecución o despliegue necesarios en el directorio elegido, recibirá un mensaje informativo.
    + En caso de que exista algún tipo de error interno, el usuario recibirá un mensaje informativo. 
- **Rendimiento**:

    + El sistema deberá ser capaz de ejecutar operaciones de despliegue de forma concurrente para un volumen de usuarios estimado en 60.

- **Frecuencia**:

    + Se espera que los usuarios utilicen esta funcionalidad en una frecuencia aproximada de 3 despliegues/hora.

- **Importancia**: Muy alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable


RF-2: Monitorización de estado
------------------------------

- **Versión**: 2
- **Autores**: Diego Martín, Rodrigo Santamaría
- **Fuentes**: Análisis preliminar del sistema
- **Objetivos asociados**: 2
- **Requisitos asociados**: RF4, NFR2
- **Descripción**: Los diferentes usuarios podrán consultar en directo diferentes valores de estado como la memoria en uso o los diferentes procesos en ejecución.
- **Precondición**: 
   
    + El usuario deberá estar autenticado en el sistema.
    + Se conoce la información sobre el estado de los nodos.

- **Secuencia normal**:

    1. El usuario accede a la vista de monitorización.
    2. La lógica que dirige la interfaz establece conexiones con los nodos previamente detectados.
    3. La interfaz es actualizada cada vez que los nodos emiten información de estado.

- **Poscondición**: Se obtiene la información sobre el estado de los diferentes nodos.
- **Excepciones**:

    + En caso de que exista algún tipo de error interno (en especial en el establecimiento de las conexiones con los diferentes nodos), el usuario recibirá un mensaje informativo. 
- **Rendimiento**: Alto
- **Frecuencia**: Alta
- **Importancia**: Muy alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable
  
RF-3: Ejecución de comandos
---------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Entrevistas
- **Objetivos asociados**: 1
- **Requisitos asociados**: RF4, NFR-9
- **Descripción**: Acompañando a un despliegue o de forma independiente, el *software* permite ejecutar comandos en los diferentes nodos que conforman el sistema.
- **Precondición**:

    + El usuario deberá estar autenticado en el sistema.
    + El módulo de control de la interfaz ha establecido una conexión con los diferentes nodos presentes en la red.

- **Secuencia normal**:

    1. Si el comando se ejecuta de forma independiente, el usuario accede a la interfaz de ejecución de comandos, donde especifica el comando a ejecutar y los nodos receptores. En caso contrario dichos parámetros son especificados durante la creación de un despliegue.
    2. Los diferentes nodos reciben el comando.
    3. El comando es ejecutado, los diferentes nodos envían la información al controlador de la interfaz, que muestra el mensaje.
    4. El usuario puede en cualquier momento detener la ejecución del comando.

- **Poscondición**: El comando es ejecutado y el usuario obtiene la salida del mismo
- **Excepciones**:

    + En caso de que exista algún tipo de error interno, el usuario recibirá un mensaje informativo y se registrará el incidente en un fichero de *log*. 

- **Rendimiento**:

    + Paso 3: Generalmente la salida que un programa emite es muy elevada.

- **Frecuencia**: Alta

- **Importancia**: Muy alta

- **Urgencia**: Alta

- **Estado**: Completo
- **Estabilidad**: Estable
  
RF-4: Autenticación
-----------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Diseño preliminar del sistema
- **Objetivos asociados**: 1
- **Requisitos asociados**: NFR1
- **Descripción**: A través de una interfaz de autenticación los usuarios acceden al sistema.
- **Precondición**:

    + El usuario debe poseer unas credenciales en el sistema.

- **Secuencia normal**:

    1. El usuario accede al sistema y este muestra una interfaz de autenticación.
    2. El usuario introduce las claves de acceso.
    3. El sistema valida dichas claves utilizando la fuente de datos especificada por el administrador.
    4. Si los datos son válidos, el sistema da acceso al usuario y muestra la interfaz de control. En caso de que los datos no sean válidos el sistema muestra un mensaje de error.
    
- **Poscondición**: El usuario es autenticado en el sistema.
- **Excepciones**:

    + En caso de que exista algún tipo de error interno (como un fallo en el acceso al sistema de validación de claves), el usuario recibirá un mensaje informativo. 

- **Rendimiento**: Medio
- **Frecuencia**: Media
- **Importancia**: Muy alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable
  
RF-5: Validar una conexión **WebSocket**
-------------------------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Fases de diseño del sistema
- **Objetivos asociados**: OBJ-2, OBJ-3, OBJ-4
- **Requisitos asociados**: NRF7
- **Descripción**: Las conexiones **WebSocket** cifradas utilizando HTTPS que se realizan utilizando certificados no confiables o sin un campo **CN** válido emiten un error no interactivo. El sistema recoge dicho error y muestra un mensaje en la interfaz de usuario, solicitando la validación del certificado de la misma forma que en una conexión HTTPS tradicional.
- **Precondición**: 
    El usuario debe estar autenticado en el sistema. Se da la siguiente secuencia de interacción:
    1. El usuario accede a la interfaz principal de la aplicación, y el sistema detecta los nodos presentes en el mismo.
    2. El mecanismo de control de la interfaz intenta establecer la conexión con el resto de nodos existentes y se detecta el error en la validación del certificado.

- **Secuencia normal**:
    1. La interfaz muestra un mensaje informativo al usuario, indicando que la funcionalidad de la aplicación se verá limitada debido a este problema.
    2. El usuario clica en el elemento solicitado por la interfaz, que muestra a través de los mecanismos del navegador la información del certificado y un elemento de control para validar el mismo.
    3. El usuario valida el certificado.
    4. La interfaz intenta establecer una conexión **websocket** y en caso de éxito, muestra un mensaje de confirmación al usuario.
    5. El usuario retorna a la interfaz principal. El problema ha sido resuelto.
    
- **Poscondición**: El usuario puede utilizar el canal **WebSocket**
- **Excepciones**: Errores en la conexión entre la interfaz y el servidor, resueltos por el navegador.
- **Rendimiento**: Alto
- **Frecuencia**: Una vez por cada sesión. Se espera alta
- **Importancia**: Media
- **Urgencia**: Baja
- **Estado**: Completo
- **Estabilidad**: Estable
  

RF-6: Instalación del sistema
--------------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Entrevistas, fases de desarrollo
- **Descripción**: El administrador contará con un conjunto de herramientas incluidas en el paquete **software** para realizar la instalación del mismo.
- **Precondición**: El Administrador debe contar con los permisos de instalación suficientes y contar con una copia del **software** o acceso a un repositorio de paquetes.
- **Secuencia normal**:
    1. El administrador ejecuta el *script* de instalación con las opciones que considere pertinentes.
    2. Tras la instalación, configura los diferentes certificados que el *software* requiere.

- **Poscondición**: El software está instalado y configurado.
- **Excepciones**: Diferentes errores relacionados con la falta de permisos pueden darse durante el paso 1. Dichos errores son descritos en el *script* de instalación en lenguaje humano, y tras actuar en consecuencia, la instalación puede retomarse, generalmente, desde el punto en el que el error aparece.
- **Rendimiento**:
- **Frecuencia**: La instalación es realizada una vez por cada uno de los nodos, salvo circunstancias particulares (reinstalación, actualización...)
- **Importancia**: Baja
- **Urgencia**: Baja
- **Estado**: Completo
- **Estabilidad**: Estable 

RF-7: Gestión de errores
---------------------------
  
- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Fases de desarrollo, análisis del sistema
- **Requisitos asociados**: RF5
- **Descripción**: En caso de que un error ocurra, el sistema debe recuperarse del mismo de forma transparente, o en caso de que no sea posible, informar al usuario de dicha situación sugiriendo opciones para la recuperación del mismo.
- **Precondición**: Ha ocurrido un error (excepción, validación insatisfactoria de parámetros introducidos por el usuario...) fruto de una interacción con el sistema. Generalmente el código que ejecuta dicha acción cuenta con una serie de puntos de entrada para gestionar este tipo de comportamiento erróneo.

- **Secuencia normal**:
    1. El sistema identifica el tipo de error y envía un mensaje a la interfaz de usuario, con una serie de parámetros que indican métodos de recuperación en caso de que sea necesario.
    2. El mecanismo de control de la interfaz analiza la respuesta del servidor tras el envío de una solicitud y determina que se trata de un error.
    3. La interfaz muestra el mensaje informativo así como los elementos de control que permiten subsanar el mismo.
    4. En caso de que el usuario decida seguir el consejo dado por la interfaz, realiz las operaciones indicadas y el error es resuelto.
    
- **Poscondición**: La sesión es funcional de nuevo. El usuario puede en este momento repetir la operación que deseaba en primera instancia.
- **Excepciones**:

    + Si el error no es determinable, se ejecuta el caso de uso considerándolo un error "desconocido".
- **Rendimiento**: Bajo
- **Frecuencia**: Bajo
- **Importancia**: Media
- **Urgencia**: Media
- **Estado**: Completo
- **Estabilidad**: Estable
  
RF-8: Procesar petición
--------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Fases de desarrollo, análisis del sistema
- **Objetivos asociados**: OBJ-1, OBJ-2, OBJ-4
- **Descripción**: El rol **deployer** y el controlador de la interfaz de usuario solicitan a los diferentes nodos que desempeñan el rol de **receiver** la realización de diferentes acciones. Estos deben identificar la acción a llevar a cabo y validar los diferentes parámetros provistos, así como verificar que el solicitante es de confianza.
- **Precondición**:
- **Secuencia normal**:
    1. El sistema recibe una petición, y valida la identidad del solicitante a través de los mecanismos dispuestos por el protocolo HTTPS.
    2. En caso de que la validación sea satisfactoria, el sistema identifica el tipo de acción a realizar.
    3. Se realiza una de las siguientes acciones:
    
        - En caso de que se solicite un despliegue, comienza el caso de uso RF-9.
        - En caso de que se solicite recibir la información sobre el estado del nodo, el cliente es añadido a la lista de interesados y comienza el caso de uso RF-10.
        - En caso de que se solicite la ejecución de un comando, comienza el caso de uso RF-11.
        
- **Poscondición**: La acción es realizada
- **Excepciones**: En caso de que la identidad del solicitante no pueda ser validada, la conexión es rechazada. El resto de errores son gestionados por los puntos de extensión.
- **Rendimiento**: Alto
- **Frecuencia**: Alta
- **Importancia**: Alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable

RF-9: Realizar despliegue
----------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar
- **Objetivos asociados**: OBJ-1
- **Descripción**: Ante la petición de un usuario, se realiza un despliegue.
- **Precondición**:
- **Secuencia normal**:
        1. El nodo procesa los diferentes campos de la solicitud y extrae los mismos.
        2. Se validan todos los parámetros y se decide el directorio de despliegue y permisos de los archivos desplegados en función de los mismos.
        3. Se pueden dar las siguientes situaciones adicionales:
        
            +  En caso de que el usuario lo solicite, el servicio será almacenado en su instancia local de **Tomcat**.
            +  En caso de que sea solicitado por el usuario, se publicará un servicio asociado al despliegue en **Polo** (si existe en el sistema).
            +  Si existe el fichero y la petición indica que no sea sobreescrito, la operación termina.
            
        4. Los archivos son copiados.
        5. En caso de que se solicite la ejecución de un comando, comienza el caso de uso RF-11.

- **Poscondición**: El despliegue se ha realizado correctamente.
- **Excepciones**: En caso de que el usuario no disponga de los suficientes permisos de ejecución, se emitirá un mensaje de error a través de la interfaz de usuario.
- **Rendimiento**: Alto
- **Frecuencia**: Alta
- **Importancia**: Alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable

RF-10: Enviar estado
--------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar
- **Objetivos asociados**: OBJ-2
- **Requisitos asociados**: NFR-3
- **Descripción**: Periódicamente la información sobre el estado del nodo es emitida a los solicitantes.
- **Precondición**:
- **Secuencia normal**:
    1. De forma continua (en intervalos de un segundo), se verifica que existan conexiones interesadas en la información del estado del nodo.
    2. En caso de que exista al menos una, se procede a la recolección de dichos datos. Comienza el caso de us RF-13 En caso contrario la ejecución de esta iteración termina y se espera al siguiente segundo.
    3. Los datos son enviados a todos los interesados recorriendo la colección de conexiones.
- **Poscondición**: Los datos son enviados a los diferentes clientes interesados, que procesan la información y la muestran.
- **Excepciones**:

    + En el caso de que se dé un fallo en la conexión de red, se registrará el error y comenzará el caso de uso **RF-7**
- **Rendimiento**: Alto
- **Frecuencia**: Alta
- **Importancia**: Alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable


RF-11: Ejecutar comando
--------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Entrevistas
- **Objetivos asociados**: OBJ-3, OBJ4
- **Requisitos asociados**: NFR-3
- **Descripción**: El sistema ejecuta un comando y vincula sus canales de salida a un sistema de notificaciones que es capaz de detectar nuevos mensajes y difundirlos.
- **Precondición**:
- **Secuencia normal**:
        1. Tras la solicitud de realización de un comando, el sistema rebaja sus permisos a los permisos del usuario, a fin de garantizar que ninguna operación no autorizada es llevada a cabo y ejecuta el comando.
        2. Se vincula el comando a los canales de difusión de los mismos.
        3. Cada vez que se emita un mensaje, el sistema recibe una notificación y difunde el mensaje. En caso de que el mensaje sea de finalización, un indicador de dicha situación es retransmitido. 
- **Poscondición**: Los usuarios reciben la información de la ejecución a través de la interfaz.
- **Excepciones**: En caso de que el usuario no disponga de los suficientes permisos de ejecución, el usuario es notificado a través del mismo canal.
- **Rendimiento**: Alto
- **Frecuencia**: Alta
- **Importancia**: Alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable


RF-12: Procesar mensaje
--------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Entrevistas
- **Objetivos asociados**: OBJ-3, OBJ4
- **Requisitos asociados**: NFR-3 
- **Descripción**: Tras la ejecución de un comando el sistema procesa la salida por los canales estándar y de error y emite un mensaje que contiene el valor de dicha salida, que es devuelto al usuario.
- **Precondición**: Tiene que haberse ejecutado un comando
- **Secuencia normal**:
        1. A través de los mecanismos de comunicación entre procesos que el sistema operativo ofrece, se detecta la generación de un mensaje.
        2. El sistema determina de qué *buffer* procede el mensaje, recoge la cadena de caracteres y solicita la difusión del mismo indicándoselo a la entidad a cargo. En caso de que el mensaje sea de fin de ejecución, el mensaje recoge esta situación.
- **Poscondición**: El servidor es notificado del mensaje.
- **Excepciones**: Fallo en la comunicación entre procesos.
- **Rendimiento**: Alto
- **Frecuencia**: Alto
- **Importancia**: Alta
- **Urgencia**: Media
- **Estado**: Completo
- **Estabilidad**: Estable
  
RF-13 Recoger estado
-----------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar del sistema
- **Objetivos asociados**: OBJ-2
- **Requisitos asociados**: NFR-2
- **Descripción**: A través de llamadas al sistema, consulta de ficheros o cualquier otro mecanismo, los datos sobre el estado del sistema son incluidos en una colección que se retorna al solicitante.
- **Precondición**:
- **Secuencia normal**:
        1. Mediante el punto de entrada dispuesto a tal efecto, se solicita la recolección de datos.
        2. De forma secuencial se ejecuta el procedimiento necesario para la obtención del dato en cuestión y se añade a la colección.
- **Poscondición**: Se retorna la colección
- **Excepciones**: En caso de fallo en la recolección de un dato, se incluye un valor nulo.
- **Rendimiento**:
- **Frecuencia**: En caso de que exista al menos un interesado, una petición por segundo.
- **Importancia**: Alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable
- **Comentarios**: Los diferentes sistemas operativos con los que se debe trabajar cuentan con un conjunto diferente de mecanismos para la obtención de datos. El sistema se debe adaptar a cada uno de ellos.

Vista de casos de uso
---------------------

.. toctree::
    :maxdepth: 2

    uc

.. 
    - **Versión**: 
    - **Autores**: 
    - **Fuentes**: 
    - **Objetivos asociados**: 
    - **Requisitos asociados**: 
    - **Descripción**
    - **Precondición**
    - **Secuencia normal**
    - **Poscondición**
    - **Excepciones**
    - **Rendimiento**
    - **Frecuencia**
    - **Importancia**
    - **Urgencia**
    - **Estado**
    - **Estabilidad**
    - **Comentarios**