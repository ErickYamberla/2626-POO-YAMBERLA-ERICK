# Restaurante App - Semana 6

Estudiante: Erick Santiago Yamberla Inzuasti

Objetivo
--------------
Esta pequeña aplicación sirve como ejercicio práctico para aprender y aplicar los tres pilares fundamentales de la Programación Orientada a Objetos (POO): herencia, encapsulamiento y polimorfismo. Modela productos de un restaurante (platillos y bebidas) usando una estructura modular en Python.

Técnicas
-------------------------------------
A continuación se explica cada técnica con ejemplos de alto nivel tomadas del código de este proyecto.

1) Herencia
-----------
- ¿Qué es? La herencia permite definir una clase general (la clase padre) con atributos y comportamientos comunes, y crear clases más específicas (clases hijas) que heredan todo lo común y añaden lo propio.
- ¿Por qué usarla aquí? En el restaurante hay muchos productos que comparten información (por ejemplo, nombre, precio y disponibilidad). Crear una clase `Producto` evita repetir esa información en `Platillo` y `Bebida`.
- ¿Cómo se implementó? En `modelos/producto.py` se define la clase `Producto`. `Platillo` y `Bebida` (en `modelos/platillo.py` y `modelos/bebida.py`) hacen `class Platillo(Producto):` y `class Bebida(Producto):` y llaman a `super().__init__(...)` para reutilizar la inicialización de la clase padre.

Ejemplo conceptual (resumen):
- Clase padre: Producto(nombre, precio, disponible)
- Clase hija Platillo: añade calorias, tipo y tiempo_preparacion
- Clase hija Bebida: añade volumen_ml, tamano y tipo_bebida

Beneficios:
- Reutilización de código: evita duplicar atributos y métodos.
- Organización: agrupa comportamientos comunes y mantiene el código más claro.

2) Encapsulamiento
-------------------
- ¿Qué es? El encapsulamiento consiste en ocultar los detalles internos de una clase (datos y/o lógica) y exponer únicamente lo necesario mediante métodos públicos.
- ¿Por qué es importante? Protege el estado del objeto para que no quede inconsistente por cambios directos desde fuera. También permite controlar y validar cambios.
- ¿Cómo se implementó? En `Producto` el atributo `precio` está encapsulado como `__precio` (nombre con doble guion bajo). El acceso se hace con `obtener_precio()` y la modificación con `cambiar_precio(nuevo_precio)`. El setter valida que el precio sea mayor que cero; si no, lanza `ValueError`.

Ejemplo de uso seguro:
- Para leer el precio: `producto.obtener_precio()`
- Para cambiarlo: `producto.cambiar_precio(30.0)` (si se intenta `producto.__precio = -5` no se deberá modificar desde fuera)

Por qué esto te ayuda como principiante:
- Aprender a proteger los datos evita errores difíciles de encontrar.
- Te obliga a pensar en reglas de negocio (por ejemplo: un precio no puede ser negativo) y centralizarlas en la clase.

3) Polimorfismo
---------------
- ¿Qué es? Polimorfismo significa "muchas formas": el mismo método (mismo nombre) puede comportarse de forma diferente según el tipo del objeto que lo implemente.
- ¿Por qué usarlo? Permite tratar objetos diferentes de forma uniforme: por ejemplo, una lista de productos puede recorrerlos y llamar al mismo método `mostrar_informacion()` y cada objeto mostrará los datos que le corresponden.
- ¿Cómo se implementó? `Producto` define un método `mostrar_informacion()` genérico. `Platillo` y `Bebida` sobrescriben (override) este método para mostrar atributos propios. En `servicios/restaurante.py`, `mostrar_productos()` recorre la lista `self.productos` y llama `producto.mostrar_informacion()` sin tener que preguntar de qué tipo es cada producto.

Beneficio práctico:
- Facilita añadir nuevos tipos de productos en el futuro (por ejemplo, `Postre` o `Promocion`) sin cambiar la lógica que administra la lista de productos.

Estructura del proyecto (resumen)
--------------------------------
restaurante_app/
- modelos/
  - __init__.py
  - producto.py     # clase Producto con atributo encapsulado y métodos getter/setter
  - platillo.py     # clase Platillo que hereda de Producto
  - bebida.py       # clase Bebida que hereda de Producto
- servicios/
  - __init__.py
  - restaurante.py  # clase Restaurante que administra la lista de productos
- main.py           # punto de entrada que crea objetos y muestra la información

Cómo ejecutar (PowerShell)
--------------------------
Desde la carpeta `restaurante_app`:

```powershell
cd "C:\Users\USER\PycharmProjects\2626-POO-YAMBERLA-ERICK\PARCIAL_1\SEMANA_6\restaurante_app"
python main.py
```

Salida esperada
------------------------
Verás en consola una lista de productos. Cada `Platillo` mostrará su tipo, calorías, tiempo de preparación y precio. Cada `Bebida` mostrará tipo, tamaño, volumen y precio. Esto demuestra que el mismo método (`mostrar_informacion`) se comporta según la clase del objeto.

Reflexión final
----------------------------------
Entender POO es aprender a modelar problemas reales como objetos que tienen estado y comportamiento. La herencia te ayuda a organizar y reutilizar; el encapsulamiento te permite proteger reglas de negocio; y el polimorfismo hace tu código más flexible y extensible. Este proyecto es un ejercicio concreto donde puedes practicar estas ideas y experimentar con pequeñas extensiones.
