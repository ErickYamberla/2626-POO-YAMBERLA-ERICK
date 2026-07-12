# Sistema de Restaurante (Semana 7)

Nombre del estudiante: [Erick Santiago Yamberla Inzuasti]

Descripción
-----------
Proyecto didáctico que implementa un sistema básico de gestión de un restaurante aplicando conceptos de Programación Orientada a Objetos: uso de constructores, decoradores @property y @setter, @dataclass y arquitectura modular por capas.

Estructura del proyecto
-----------------------
SEMANA_7/
├── restaurante_app/
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── producto.py    # Clase Producto con constructor y @property/@setter
│   │   └── cliente.py     # Clase Cliente implementada con @dataclass
│   ├── servicios/
│   │   ├── __init__.py
│   │   └── restaurante.py # Clase Restaurante que administra listas y operaciones
│   └── main.py            # Menú interactivo y punto de entrada
└── README.md

Principales decisiones de diseño
-------------------------------
- La clase `Producto` utiliza un constructor tradicional (`__init__`) y propiedades para encapsular y validar los atributos `nombre`, `categoria`, `precio` y `disponible`.
- La clase `Cliente` fue implementada con `@dataclass` para simplificar la definición de datos.
- La clase `Restaurante` (en `servicios/restaurante.py`) administra las listas de productos y clientes y provee métodos para registrar, listar y buscar.
- Se agregó carga de datos de ejemplo en el constructor de `Restaurante` para facilitar pruebas y demostraciones didácticas.

Ejecución
---------
1. Abrir una terminal en la carpeta `SEMANA_7/restaurante_app`.
2. Ejecutar:

```powershell
python main.py
```

Uso del constructor en `Producto`
--------------------------------
El constructor tradicional `__init__` recibe `nombre`, `categoria`, `precio` y `disponible`. Para establecer los valores se reutilizan los setters (`self.nombre = nombre`) de modo que las validaciones se apliquen al crear el objeto.

Uso de @property y @setter
--------------------------
Se empleó `@property` para exponer los atributos de `Producto` de forma controlada y `@setter` para validar datos: nombre y categoría no vacíos, precio numérico mayor que cero.

Uso de @dataclass
-----------------
La clase `Cliente` utiliza `@dataclass` para definir rápidamente una clase de datos con atributos `nombre`, `correo` e `id_cliente`.

Menú interactivo
----------------
El archivo `main.py` presenta un menú con las opciones solicitadas: registrar, listar y buscar productos y clientes. Los objetos se crean con los datos ingresados por el usuario mediante `input()` y se registran en la clase `Restaurante`.

Reflexión
---------
Crear objetos a partir de datos ingresados por el usuario demuestra cómo las clases y sus constructores pasan de ser plantillas a instancias útiles en tiempo de ejecución. El uso de propiedades y validaciones ayuda a mantener la integridad de los datos y mejora la mantenibilidad del código.
