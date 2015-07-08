Diseño procedimental
====================

En este apartado se referencian los algoritmos implementados en el sistema que son considerados de mayor relevancia.

La aplicación utiliza las siguientes bibliotecas y *frameworks*:
    
- **Tornado** como servidor web.
- **Snorky** para la gestión de los **WebSocket**
- **Jade** como motor de renderizado de plantillas (mediante **pyjade**.
- **jQuery** como biblioteca para la gestión de peticiones asíncronas y gestión de los diferentes elementos con el *plugin* **jQuery Cookie**.
- **Bootstrap** para la gestión de los elementos visuales.
- **MarcoPolo** para la detección de los diferentes nodos.
- **PAM** para la gestión de usuarios mediante la interfaz **python-pam**.

La autenticación en el cliente se realiza mediante la interfaz PAM disponible en Python. En caso de ser exitosa, el cliente recibe una cookie segura, firmada mediante HMAC y marcada temporalmente. Dicha cookie es enviada en todas las transmisiones WebSocket como token de autenticación (los nodos son capaces de descifrar el valor de la misma al conocer la clave criptográfica con la que se ha realizado el proceso de firmado).

Antes de realizarse el despliegue se crea el canal **WebSocket**. Todas las salidas se envían por el mismo canal. Los nodos mantienen una tabla clave-valor para identificar los **WebSockets** abiertos, siendo la clave el nombre de usuario en el sistema (mediante PAM dichos nombres son homogéneos en el sistema). Cada ejecución cuenta con un identificador aleatorio que el servidor comparte con el cliente.


Despliegue
----------

.. literalinclude:: ../../../../marcodeployer/deployer.py
    :language: python
    :lines: 141-148,166-212,228-256
    :linenos: 

Secuencia de realización de un despliegue. Mediante el uso de ``futures`` se consigue que el código sea asíncrono y de esta forma se optimiza el rendimiento del sistema de forma significativa.

Recepción de un despliegue
--------------------------

.. literalinclude:: ../../../../marcodeployer/receiver.py
    :language: python
    :lines: 82-161
    :linenos:


Ejecución de un comando
-----------------------

.. literalinclude:: ../../../../marcodeployer/bufferprocessor.py
    :language: python
    :lines: 23-
    :linenos:

La ejecución de un comando es completamente asíncrona, dado que se vincula el descriptor de fichero de cada uno de los *streams* de salida del comando al bucle de eventos de Tornado, añadiendo manejadoras que recojan los diferentes eventos emitidos por el bucle relativos a dichos descriptores.

Recolección de datos
--------------------

.. literalinclude:: ../../../../marcodeployer/statusmonitor.py
    :language: python
    :lines: 7,28-41,71
    :linenos:

La recolección de datos se realiza mediante llamadas al sistema.