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
