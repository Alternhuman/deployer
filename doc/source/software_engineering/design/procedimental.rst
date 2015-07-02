Diseño procedimental
====================

En este apartado se referencian los algoritmos implementados en el sistema que son considerados de mayor relevancia.

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