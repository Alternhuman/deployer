Diseño arquitectónico
=====================

.. figure:: ../img/deployment.*
	:align: center

	La arquitectura comprende tres nodos que interaccionan entre sí. Un nodo cliente se conecta a un nodo de despliegue, obteniendo diferentes archivos interpretables por un navegador web. Dicho nodo de despliegue se conectará a uno o más nodos receptores, sobre los cuales se realizarán las operaciones de despliegue. También existe una conexión WebSocket directa entre los nodos receptores y el nodo cliente, a fin de eliminar el "cuello de botella" que el nodo de despliegue establecería si en comunicación figurara como intermediario.