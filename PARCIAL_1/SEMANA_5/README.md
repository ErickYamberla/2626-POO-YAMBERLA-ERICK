Nombre del estudiante: ERICK SANTIAGO YAMBERLA INZUASTI

Descripción
-----------
El sistema demuestra el uso de clases, objetos, constructores, atributos tipados, listas como tipo compuesto
y buenas prácticas de nombres (PascalCase para clases, snake_case para variables y métodos).

Estructura del proyecto
-----------------------
restaurante_app/
├── modelos/
│   ├── __init__.py
│   ├── producto.py   # Clase Producto (str, int, float, bool)
│   └── cliente.py    # Clase Cliente (str, int, bool)
├── servicios/
│   ├── __init__.py
│   └── restaurante.py # Clase RestauranteService (listas para almacenar objetos)
└── main.py            # Punto de arranque: crea objetos y muestra información

Tipos de datos utilizados
-------------------------
- str: nombre, descripcion, telefono, correo
- int: codigo, id_cliente, puntos_fidelidad
- float: precio
- bool: disponible, activo
- list: almacenamiento de múltiples objetos Producto y Cliente en el servicio

Reflexión corta
----------------
Usar identificadores descriptivos facilita la lectura y mantenimiento del código. Elegir tipos de datos
adecuados (p. ej. float para precios, int para identificadores) evita errores y hace más claro el modelado
del dominio. Las listas permiten gestionar colecciones de objetos de forma eficiente dentro de una estructura
modular.

Instrucciones
------------
1. Ejecutar el programa desde la carpeta `restaurante_app` con:

   python main.py

