Requisitos no funcionales
=========================

NFR-1: Autenticación con credenciales ya conocidas por los usuarios
-------------------------------------------------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Entrevistas, análisis preliminar del sistema
- **Objetivos asociados**: OBJ-1
- **Requisitos asociados**: RF-1
- **Descripción**: El sistema deberá utilizar el directorio LDAP presente en la infraestructura en la que la aplicación se integra
- **Importancia**: Alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable

NFR-2: Frecuencia de actualización del monitor de estado 
--------------------------------------------------------

- **Versión**: 1.5
- **Autores**: Diego Martín, Rodrigo Santamaría
- **Fuentes**: Reuniones del equipo, análisis preliminar
- **Objetivos asociados**: OBJ-2
- **Requisitos asociados**: RF-2
- **Descripción**: La frecuencia debe ser de un segundo.
- **Importancia**: Media
- **Urgencia**: Baja
- **Estado**: Completo
- **Estabilidad**: Estable
- **Comentarios**: Esta restricción no es rígida, admitiéndose frecuencias de actualización oscilantes entre 0.5 y 2 segundos.


NFR-3: Eliminación de "cuellos de botella"
------------------------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar
- **Objetivos asociados**: OBJ-2, OBJ-3
- **Requisitos asociados**: 
- **Descripción**: La comunicación entre los diferentes nodos y la interfaz de usuario no debe utilizar el nodo encargado del control de la ejecución como punto intermedio. Para ello se utilizarán canales de comunicación que utilicen el protocolo **Websocket**.
- **Importancia**: Media
- **Urgencia**: Baja
- **Estado**: Completo
- **Estabilidad**: Estable

NFR-4: Descubrimiento de los nodos con MarcoPolo
------------------------------------------------

- **Versión**: 1.5
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar
- **Objetivos asociados**
- **Requisitos asociados**
- **Descripción**: El descubrimiento de los diferentes nodos presentes en la red se deberá realizar a través de comandos **Request-For** del protocolo MarcoPolo, aprovechando además la información de los parámetros opcionales que incluye el comando como filtro, en caso de que se desee.
- **Importancia**: Media
- **Urgencia**: Baja
- **Estado**: Completo
- **Estabilidad**: Estable

NFR-5: Servicios dinámicos
--------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Fases de desarrollo del sistema
- **Objetivos asociados**
- **Requisitos asociados**: NRF4
- **Descripción**: Los diferentes servicios que la herramienta publique serán de tipo dinámico.
- **Importancia**: Media
- **Urgencia**: Baja
- **Estado**: Completo
- **Estabilidad**: Estable


NFR-6: Tornado
--------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar del sistema
- **Objetivos asociados**
- **Requisitos asociados**
- **Descripción**: Toda la lógica de los diferentes roles servidor presentes en la aplicación se implementará en el **framework** Tornado con el objetivo de optimizar el rendimiento.
- **Importancia**: Media
- **Urgencia**: Baja
- **Estado**: Completo
- **Estabilidad**: Estable

NFR-7 Encriptación
------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Análisis preliminar del sistema
- **Objetivos asociados**
- **Requisitos asociados**
- **Descripción**: Todas las comunicaciones entre los diferentes componentes se realizan de forma cifrada utilizando HTTPS o WSS (*Secure WebSocket*). Ambos roles (cliente y servidor) deberán aportar un certificado que será validado por la entidad al otro lado del canal durante la creación del canal.
- **Importancia**: Alta
- **Urgencia**: Media
- **Estado**: Completo
- **Estabilidad**: Estable


NFR-8 Permisos
--------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Fases de desarrollo del sistema
- **Objetivos asociados**: OBJ-3, OBJ-4
- **Requisitos asociados**: RF-3, RF-4
- **Descripción**: Únicamente el usuario que ha realizado la ejecución está autorizado a visualizar la información de salida.
- **Importancia**: Alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable


NFR-9 Visualización de la salida
--------------------------------

- **Versión**: 1
- **Autores**: Diego Martín
- **Fuentes**: Fases de desarrollo del sistema
- **Objetivos asociados**: OBJ-3, OBJ-4
- **Requisitos asociados**: RF-3
- **Descripción**: Las salidas estándar y de error (``stdout``, ``stderr``) deben ser observables y diferenciables en el momento que se genera la información. La información sobre cada nodo y ejecución debe ser diferenciable.
- **Importancia**: Alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable

.. 
    - **Versión**
    - **Autores**
    - **Fuentes**
    - **Objetivos asociados**
    - **Requisitos asociados**
    - **Descripción**
    - **Importancia**
    - **Urgencia**
    - **Estado**
    - **Estabilidad**
    - **Comentarios**


