"""Modelo Cliente

Define la clase Cliente que representa a una persona registrada en el
sistema del restaurante.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Cliente:
    """Representa un cliente del restaurante.

    Atributos:
        id_cliente: int - identificador único del cliente
        nombre: str - nombre completo del cliente
        telefono: str - contacto telefónico
        correo: str - dirección de correo electrónico
        puntos_fidelidad: int - puntos acumulados en el programa de fidelidad
        activo: bool - indica si el cliente está activo en el sistema
    """

    id_cliente: int
    nombre: str
    telefono: str
    correo: str
    puntos_fidelidad: int = 0
    activo: bool = True

    def __str__(self) -> str:
        """Representación en texto del cliente."""
        estado = "Activo" if self.activo else "Inactivo"
        return (
            f"Cliente #{self.id_cliente}: {self.nombre} | Tel: {self.telefono} | "
            f"Correo: {self.correo} | Puntos: {self.puntos_fidelidad} | {estado}"
        )

