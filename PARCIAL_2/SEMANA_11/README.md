# Restaurante App - Semana 11

Estudiante: Erick Yamberla

Este repositorio contiene la evolución de la aplicación restaurante_app para la Semana 11.

Mejoras principales:
- Se agregó el atributo `stock` a Producto y lógica para vender unidades.
- Se creó la entidad Venta que relaciona Usuario y Producto con una cantidad vendida.
- Persistencia ampliada: productos.json, usuarios.json y ventas.json en la carpeta `datos/`.
- Se implementó la operación `vender_producto` en el servicio Restaurante y la consulta de ventas por usuario.
- Manejo de excepciones para archivos faltantes, JSON inválido y permisos.

Estructura del proyecto:
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
└── README.md

Ejecución:
1. Ejecutar `python main.py` desde la carpeta `restaurante_app`.
2. Registrar usuarios y productos (con stock).
3. Usar la opción "Vender producto" para realizar ventas.
4. Consultar ventas por usuario para ver las operaciones registradas.

Pruebas realizadas (breve):
- Registrar usuario y producto, realizar venta y verificar que stock disminuye y que ventas.json contiene el registro.
- Reiniciar la aplicación y verificar que productos, usuarios y ventas se cargan desde JSON.
- Intentar vender más de lo disponible: operación rechazada y datos sin cambios.
