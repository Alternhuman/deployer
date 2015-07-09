Diseño de datos
===============

Objetos de datos
----------------

El sistema utiliza un gran abanico de estructuras de datos, entre las que destacan las siguientes:

- Objetos :class:`Node <marcopolo.marco_conf.utils.Node>` para la identificación de los diferentes nodos.
- Objetos JSON para la comunicación entre la interfaz web y los diferentes servidores, así como entre un servidor deployer y las diferentes instancias de receiver.
- Objetos diccionario (:class:`dict`) con todos los datos sobre el sistema.
 
Estructuras de archivo
----------------------

Se consultan varias fuentes de datos en la aplicación:

- Módulo PAM. Es utilizado para la validación de credenciales.
- Ficheros ``/etc/passwd`` y ``/etc/shadow`` como segunda fuente de datos, en caso de que no se pueda acceder al módulo PAM o no se encuentre en dicha fuente de datos al usuario.
- Ficheros de configuración ``/etc/marcodeployer/deployer.cfg`` y  ``/etc/marcodeployer/secret``, que permiten modificar el comportamiento de la aplicación.
- Ficheros del sistema situados en las particiones virtuales ``/proc`` y ``/sys``, necesarios para la recolección de datos.
- Ficheros de *log*, que permiten analizar *a posteriori* el comportamiento del programa, en particular ante algún tipo de situación irregular.