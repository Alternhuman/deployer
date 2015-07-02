.. Análisis

Vista estática del sistema
==========================

.. image:: ../img/analysis_deployer.*
    :align: center

Vista de los paquetes de la vista de análisis. Se plantea el uso de una clase interfaz que presente al usuario una interfaz web o en el caso del paquete receiver, una serie de puntos de acceso sobre el protocolo HTTP. En el paquete receiver la funcionalidad accesoria se delega a clases de control que realicen la misma y retornen los resultados al controlador principal (handler).