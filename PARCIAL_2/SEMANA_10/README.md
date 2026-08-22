# PARCIAL_2 - SEMANA_10

Nombre del estudiante: Erick Santiago Yamberla Inzuasti

Descripción

Proyecto `restaurante_app` con persistencia de productos en formato JSON. Los productos se guardan en `datos/productos.json` y se cargan al inicio para reconstruir objetos Producto.

Estructura mínima requerida

restaurante_app/
├── datos/
│   └── productos.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
├── main.py
└── README.md

Responsabilidades

- modelos/producto.py: Clase Producto, validaciones, conversión to_dict()/from_dict().
- modelos/usuario.py: Clase Usuario (información en memoria para esta semana).
- servicios/archivo_servicio.py: Lectura y escritura de `datos/productos.json` con manejo de excepciones.
- servicios/restaurante.py: Administra objetos Producto en memoria y solicita carga/guardado al ArchivoServicio.
- main.py: Punto de entrada y coordina el menú.

Funcionamiento de productos.json

- Archivo ubicado en `datos/productos.json`.
- Admite formatos previos (diccionario código→registro) y el formato nuevo (lista de registros).
- Al iniciar, se carga el contenido y cada registro válido reconstruye un Producto con Producto.from_dict().
- Al modificar productos, se guarda la lista actualizada con json.dump().

Excepciones controladas

- FileNotFoundError: inicio con colección vacía si no existe el archivo.
- json.JSONDecodeError: archivo con JSON inválido es detectado e informado; registros omitidos.
- PermissionError: si no hay permisos para leer/escribir se informa o se propaga según corresponda.
- KeyError / ValueError: registros incompletos o inválidos se omiten sin detener la aplicación.

Instrucciones de ejecución

Abrir terminal en `PARCIAL_2/SEMANA_10/restaurante_app` y ejecutar:

python main.py

Prueba de persistencia

1. Registrar productos desde el menú (opción 1).
2. Salir (opción 12).
3. Ejecutar nuevamente `python main.py` y listar productos (opción 5) — los productos guardados deberían aparecer.
