Vista de interacción
====================

Inicio de sesión
----------------

.. image:: ../img/authentication.*
    :align: center

La fase de inicio de sesión es relativamente compleja debido a los diferentes flujos de información que intervienen en la misma. El usuario deberá introducir sus credenciales de usuario en el *frontend* web, que procederá a la validación de los datos. En caso de que dicha validación sea satisfactoria, se envía al usuario el código JavaScript que incluye la lógica de la aplicación web, así como ficheros HTML y CSS y una cookie que identificará al usuario en otras sesiones. Una vez recibidos y cargados, se solicita la lista de nodos presentes en la red, para la cual se utiliza de nuevo el controlador del *backend* y un binding de Marco. Los datos son devueltos al usuario, que establece conexiones WebSocket a cada uno (aunque esta circunstancia no se refleje en el diagrama debido a la naturaleza del mismo) de los nodos. La conexión debe incluir el mensaje contenido en la cookie que el *backend* de deployer ha enviado al cliente. En caso de que la cookie sea válida, la conexión es establecida.