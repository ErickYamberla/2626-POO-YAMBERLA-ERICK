"""Modelo Producto.

Implementa constructor tradicional, @property y @setter con validaciones básicas.
"""

from typing import Any


class Producto:
    """Representa un producto del restaurante.

    Atributos principales: nombre, categoria, precio, disponible.
    Se usan propiedades para controlar acceso y validaciones.
    """

    def __init__(self, nombre: str, categoria: str, precio: float, disponible: bool = True) -> None:
        # atributos internos con guion bajo
        self._nombre: str | None = None
        self._categoria: str | None = None
        self._precio: float | None = None
        self._disponible: bool = bool(disponible)

        # usar setters para validar
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio

    # nombre
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    # categoria
    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La categoría del producto no puede estar vacía.")
        self._categoria = valor.strip()

    # precio
    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: Any) -> None:
        try:
            numero = float(valor)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un número válido mayor que cero.")
        if numero <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
        self._precio = numero

    # disponible
    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: Any) -> None:
        self._disponible = bool(valor)

    def mostrar_informacion(self) -> str:
        """Devuelve una cadena con la información del producto en formato legible."""
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Producto: {self.nombre} | Categoría: {self.categoria} | Precio: S/{self.precio:.2f} | {estado}"

    def __repr__(self) -> str:
        return f"<Producto nombre={self._nombre!r} categoria={self._categoria!r} precio={self._precio!r} disponible={self._disponible!r}>"

