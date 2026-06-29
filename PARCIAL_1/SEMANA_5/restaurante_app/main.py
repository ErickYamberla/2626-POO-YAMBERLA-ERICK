"""Punto de arranque del sistema de gestión del restaurante.

En este archivo se crean objetos de Producto y Cliente, se agregan al
servicio principal y se muestra la información registrada en consola.
"""
# Importaciones adaptadas para ejecutar el script desde la carpeta `restaurante_app`
# Se usan rutas relativas al paquete local cuando sea posible.
from modelos.producto import Producto
from modelos.cliente import Cliente
from servicios.restaurante import RestauranteService


def main() -> None:
    # Crear el servicio principal
    servicio = RestauranteService()

    # Crear productos (al menos dos)
    producto1 = Producto(
        codigo=101,
        nombre="Ceviche de la casa",
        descripcion="Porción tradicional con limón y cilantro",
        precio=12.50,
        disponible=True,
    )

    producto2 = Producto(
        codigo=102,
        nombre="Limonada natural",
        descripcion="Limonada fresca sin azúcar añadida",
        precio=3.00,
        disponible=True,
    )

    # Crear clientes (al menos dos)
    cliente1 = Cliente(
        id_cliente=1,
        nombre="Ana Gómez",
        telefono="555-1234",
        correo="ana.gomez@example.com",
        puntos_fidelidad=120,
        activo=True,
    )

    cliente2 = Cliente(
        id_cliente=2,
        nombre="Carlos Pérez",
        telefono="555-5678",
        correo="c.perez@example.com",
        puntos_fidelidad=45,
        activo=True,
    )

    # Agregar objetos al servicio
    servicio.agregar_producto(producto1)
    servicio.agregar_producto(producto2)

    servicio.agregar_cliente(cliente1)
    servicio.agregar_cliente(cliente2)

    # Mostrar información registrada de forma organizada
    print("--- Productos registrados ---")
    for texto in servicio.listar_productos():
        print(texto)

    print("\n--- Clientes registrados ---")
    for texto in servicio.listar_clientes():
        print(texto)

    # Ejemplos de uso de métodos adicionales
    print("\nBuscando producto con código 101:")
    encontrado = servicio.buscar_producto_por_codigo(101)
    print(encontrado if encontrado else "No encontrado")

    print("\nActualizando precio del producto 102 a $3.50...")
    servicio.actualizar_precio(102, 3.5)
    print(servicio.buscar_producto_por_codigo(102))


if __name__ == "__main__":
    main()


