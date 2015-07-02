Requisitos no funcionales
=========================

NFR-1: Autenticación con credenciales ya conocidas por los usuarios
-------------------------------------------------------------------

- **Versión**
- **Autores**
- **Fuentes**
- **Objetivos asociados**
- **Requisitos asociados**
- **Descripción**: El sistema deberá utilizar el directorio LDAP presente en la infraestructura en la que la aplicación se integra
- **Importancia**: Alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Alta
- **Comentarios**


NFR-2: Frecuencia de actualización del monitor de estado
-----------------------------------------------------------

- **Versión**
- **Autores**
- **Fuentes**
- **Objetivos asociados**
- **Requisitos asociados**
- **Descripción**: La frecuencia debe ser de un segundo.
- **Importancia**: Media
- **Urgencia**: Baja
- **Estado**: Completo
- **Estabilidad**
- **Comentarios**: Esta restricción no es rígida, admitiéndose frecuencias de actualización oscilantes entre 0.5 y 2 segundos.


NFR-3: Eliminación de "cuellos de botella"
------------------------------------------

- **Versión**
- **Autores**
- **Fuentes**
- **Objetivos asociados**
- **Requisitos asociados**
- **Descripción**: La comunicación entre los diferentes nodos y la interfaz de usuario no debe utilizar el nodo encargado del control de la ejecución como punto intermedio. Para ello se utilizarán canales de comunicación que utilicen el protocolo **Websocket**.
- **Importancia**: Media
- **Urgencia**: Baja
- **Estado**: Completo
- **Estabilidad**
- **Comentarios**:

NFR-4: Descubrimiento de los nodos con MarcoPolo
------------------------------------------------

- **Versión**
- **Autores**
- **Fuentes**
- **Objetivos asociados**
- **Requisitos asociados**
- **Descripción**: El descubrimiento de los diferentes nodos presentes en la red se deberá realizar a través de comandos **Request-For** del protocolo MarcoPolo, aprovechando además la información de los parámetros opcionales que incluye el comando como filtro, en caso de que se desee.
- **Importancia**: Media
- **Urgencia**: Baja
- **Estado**: Completo
- **Estabilidad**
- **Comentarios**

NFR-5: Servicios dinámicos
--------------------------

- **Versión**
- **Autores**
- **Fuentes**
- **Objetivos asociados**
- **Requisitos asociados**: NRF4
- **Descripción**: Los diferentes servicios que la herramienta publique serán de tipo dinámico.
- **Importancia**: Media
- **Urgencia**: Baja
- **Estado**: Completo
- **Estabilidad**
- **Comentarios**


NFR-6: Tornado
--------------

- **Versión**
- **Autores**
- **Fuentes**
- **Objetivos asociados**
- **Requisitos asociados**
- **Descripción**: Toda la lógica de los diferentes roles servidor presentes en la aplicación se implementará en el **framework** Tornado con el objetivo de optimizar el rendimiento.
- **Importancia**: Media
- **Urgencia**: Baja
- **Estado**: Completo
- **Estabilidad**
- **Comentarios**

NFR-7 Encriptación
------------------

- **Versión**
- **Autores**
- **Fuentes**
- **Objetivos asociados**
- **Requisitos asociados**
- **Descripción**: Todas las comunicaciones entre los diferentes componentes se realizan de forma cifrada utilizando HTTPS o WSS (*Secure WebSocket*). Ambos roles (cliente y servidor) deberán aportar un certificado que será validado por la entidad al otro lado del canal durante la creación del canal.
- **Importancia**
- **Urgencia**
- **Estado**
- **Estabilidad**
- **Comentarios**

.. 
    s
    3 

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


