# Sistema básico de gestión de restaurante

- Nombre del estudiante: Erick Santiago Yamberla Inzuasti

Descripción
-----------
Este proyecto muestra un sistema simple para modelar elementos básicos de un restaurante usando Programación Orientada a Objetos en Python. Está pensado como una práctica académica para demostrar:

- Organización del proyecto en módulos y paquetes.
- Separación de responsabilidades entre modelos (entidades) y servicios (lógica de negocio).
- Comunicación entre archivos mediante importaciones.

Ámbito y limitaciones
---------------------
Este proyecto NO incluye:

- Interfaz gráfica o web.
- Persistencia en base de datos (solo memoria en tiempo de ejecución).
- Gestión de concurrencia ni autenticación.

Está pensado para ser ampliado y servir como base para funcionalidades adicionales.

Requisitos cumplidos
---------------------
- Estructura mínima solicitada con `modelos/`, `servicios/` y `main.py`.
- Implementación de al menos dos clases en `modelos` (`Producto`, `Cliente`).
- Implementación de la clase `Restaurante` en `servicios`.
- Uso de constructores `__init__()` y del método especial `__str__()` cuando corresponde.
- Uso de importaciones entre archivos y demostración en `main.py`.

Estructura del proyecto
-----------------------
restaurante_app/
├── modelos/
│   ├── producto.py      # Clase Producto (id, nombre, descripcion, precio, tipo)
│   ├── cliente.py       # Clase Cliente (id, nombre, telefono, pedidos)
│   └── __init__.py
├── servicios/
│   ├── restaurante.py   # Clase Restaurante: agrega/lista productos y clientes, crea pedidos
│   └── __init__.py
└── main.py              # Punto de entrada con demo

Descripción de las clases (resumen técnico)
-------------------------------------------

1) `Producto` (`modelos/producto.py`)
   - Atributos:
	 - `id` (int): identificador único.
	 - `nombre` (str): nombre del producto.
	 - `descripcion` (str): descripción breve.
	 - `precio` (float): precio del producto.
	 - `tipo` (str): categoría (ej. 'plato', 'bebida').
   - Métodos:
	 - `__init__`: constructor.
	 - `__str__`: representación corta.
	 - `info()`: cadena con información detallada.

2) `Cliente` (`modelos/cliente.py`)
   - Atributos:
	 - `id` (int): identificador del cliente.
	 - `nombre` (str): nombre completo.
	 - `telefono` (str): teléfono (opcional).
	 - `pedidos` (list): lista de pedidos realizados; cada pedido es un diccionario con `productos` y `total`.
   - Métodos:
	 - `__init__`: constructor.
	 - `registrar_pedido(productos, total)`: agrega un pedido a la lista interna.
	 - `resumen_pedidos()`: devuelve una cadena legible con los pedidos del cliente.
	 - `__str__`: representación corta.

3) `Restaurante` (`servicios/restaurante.py`)
   - Atributos:
	 - `nombre` (str): nombre del restaurante.
	 - `productos` (list[Producto]): catálogo en memoria.
	 - `clientes` (list[Cliente]): clientes registrados.
   - Métodos principales:
	 - `agregar_producto(producto)` / `agregar_cliente(cliente)`
	 - `listar_productos()` / `listar_clientes()` — imprimen información en consola.
	 - `buscar_producto_por_id(id)` / `buscar_cliente_por_id(id)`
	 - `crear_pedido(cliente_id, productos_ids)` — construye y registra un pedido para un cliente dado.

Ejemplo de uso (resumen de `main.py`)
-----------------------------------
El archivo `main.py` crea instancias de `Producto` y `Cliente`, las registra en un `Restaurante` y crea pedidos de ejemplo. Ejecución típica:

```powershell
cd "C:\Users\USER\PycharmProjects\2626-POO-YAMBERLA-ERICK\PARCIAL_1\SEMANA_4\restaurante_app"
python .\main.py
```

Salida esperada (ejemplo resumido):

- Lista de productos con su información.
- Lista de clientes registrados.
- Mensajes al registrar pedidos (incluye advertencia si se referencia un producto inexistente).
- Resumen de pedidos por cliente mostrando productos y totales.

Ejemplo de fragmento de salida:

```
Productos en La Esquina Del Sabor:
 - Lomo Saltado (plato) - Plato típico con carne y papas : $22.50
 - Ceviche (plato) - Ceviche de pescado fresco : $18.00
 - Inca Kola (bebida) - Bebida gaseosa 500ml : $3.50
 - Café (bebida) - Café de la casa : $2.50

Clientes registrados en La Esquina Del Sabor:
 - Cliente(id=1, nombre='Ana Pérez', telefono='+51 987654321')
 - Cliente(id=2, nombre='Carlos Soto', telefono='+51 912345678')

-- Creando pedidos de ejemplo --
Pedido registrado para Ana Pérez. Total: $26.00
Advertencia: producto con id=99 no encontrado — se omite.
Pedido registrado para Carlos Soto. Total: $20.50

-- Resumen de pedidos --
Pedidos de Ana Pérez:
  1. Productos: Lomo Saltado, Inca Kola | Total: $26.00

Pedidos de Carlos Soto:
  1. Productos: Ceviche, Café | Total: $20.50
```

Buenas prácticas y posibles extensiones
--------------------------------------
- Persistencia: guardar y cargar productos/clientes/pedidos en JSON o una base de datos.
- Validaciones: evitar ids duplicados, validar precios negativos, sanitizar entradas.
- Tests: añadir pruebas unitarias (pytest) para las clases y servicios.
- Interfaz: implementar una CLI interactiva o una API web (Flask/FastAPI) para exponer las operaciones.

Reflexión sobre modularidad
--------------------------------------
La separación entre `modelos` y `servicios` facilita:

- Reutilización: las clases de dominio pueden reutilizarse en diferentes interfaces (CLI, web, tests).
- Mantenibilidad: los cambios en la lógica de negocio no requieren tocar la definición de las entidades y viceversa.
- Pruebas: permite probar la lógica de negocio aislada creando mocks de las entidades si es necesario.

Contacto / Autor
----------------
Proyecto creado como práctica académica por Erick Santiago Yamberla Inzuasti.
