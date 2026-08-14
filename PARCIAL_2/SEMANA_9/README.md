Proyecto: PARCIAL_2 - Semana 9

Descripción:
Sistema de restaurante que permite registrar, buscar, actualizar, eliminar y listar
productos; además registra y lista clientes. Los datos se archivan en archivos JSON
como diccionarios para persistencia entre ejecuciones.

Estructura:
- modelos/: clases Producto, Bebida (opcional) y Usuario
- servicios/: Restaurante que gestiona colecciones y archivos JSON (data/)
- main.py: menú interactivo que usa el servicio; no manipula internamente las colecciones

Características implementadas:
- Persistencia en JSON (productos.json y clientes.json en la carpeta data/)
- Evita códigos/identificaciones duplicadas
- Búsqueda, actualización y eliminación de productos
- Búsqueda, actualización y eliminación de clientes
- Listado de productos y clientes
- Muestra categorías únicas de productos (utiliza conjunto)
- Uso de tupla para información estable del sistema
- Validaciones básicas de entrada y manejo de excepciones

Menú principal (resumen):
1. Registrar producto
2. Buscar producto
3. Actualizar producto
4. Eliminar producto
5. Listar productos
6. Registrar cliente
7. Buscar cliente
8. Actualizar cliente
9. Eliminar cliente
10. Listar clientes
11. Mostrar categorías
12. Salir

Notas:
- Los datos se guardan en PARCIAL_2\SEMANA_9\restaurante_app\data
- main.py solicita entradas y delega operaciones al servicio Restaurante
- No modifique manualmente los archivos JSON salvo para pruebas controladas

Cómo ejecutar:
1. Abrir consola en PARCIAL_2\SEMANA_9\restaurante_app
2. Ejecutar: python main.py
3. Seguir el menú interactivo

Autor: Erick Yamberla
