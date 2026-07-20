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


