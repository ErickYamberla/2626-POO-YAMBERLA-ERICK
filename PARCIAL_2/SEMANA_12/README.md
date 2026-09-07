# Restaurante App - Semana 12

Estudiante: Erick Yamberla

## Descripción del sistema
Este proyecto es una evolución del sistema restaurante_app desarrollado durante las semanas anteriores. El objetivo principal de la Semana 11 es mantener la lógica previa del restaurante y ampliar la gestión para incorporar la venta de productos, el control de stock y la relación entre usuarios y productos mediante una colección de ventas.

La aplicación permite registrar productos, usuarios, vender artículos y consultar las ventas realizadas por un usuario específico. Además, toda la información se conserva en archivos JSON para que pueda recuperarse al reiniciar la aplicación.

## Estructura del proyecto
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
├── main.py
├── README.md
└── __pycache__/

## Responsabilidad de cada componente
- modelos/producto.py:
  Representa cada producto del restaurante y conserva el atributo stock. Incluye validaciones del código, nombre, precio y stock, además de serialización a JSON.

- modelos/usuario.py:
  Representa a una persona registrada que puede realizar compras. Incluye validaciones básicas y soporte para convertirse a diccionario y reconstruirse desde JSON.

- modelos/venta.py:
  Representa la relación entre un usuario y un producto vendido. Guarda como mínimo el identificador del usuario, el código del producto y la cantidad vendida.

- servicios/restaurante.py:
  Es el centro de la lógica de negocio. Administra las colecciones de productos, usuarios y ventas, valida reglas del negocio y ejecuta las operaciones de registro, búsqueda, actualización y venta.

- servicios/archivo_servicio.py:
  Centraliza la lectura y escritura de los archivos JSON de productos, usuarios y ventas. Maneja errores de lectura, escritura y contenido inválido.

- main.py:
  Coordina la interacción con la consola. Solicita los datos al usuario, llama a los métodos del servicio y evita modificar directamente las colecciones internas.

## Funcionamiento del stock
Cada producto cuenta con un atributo stock que indica la cantidad disponible. La venta solo puede realizarse si:
- el usuario existe,
- el producto existe,
- la cantidad es mayor que cero,
- el stock disponible es suficiente.

Cuando se registra una venta, la cantidad solicitada se descuenta del stock del producto y la operación queda registrada en la colección de ventas.

Ejemplo:
- Producto: Hamburguesa Clásica
- Stock inicial: 18
- Venta: 3 unidades
- Stock final: 15

## Relación Usuario–Producto mediante Venta
La relación principal del sistema se representa con la clase Venta. Una venta conserva la referencia del usuario y del producto, además de la cantidad comprada. Esto permite cruzar información de forma clara y consultar las ventas asociadas a cada usuario.

La operación principal es:
- vender_producto(codigo_producto, identificacion_usuario, cantidad)

Esta operación crea una instancia de Venta, agrega la venta a la colección correspondiente y descuenta la cantidad vendida del stock del producto.

## Persistencia JSON
La persistencia se amplió para conservar tres colecciones fundamentales:
- productos.json
- usuarios.json
- ventas.json

Cada clase del modelo puede convertirse a diccionario y reconstruirse desde JSON. La aplicación guarda la información después de cada operación relevante:
- registrar, actualizar o eliminar un producto: guardar productos.json
- registrar, actualizar o eliminar un usuario: guardar usuarios.json
- registrar una venta: guardar ventas.json y productos.json

La carga se realiza al iniciar la aplicación. Si los archivos no existen, el sistema arranca con colecciones vacías. Si un archivo tiene JSON inválido, el programa lo maneja con mensajes claros sin detener la ejecución.

## Excepciones controladas
El sistema incorpora manejo de errores para situaciones habituales:
- FileNotFoundError: si un archivo no existe, se inicializa con una colección vacía.
- json.JSONDecodeError: si el contenido JSON es inválido.
- PermissionError: si no hay permisos de lectura o escritura.
- KeyError: cuando un registro JSON no tiene una clave esperada.
- ValueError: cuando una validación de Producto, Usuario o Venta falla.

Se evita el uso de capturas genéricas para ocultar errores; se manejan de forma explícita para mantener la integridad del sistema.

## Menú de opciones
El sistema ofrece las siguientes operaciones principales:
1. Registrar producto
2. Buscar producto
3. Actualizar producto
4. Eliminar producto
5. Listar productos
6. Registrar usuario
7. Buscar usuario
8. Actualizar usuario
9. Eliminar usuario
10. Listar usuarios
11. Mostrar categorías
12. Registrar Venta
13. Consultar ventas por usuario
14. Salir

La opción "Registrar Venta" solicita la identificación del usuario, el código del producto y la cantidad. Luego valida las condiciones del negocio y descuenta el stock para confirmar la operación.

## Forma de ejecución
Para ejecutar la aplicación desde la carpeta del proyecto, use:

python main.py

Desde la consola interactiva deberá registrar usuarios y productos con stock disponible. Luego podrá realizar ventas y consultar las ventas de un usuario específico.

## Pruebas realizadas
Se realizaron pruebas básicas para verificar el funcionamiento del sistema:
- Registro de usuarios y productos con stock real.
- Venta válida: se descuenta el stock correctamente y se registra la venta.
- Consulta de ventas por usuario: devuelve solo las ventas asociadas a la identificación solicitada.
- Intento de venta con stock insuficiente: la operación es rechazada sin afectar los datos.
- Cierre y reinicio del programa: se recuperan productos, usuarios y ventas desde JSON.

## Mejoras realizadas (Semana 12)
Se implementaron índices en memoria para optimizar búsquedas y consultas frecuentes sin sustituir las colecciones principales:

- Productos y usuarios: ya se almacenan en diccionarios internos (dict) indexados por código de producto y por identificación de usuario, lo que permite búsquedas O(1) con buscar_producto(codigo) y buscar_usuario(identificacion).
- Ventas por usuario: se añadió un índice auxiliar _ventas_por_usuario (dict) que mapea identificaciones de usuario a listas de Venta. La consulta ventas_por_usuario(identificacion) utiliza este índice para evitar recorrer cada vez la lista completa de ventas.

Se mantuvieron las listas principales (_ventas) para persistencia y recorrido, y al registrar una venta se actualizan ambas estructuras (lista e índice). Al cargar los datos desde JSON se reconstruyen los índices en memoria.

## Observación
El proyecto conserva la estructura modular trabajada durante el curso y evoluciona la aplicación previa sin reemplazar los modelos por diccionarios. Los modelos siguen siendo objetos y la lógica de negocio se mantiene en el servicio Restaurante.

## Pruebas principales realizadas (resumen)
- Buscar producto por código: verificado con buscar_producto(codigo).
- Buscar usuario por identificación: verificado con buscar_usuario(identificacion).
- Consultar ventas por usuario: verificado que ventas_por_usuario devuelve ventas sin recorrer toda la colección de ventas.
- Registrar venta: la venta se registra, el stock se actualiza y el índice por usuario se mantiene coherente.
- Reinicio de la aplicación: al volver a ejecutar main.py, los datos JSON se cargan y los índices se reconstruyen correctamente.
