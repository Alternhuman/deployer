Patrones de diseño destacados
=============================

- La clase ``NotCheckingHostnameHTTPAdapter`` es un adaptador que modifica el comportamiento de otro objeto "interceptando" varias de las llamadas a un conjunto de funciones, reemplazándolas por otras integradas en el módulo.
- La estructura de la aplicación se basa en el patrón MVC, siendo el controlador el sistema de enrutado y las diferentes clases ``Handler``, el modelo cada uno de los datos a los que se accede (monitor de estado, archivos auxiliares...) y la vista la interfaz web.
- El uso de decoradores como ``@engine`` facilitan la modificación del comportamiento de la aplicación.
