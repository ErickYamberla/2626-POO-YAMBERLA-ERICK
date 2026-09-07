# 2626-POO-YAMBERLA-ERICK

Nombre del estudiante: Erick Santiago Yamberla Inzuasti

Descripción de los programas desarrollados:

- Programación Tradicional (`PARCIAL_1/SEMANA_3/programacion_tradicional/tradicional.py`):
  - Implementación basada en variables y funciones.
  - Permite registrar una o varias mascotas solicitando datos por teclado
	(nombre, especie, edad, color, dueño), valida la edad y muestra un
	resumen organizado de los registros.

- Programación Orientada a Objetos (`PARCIAL_1/SEMANA_3/programacion_poo/`):
  - Implementa la clase `Mascota` en `mascota.py` con atributos `nombre`,
	`especie` y `edad` y los métodos `mostrar_informacion()` y `hacer_sonido()`.
  - `main.py` crea varias instancias de `Mascota` y demuestra el uso de los
	métodos para mostrar información y comportamientos (sonidos).

Reflexión sobre diferencias entre Programación Tradicional y Programación
Orientada a Objetos:

- Abstracción y modelado: En la programación tradicional organizamos la
  información y el comportamiento mediante variables y funciones. En OOP
  agrupamos datos y comportamiento relacionados dentro de clases, lo que
  facilita modelar entidades del mundo real (por ejemplo, una mascota).

- Encapsulación y organización: OOP permite encapsular atributos y métodos
  en objetos, mejorando la organización del código y reduciendo la
  probabilidad de efectos secundarios inesperados. En programación
  tradicional, el estado suele ser manejado por variables globales o
  pasadas entre funciones.

- Reutilización y extensión: Las clases facilitan la reutilización y la
  extensión (herencia y composición). Para proyectos pequeños la
  aproximación procedural puede ser más simple, pero para sistemas más
  grandes OOP suele facilitar el mantenimiento.

- Curva de aprendizaje y sobrecarga: OOP añade conceptos extra (clases,
  objetos, métodos) que pueden parecer más complejos al inicio. Para
  tareas sencillas, el enfoque tradicional es directo y rápido de
  implementar.

- Elección práctica: No hay una única respuesta correcta — elegir entre
  procedural y OOP depende del problema, la escala y las necesidades de
  mantenimiento. En este proyecto se implementaron ambas versiones para
  comparar y aprender las diferencias.

Ejecución rápida:

 - Ejecutar el programa tradicional:
```powershell
python .\PARCIAL_1\SEMANA_3\programacion_tradicional\tradicional.py
```

 - Ejecutar la versión orientada a objetos:
```powershell
python .\PARCIAL_1\SEMANA_3\programacion_poo\main.py
```

---

## Semana 8 - proyecto `restaurante_app`

Nombre del estudiante: Erick Santiago Yamberla Inzuasti

Descripción:

Este proyecto implementa un sistema básico de gestión de un restaurante que permite registrar y listar productos, bebidas y clientes. Está diseñado para evidenciar los principios SOLID (SRP, OCP y LSP) aplicados al modelado orientado a objetos.

Estructura del proyecto (dentro de `PARCIAL_1/SEMANA_8`):

```
restaurante_app/
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── bebida.py
│   └── cliente.py
├── servicios/
│   ├── __init__.py
│   └── restaurante.py
└── main.py
```

Responsabilidad de las clases:

- `Producto` (`modelos/producto.py`): datos comunes de un producto y método `mostrar_informacion()`.
- `Bebida` (`modelos/bebida.py`): hereda de `Producto`, añade atributos como `tamano` y `presentacion`, sobrescribe `mostrar_informacion()`.
- `Cliente` (`modelos/cliente.py`): modela la información de un cliente y su método `mostrar_informacion()`.
- `Restaurante` (`servicios/restaurante.py`): servicio que administra el registro y listado de productos y clientes, valida duplicados y usa polimorfismo para listar productos.

Relación entre `Producto` y `Bebida`:

`Bebida` es una especialización de `Producto`. Se utiliza herencia porque una bebida es un tipo de producto; al sobrescribir `mostrar_informacion()` la bebida puede presentarse con información adicional, y `Restaurante` puede manejar ambos tipos en la misma colección sin conocer el tipo concreto.

Principios aplicados:

- SRP (Single Responsibility Principle): cada clase tiene una única responsabilidad clara.
- OCP (Open/Closed Principle): `Bebida` extiende `Producto` sin modificar la lógica del servicio.
- LSP (Liskov Substitution Principle): instancias de `Bebida` pueden usarse donde se espera un `Producto`.

Ejecución:

Abrir la terminal en la raíz del repositorio y ejecutar:

```powershell
python .\PARCIAL_1\SEMANA_8\restaurante_app\main.py
```

Reflexión breve:

Diseñar módulos con responsabilidades claras facilita el mantenimiento y la extensión del sistema. Aplicando SOLID conseguimos que agregar nuevas funcionalidades (por ejemplo, un nuevo tipo de producto) requiera cambios mínimos y localizados.



## Semana 10 - persistencia de productos (restaurante_app)

Nombre del estudiante: Erick Santiago Yamberla Inzuasti

Descripción:
Este hito añade persistencia de productos en formato JSON al proyecto restaurante_app. Los productos se guardan en datos/productos.json y se cargan al iniciar la aplicación, reconstruyendo objetos Producto para mantener la lógica orientada a objetos.

Estructura (extra añadida):
`
restaurante_app/
├── datos/
│   └── productos.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── cliente.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
├── main.py
└── README.md
` 

Responsabilidades:
- modelos/producto.py: clase Producto con validaciones, to_dict() y from_dict().
- servicios/archivo_servicio.py: lectura y escritura de productos.json (with open, json.load, json.dump) y manejo de excepciones.
- servicios/restaurante.py: administra colección de objetos Producto en memoria y solicita guardado/recuperación al ArchivoServicio.
- main.py: coordina el flujo y utiliza el servicio Restaurante.

Flujo de carga y guardado:
- Al iniciar: main crea Restaurante → Restaurante utiliza ArchivoServicio.cargar_productos() → cada registro válido se convierte en Producto y se incorpora a la colección en memoria.
- Al modificar productos: Restaurante actualiza la colección en memoria y llama ArchivoServicio.guardar_productos() con la lista de diccionarios.

Excepciones controladas:
- FileNotFoundError: ausencia inicial de productos.json se trata como colección vacía.
- json.JSONDecodeError: archivo con formato inválido se detecta y se omiten registros corruptos (se muestra mensaje).
- PermissionError: se informa si no hay permisos para leer o escribir.
- KeyError / ValueError: registros incompletos o inválidos se omiten y no detienen la aplicación.

Ejecución:
Abrir terminal en PARCIAL_2/SEMANA_10/restaurante_app y ejecutar:
`
python main.py
` 


Comprobación de persistencia:
1. Registrar uno o más productos desde el menú.
2. Salir de la aplicación.
3. Ejecutar nuevamente python main.py — los productos previamente registrados deben listarse automáticamente.

---

## Semana 12 - mejoras de rendimiento con colecciones

Descripción:
En la Semana 12 se mejoró la forma en que la aplicación busca, consulta y valida información utilizando colecciones auxiliares en memoria, manteniendo las colecciones principales para almacenamiento y persistencia.

Mejoras implementadas:
- Índices en memoria:
  - Productos y usuarios se almacenan en diccionarios internos indexados por código de producto e identificación de usuario, permitiendo búsquedas O(1) mediante buscar_producto(codigo) y buscar_usuario(identificacion).
  - Se añadió un índice auxiliar `_ventas_por_usuario` (dict) que mapea `identificacion_usuario` → lista de `Venta`. La consulta `ventas_por_usuario(identificacion)` utiliza este índice en lugar de recorrer cada vez la lista completa de ventas.
- Mantenimiento de colecciones:
  - Se mantuvieron las listas principales (`_productos`, `_usuarios`, `_ventas`) para recorrido y persistencia en JSON.
  - Al registrar una venta se actualizan ambas estructuras (lista principal e índice auxiliar). En caso de fallo, la operación revierte ambos.
  - Los índices se reconstruyen al iniciar la aplicación a partir de los objetos cargados desde JSON.
- Uso de `set`:
  - Se utiliza `set` sólo cuando aporta unicidad o validaciones de pertenencia (por ejemplo, para mostrar categorías únicas).

Cómo probar las mejoras:
1. Ejecutar desde la carpeta del proyecto Semana_12:

```powershell
python .\PARCIAL_2\SEMANA_12\restaurante_app\main.py
```
2. Registrar o cargar usuarios, productos y ventas existentes.
3. Buscar un producto por código (buscar_producto) y un usuario por identificación (buscar_usuario).
4. Consultar ventas por usuario: `ventas_por_usuario(identificacion)` debe devolver las ventas sin recorrer la colección completa de ventas.
5. Registrar una venta válida y comprobar que el stock se actualiza y que `_ventas_por_usuario` contiene la nueva venta.
6. Cerrar y volver a ejecutar la aplicación para verificar que los índices se reconstruyen correctamente desde los archivos JSON.

Notas:
- No se añadieron funcionalidades nuevas fuera del alcance (préstamos, facturación, proveedores, etc.).
- La lógica de negocio permanece en `servicios/restaurante.py` y los modelos siguen siendo objetos.
- README en `PARCIAL_2/SEMANA_12/restaurante_app/README.md` contiene un resumen de las mejoras y pruebas realizadas.
