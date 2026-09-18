# Restaurante App - Semana 14

Estudiante: Erick Yamberla

Este proyecto corresponde a la evolucion de la aplicacion del restaurante para la Semana 14. Se parte de la base grafica desarrollada en la Semana 13 y se refactoriza la capa de interfaz para incorporar componentes y contenedores de Tkinter, manteniendo la separacion por modelos, servicios y vistas.

## Proposito de la semana

La actividad centra su atencion en la aplicacion correcta de componentes y contenedores dentro de la interfaz grafica. El objetivo es mejorar la organizacion visual de la aplicacion, reforzar la navegacion del sistema y completar el flujo de gestion de productos mediante botones y formularios, todo sin mezclar la logica del dominio con la capa de presentacion.

## Estructura del repositorio

Repositorio GitHub
??? restaurante_app/
?   ??? datos/
?   ?   ??? productos.json
?   ?   ??? usuarios.json
?   ??? modelos/
?   ?   ??? __init__.py
?   ?   ??? producto.py
?   ?   ??? usuario.py
?   ??? servicios/
?   ?   ??? __init__.py
?   ?   ??? archivo_servicio.py
?   ?   ??? restaurante_servicio.py
?   ??? ui/
?   ?   ??? __init__.py
?   ?   ??? login_view.py
?   ?   ??? main_view.py
?   ??? assets/              (opcional)
?   ??? main.py
??? README.md

## Componentes y contenedores utilizados

La interfaz se organiza con contenedores principales para separar la zona de autenticacion, la navegacion y la gestion de informacion. En la vista principal se usan:

- Frame y LabelFrame para estructurar secciones.
- ttk.Entry para capturar datos del producto.
- ttk.Button para ejecutar acciones como registrar, consultar, actualizar y eliminar.
- ttk.Treeview para mostrar la informacion de productos en formato tabular.
- Text para visualizar los usuarios registrados.

Estos elementos permiten una distribucion clara y ordenada de la informacion, mejorando la experiencia del usuario sin abandonar la organizacion modular del proyecto.

## Mejoras realizadas en la interfaz

- Se mantiene el inicio de sesion con validacion de usuario y contrasena.
- Se conserva la vista principal y la navegacion del sistema.
- La pantalla principal se divide en zonas de formulario, tabla y consulta de usuarios.
- La gestion de productos se presenta con controles claros y agrupados por funcion.
- Los mensajes de estado informan al usuario si la operacion fue exitosa o si ocurrio un error.
- La interfaz se actualiza automaticamente despues de cada operacion.

## Operaciones de productos implementadas

La seccion de productos integra las operaciones minimas requeridas:

- Registrar producto.
- Consultar/cargar producto por codigo.
- Actualizar producto.
- Eliminar producto.
- Visualizar informacion de todos los productos en una tabla.

Estas operaciones se ejecutan desde la interfaz grafica, pero las validaciones y la persistencia quedan dentro de `RestauranteServicio`, que se encarga de delegar la escritura al servicio de archivos JSON.

## Persistencia de datos

La informacion de productos y usuarios se guarda en archivos JSON ubicados en `restaurante_app/datos/`.

- `productos.json`: guarda la lista de productos del restaurante.
- `usuarios.json`: conserva los usuarios de acceso de la aplicacion.

La lectura y escritura se realiza exclusivamente a traves de `ArchivoServicio` y `RestauranteServicio`, evitando que la vista manipule directamente los archivos JSON.

## Como ejecutar la aplicacion

Desde la raiz del proyecto, ejecute:

python PARCIAL_2/SEMANA_14/restaurante_app/main.py

O bien, si se encuentra dentro de la carpeta `SEMANA_14`:

python restaurante_app/main.py

La aplicacion abrira la vista de login y, despues de validar las credenciales, mostrara el panel principal con la gestion de productos y la consulta de usuarios.

## Usuarios de prueba

Los usuarios almacenados para iniciar sesion son:

- Usuario: admin
- Contrasena: admin123

- Usuario: carlos
- Contrasena: carlos456

## Conclusion

La Semana 14 refuerza la separacion de responsabilidades del proyecto, mantiene la logica de negocio en servicios y aprovecha componentes de Tkinter y contenedores para mejorar la experiencia visual del usuario. La estructura modular se conserva y se acompana con la gestion eficiente de productos mediante operaciones simples y persistentes.
