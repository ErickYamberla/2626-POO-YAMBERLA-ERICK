"""
Módulo restaurante.py
Contiene la clase Restaurante, encargada de administrar productos del restaurante.
"""

from typing import List
from modelos.producto import Producto


class Restaurante:
    """Servicio que administra una lista de productos registrados."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.productos: List[Producto] = []

    def agregar_producto(self, producto: Producto) -> None:
        """Agrega un producto a la lista. Valida que sea una instancia de Producto."""
        if not isinstance(producto, Producto):
            raise TypeError("Solo se pueden agregar instancias de Producto o sus subclases.")
        self.productos.append(producto)

    def mostrar_productos(self) -> None:
        """Muestra la información de todos los productos registrados (ejemplo de polimorfismo)."""
        print(f"\n--- Productos del restaurante: {self.nombre} ---\n")
        if not self.productos:
            print("No hay productos registrados.")
            return
        for producto in self.productos:
            # Polimorfismo: cada objeto responde a su propia implementación de mostrar_informacion()
            producto.mostrar_informacion()
            print("-------------------------------------")


