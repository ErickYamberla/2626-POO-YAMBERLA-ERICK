"""Modelo Producto

Define la clase Producto que representa un plato, bebida o producto
disponible en el restaurante.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Producto:
    """Representa un producto del restaurante.

    Atributos:
        codigo: int - identificador numérico del producto
        nombre: str - nombre descriptivo del producto
        descripcion: str - descripción breve del producto
        precio: float - precio del producto en moneda local
        disponible: bool - indica si el producto está disponible
    """

    codigo: int
    nombre: str
    descripcion: str
    precio: float
    disponible: bool = True

    def __str__(self) -> str:
        """Representación en texto del producto."""
        estado = "Disponible" if self.disponible else "No disponible"
        return (
            f"Producto #{self.codigo}: {self.nombre} - {self.descripcion} | "
            f"Precio: ${self.precio:.2f} | {estado}"
        )

