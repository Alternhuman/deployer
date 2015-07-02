Ámbito
======

El software deberá ser ejecutado en un conjunto de nodos con una serie de características técnicas limitadas, por lo que la optimización del rendimiento del mismo es un aspecto clave. Existen además restricciones de tiempo, como la recogida en el requisito no funcional **NFR-2**.

Otro aspecto crítico es la seguridad del sistema, dado que durante diferentes fases de la ejecución se transmiten mensajes que solicitan la realización de tareas asumiendo el rol de superusuario. Si un usuario malintencionado consigue acceder de forma no autorizada a dicha información podría comprometer la integridad de todo el sistema.