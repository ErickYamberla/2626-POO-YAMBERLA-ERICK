"""
Punto de entrada del programa que demuestra el funcionamiento del sistema básico de restaurante.
"""

from modelos.producto import Producto
from modelos.cliente import Cliente
from servicios.restaurante import Restaurante


def main():
    # Crear servicio principal
    r = Restaurante("La Esquina Del Sabor")

    # Crear algunos productos (id, nombre, descripcion, precio, tipo)
    p1 = Producto(1, "Lomo Saltado", "Plato típico con carne y papas", 22.50, "plato")
    p2 = Producto(2, "Ceviche", "Ceviche de pescado fresco", 18.00, "plato")
    p3 = Producto(3, "Inca Kola", "Bebida gaseosa 500ml", 3.50, "bebida")
    p4 = Producto(4, "Café", "Café de la casa", 2.50, "bebida")

    # Agregar productos al restaurante
    r.agregar_producto(p1)
    r.agregar_producto(p2)
    r.agregar_producto(p3)
    r.agregar_producto(p4)

    # Crear clientes
    c1 = Cliente(1, "Ana Pérez", "+51 987654321")
    c2 = Cliente(2, "Carlos Soto", "+51 912345678")

    # Agregar clientes al restaurante
    r.agregar_cliente(c1)
    r.agregar_cliente(c2)

    # Mostrar información registrada
    r.listar_productos()
    r.listar_clientes()

    # Crear pedidos
    print("\n-- Creando pedidos de ejemplo --")
    r.crear_pedido(cliente_id=1, productos_ids=[1, 3])  # Ana pide Lomo + Inca Kola
    r.crear_pedido(cliente_id=2, productos_ids=[2, 4, 99])  # Carlos pide Ceviche + Café (99 no existe)

    # Mostrar resumen de pedidos por cliente
    print("\n-- Resumen de pedidos --")
    print(c1.resumen_pedidos())
    print()
    print(c2.resumen_pedidos())


if __name__ == "__main__":
    main()

