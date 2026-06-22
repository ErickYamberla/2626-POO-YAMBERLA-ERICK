"""
modelos/cliente.py
Clase Cliente que representa a un cliente del restaurante.
"""

from typing import List, Dict


class Cliente:
    """Representa a un cliente.

    Atributos:
        id (int): Identificador del cliente.
        nombre (str): Nombre completo.
        telefono (str): Teléfono de contacto.
        pedidos (list): Lista de pedidos realizados por el cliente.
    """

    def __init__(self, id: int, nombre: str, telefono: str = ""):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        # cada pedido será un dict con claves: 'productos' (lista de ids), 'total' (float)
        self.pedidos: List[Dict] = []

    def registrar_pedido(self, productos: List[dict], total: float) -> None:
        """Registra un pedido en la lista de pedidos del cliente.

        Args:
            productos: lista de dicts con información mínima de cada producto pedido.
            total: monto total del pedido.
        """
        pedido = {
            "productos": productos,
            "total": float(total)
        }
        self.pedidos.append(pedido)

    def __str__(self) -> str:
        return f"Cliente(id={self.id}, nombre='{self.nombre}', telefono='{self.telefono}')"

    def resumen_pedidos(self) -> str:
        """Devuelve un resumen legible de los pedidos del cliente."""
        if not self.pedidos:
            return f"{self.nombre} no tiene pedidos registrados."
        lines = [f"Pedidos de {self.nombre}:"]
        for i, p in enumerate(self.pedidos, start=1):
            productos_nombres = ", ".join([str(prod.get("nombre", "?")) for prod in p["productos"]])
            lines.append(f"  {i}. Productos: {productos_nombres} | Total: ${p['total']:.2f}")
        return "\n".join(lines)

