"""Modelo Cliente usando @dataclass."""

from dataclasses import dataclass


@dataclass
class Cliente:
    """Clase de datos para representar un cliente.

    Atributos: nombre, correo, id_cliente
    """

    nombre: str
    correo: str
    id_cliente: str

    def __repr__(self) -> str:
        return f"Cliente(nombre={self.nombre!r}, correo={self.correo!r}, id_cliente={self.id_cliente!r})"

