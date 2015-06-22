Requisitos funcionales
----------------------

RF 1: Despliegue
~~~~~~~~~~~~~~~~

- **Versión**: 
- **Autores**: 
- **Fuentes**: 
- **Objetivos asociados**: 1
- **Requisitos asociados**: RF4
- **Descripción**: 
    El sistema realizar operaciones de despliegue.

- **Precondición**: 
    El usuario deberá estar autenticado en el sistema.

- **Secuencia normal**:

    1. El usuario solicita realizar una operación de despliegue.
    2. El sistema muestra la información sobre los diferentes nodos que admiten operaciones de despliegue.
    3. El usuario selecciona los nodos donde desea ubicar los ficheros.
    4. El usuario elige un fichero ejecutable e indica los diferentes parámetros de despliegue.
    5. Para cada uno de los ficheros a desplegar realizará esta acción.
    6. Una vez que termine de añadir ficheros, el despliegue comenzará.
    7. Si se indica un comando en uno o varios de los ficheros, el usuario recibe la salida de estos en la vista dispuesta a tal efecto.  Se ejecuta el caso de uso RF 4
- **Poscondición**:

    El usuario recibe la confirmación de éxito o un mensaje de error en su defecto.
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
- **Comentarios**

  

RF 2: Monitorización de estado
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Versión**: 
- **Autores**: 
- **Fuentes**: 
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

- **Poscondición**
- **Excepciones**:
    + En caso de que exista algún tipo de error interno (en especial en el establecimiento de las conexiones con los diferentes nodos), el usuario recibirá un mensaje informativo. 

- **Rendimiento**:
- **Frecuencia**:

    + 

- **Importancia**: Muy alta

- **Urgencia**: Alta

- **Estado**: Completo
- **Estabilidad**: Estable
- **Comentarios**
  
RF 3: Ejecución de comandos
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Versión**: 
- **Autores**: 
- **Fuentes**: 
- **Objetivos asociados**: 1
- **Requisitos asociados**: RF4
- **Descripción**: Acompañando a un despliegue o de forma independiente, el *software* permite ejecutar comandos en los diferentes nodos que conforman el sistema.

- **Precondición**:

    + El usuario deberá estar autenticado en el sistema.
    + El módulo de control de la interfaz ha establecido una conexión con los diferentes nodos presentes en la red.

- **Secuencia normal**:

    1. Si el comando se ejecuta de forma independiente, el usuario accede a la interfaz de ejecución de comandos, donde especifica el comando a ejecutar y los nodos receptores. En caso contrario dichos parámetros son especificados durante la creación de un despliegue.
    2. Los diferentes nodos reciben el comando.
    3. El comando es ejecutado, los diferentes nodos envían la información al controlador de la interfaz, que muestra el mensaje.
    4. El usuario puede en cualquier momento detener la ejecución del comando.

- **Poscondición**:
- **Excepciones**:

    + En caso de que exista algún tipo de error interno, el usuario recibirá un mensaje informativo. 

- **Rendimiento**:

    + Paso 3: Generalmente la salida que un programa emite es muy elevada.

- **Frecuencia**:

    + 

- **Importancia**: Muy alta

- **Urgencia**: Alta

- **Estado**: Completo
- **Estabilidad**: Estable
- **Comentarios**
  
RF 4: Autenticación
~~~~~~~~~~~~~~~~~~~

- **Versión**: 
- **Autores**: 
- **Fuentes**: 
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

- **Rendimiento**:

- **Frecuencia**:

- **Importancia**: Muy alta

- **Urgencia**: Alta

- **Estado**: Completo
- **Estabilidad**: Estable
- **Comentarios**
  



- **Versión**: 
- **Autores**: 
- **Fuentes**: 
- **Objetivos asociados**: 1
- **Requisitos asociados**: 
- **Descripción**: 
    El sistema realizar operaciones de despliegue.

- **Precondición**: 
    El usuario deberá estar autenticado en el sistema.

- **Secuencia normal**:

    1. El usuario solicita realizar una operación de despliegue.
    2. El sistema muestra la información sobre los diferentes nodos que admiten operaciones de despliegue.
    3. El usuario selecciona los nodos donde desea ubicar los ficheros.
    4. El usuario elige un fichero ejecutable e indica los diferentes parámetros de despliegue.
    5. Para cada uno de los ficheros a desplegar realizará esta acción.
    6. Una vez que termine de añadir ficheros, el despliegue comenzará.
    7. Si se indica un comando en uno o varios de los ficheros, el usuario recibe la salida de estos en la vista dispuesta a tal efecto.
- **Poscondición**:

    El usuario recibe la confirmación de éxito o un mensaje de error en su defecto.
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
- **Comentarios**
  



  


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