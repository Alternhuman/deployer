Diseño arquitectónico
=====================

.. figure:: ../img/deployment.*
	:align: center

	La arquitectura comprende tres nodos que interaccionan entre sí. Un nodo cliente se conecta a un nodo de despliegue, obteniendo diferentes archivos interpretables por un navegador web. Dicho nodo de despliegue se conectará a uno o más nodos receptores, sobre los cuales se realizarán las operaciones de despliegue. También existe una conexión WebSocket directa entre los nodos receptores y el nodo cliente, a fin de eliminar el "cuello de botella" que el nodo de despliegue establecería si en comunicación figurara como intermediario.

	En los nodos sobre los que se realizan las ejecuciones se ejecuta una instancia de **receiver.py**, que se encarga de la recepción de los diferentes ejecutables y comandos a ejecutar.

	En el nodo al que se conecta el cliente (en caso de que no sea su propio equipo) se ejecuta una instancia de **deployer.py**, encargado de la generación de la interfaz web, detección de nodos y realización del despliegue.
