from typing import List
from modelos.producto import Producto
from modelos.cliente import Cliente


class Restaurante:
    """Servicio que administra productos y clientes."""

    def __init__(self) -> None:
        self._productos: List[Producto] = []
        self._clientes: List[Cliente] = []

    # Métodos para productos
    def registrar_producto(self, producto: Producto) -> bool:
        """Registra un producto si su código no existe. Devuelve True si se registró."""
        if self._existe_codigo_producto(producto.codigo):
            return False
        self._productos.append(producto)
        return True

    def _existe_codigo_producto(self, codigo: str) -> bool:
        return any(p.codigo == codigo for p in self._productos)

    def listar_productos(self) -> List[str]:
        """Retorna una lista con las representaciones de cada producto usando polimorfismo."""
        return [p.mostrar_informacion() for p in self._productos]

    # Métodos para clientes
    def registrar_cliente(self, cliente: Cliente) -> bool:
        """Registra un cliente si su identificación no existe. Devuelve True si se registró."""
        if self._existe_identificacion_cliente(cliente.identificacion):
            return False
        self._clientes.append(cliente)
        return True

    def _existe_identificacion_cliente(self, identificacion: str) -> bool:
        return any(c.identificacion == identificacion for c in self._clientes)

    def listar_clientes(self) -> List[str]:
        return [c.mostrar_informacion() for c in self._clientes]


