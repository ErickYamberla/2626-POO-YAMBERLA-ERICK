"""Servicio que gestiona productos y clientes del restaurante.

Contiene métodos para agregar, listar y buscar objetos en las listas
internas. Utiliza listas como tipo compuesto para almacenar múltiples
objetos.
"""
from __future__ import annotations
from typing import List, Optional

# Importaciones locales para ejecutar el paquete como script desde la carpeta
from modelos.producto import Producto
from modelos.cliente import Cliente


class RestauranteService:
    """Servicio principal para la gestión básica del restaurante."""

    def __init__(self) -> None:
        # Listas que almacenan objetos Producto y Cliente
        self.productos: List[Producto] = []
        self.clientes: List[Cliente] = []

    def agregar_producto(self, producto: Producto) -> None:
        """Agrega un producto a la lista de productos si no existe el código."""
        if any(p.codigo == producto.codigo for p in self.productos):
            raise ValueError(f"Ya existe un producto con código {producto.codigo}")
        self.productos.append(producto)

    def agregar_cliente(self, cliente: Cliente) -> None:
        """Agrega un cliente a la lista de clientes si no existe el id."""
        if any(c.id_cliente == cliente.id_cliente for c in self.clientes):
            raise ValueError(f"Ya existe un cliente con id {cliente.id_cliente}")
        self.clientes.append(cliente)

    def listar_productos(self) -> List[str]:
        """Devuelve la representación en texto de todos los productos."""
        return [str(p) for p in self.productos]

    def listar_clientes(self) -> List[str]:
        """Devuelve la representación en texto de todos los clientes."""
        return [str(c) for c in self.clientes]

    def buscar_producto_por_codigo(self, codigo: int) -> Optional[Producto]:
        """Busca y retorna un producto por su código o None si no existe."""
        for producto in self.productos:
            if producto.codigo == codigo:
                return producto
        return None

    def buscar_cliente_por_id(self, id_cliente: int) -> Optional[Cliente]:
        """Busca y retorna un cliente por su id o None si no existe."""
        for cliente in self.clientes:
            if cliente.id_cliente == id_cliente:
                return cliente
        return None

    def eliminar_producto_por_codigo(self, codigo: int) -> bool:
        """Elimina un producto por código. Retorna True si se eliminó."""
        producto = self.buscar_producto_por_codigo(codigo)
        if producto:
            self.productos.remove(producto)
            return True
        return False

    def actualizar_precio(self, codigo: int, nuevo_precio: float) -> bool:
        """Actualiza el precio de un producto identificado por su código."""
        producto = self.buscar_producto_por_codigo(codigo)
        if producto:
            producto.precio = float(nuevo_precio)
            return True
        return False



