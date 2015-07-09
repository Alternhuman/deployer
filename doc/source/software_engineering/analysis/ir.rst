Requisitos de información
=========================

IRQ-1: Información sobre los usuarios del sistema
-------------------------------------------------

- **Versión**: 1.5
- **Autores**: Diego Martín
- **Fuentes**: Fases de desarrollo del sistema
- **Objetivos asociados**: OBJ-1, OBJ-3, OBJ-4
- **Requisitos asociados**: RF-1, RF-3, NFR-8
- **Descripción**: El sistema deberá consultar la información de los usuarios relativa a los permisos de acceso y ejecución sobre diferentes ficheros del sistema. Esta información se utilizará en el acceso al sistema y durante diferentes fases de las operaciones de despliegue y ejecución.
- **Datos específicos**: Nombre, UID y GID del usuario.
- **Tiempo de vida**: Permanente
- **Ocurrencias simultáneas**
- **Importancia**: Muy alta
- **Urgencia**: Elevada
- **Estado**: Completo
- **Estabilidad**: Completo
- **Comentarios**: Esta información no es gestionada por el *software*, sino únicamente consultada.

IRQ-2: Información de estado
----------------------------

- **Versión**: 1.5
- **Autores**: Diego Martín
- **Fuentes**: Diseño preliminar del sistema
- **Objetivos asociados**: OBJ-2
- **Requisitos asociados**: RF-2
- **Descripción**: El sistema almacenará diferentes registros de las operaciones realizadas en el mismo, así como una serie de mensajes que reflejen actualizaciones en el estado del sistema.
- **Datos específicos**: Ficheros *log*.
- **Tiempo de vida**: Permanente
- **Ocurrencias simultáneas**:
- **Importancia**: Media
- **Urgencia**: Elevada
- **Estado**: Completo
- **Estabilidad**: Completo

IRQ-3: Estadísticas del sistema
-------------------------------

- **Versión**: 2
- **Autores**: Diego Martín, Rodrigo Santamaría
- **Fuentes**: Análisis inicial, entrevistas y reuniones del equipo.
- **Objetivos asociados**: OBJ-3, OBJ-4
- **Requisitos asociados**: NRF-2, RF-2
- **Descripción**: La aplicación deberá generar y gestionar el envío de diferentes datos del sistema (CPU, memoria, temperatura...) en directo.
- **Datos específicos**: CPU, Temperatura, memoria libre, *swap*, listado de procesos con el consumo de memoria y CPU, extensible a otros datos.
- **Tiempo de vida**: Cada segundo se genera un nuevo conjunto de datos, descartando el anterior.
- **Ocurrencias simultáneas**: Una única ocurrencia por cada instancia.
- **Importancia**: Alta
- **Urgencia**: Alta
- **Estado**: Completo
- **Estabilidad**: Estable
- **Comentarios**

.. 
    - **Versión**
    - **Autores**
    - **Fuentes**
    - **Objetivos asociados**
    - **Requisitos asociados**
    - **Descripción**
    - **Datos específicos**
    - **Tiempo de vida**
    - **Ocurrencias simultáneas**
    - **Importancia**
    - **Urgencia**
    - **Estado**
    - **Estabilidad**
    - **Comentarios**