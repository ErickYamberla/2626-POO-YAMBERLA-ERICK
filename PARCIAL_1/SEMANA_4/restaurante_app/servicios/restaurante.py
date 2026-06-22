"""
servicios/restaurante.py
Clase Restaurante que administra productos y clientes y permite crear pedidos.
"""

from typing import List, Optional
from modelos.producto import Producto
from modelos.cliente import Cliente


class Restaurante:
    """Servicio principal que mantiene listas de productos y clientes.

    Métodos principales:
        agregar_producto, agregar_cliente, listar_productos, listar_clientes,
        buscar_producto_por_id, crear_pedido
    """

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.productos: List[Producto] = []
        self.clientes: List[Cliente] = []

    def agregar_producto(self, producto: Producto) -> None:
        self.productos.append(producto)

    def agregar_cliente(self, cliente: Cliente) -> None:
        self.clientes.append(cliente)

    def listar_productos(self) -> None:
        print(f"\nProductos en {self.nombre}:")
        for p in self.productos:
            print(" -", p.info())

    def listar_clientes(self) -> None:
        print(f"\nClientes registrados en {self.nombre}:")
        for c in self.clientes:
            print(" -", c)

    def buscar_producto_por_id(self, id: int) -> Optional[Producto]:
        for p in self.productos:
            if p.id == id:
                return p
        return None

    def buscar_cliente_por_id(self, id: int) -> Optional[Cliente]:
        for c in self.clientes:
            if c.id == id:
                return c
        return None

    def crear_pedido(self, cliente_id: int, productos_ids: List[int]) -> Optional[float]:
        """Crea un pedido para un cliente sumando los precios de los productos indicados.

        Registra el pedido en el cliente y devuelve el total. Si cliente o producto no existen,
        devuelve None.
        """
        cliente = self.buscar_cliente_por_id(cliente_id)
        if cliente is None:
            print(f"Cliente con id={cliente_id} no encontrado.")
            return None

        productos_en_pedido = []
        total = 0.0
        for pid in productos_ids:
            prod = self.buscar_producto_por_id(pid)
            if prod is None:
                print(f"Advertencia: producto con id={pid} no encontrado — se omite.")
                continue
            productos_en_pedido.append({"id": prod.id, "nombre": prod.nombre, "precio": prod.precio})
            total += prod.precio

        if not productos_en_pedido:
            print("No se agregaron productos válidos al pedido; no se registrará.")
            return None

        cliente.registrar_pedido(productos_en_pedido, total)
        print(f"Pedido registrado para {cliente.nombre}. Total: ${total:.2f}")
        return total

