"""Servicio Restaurante: administra productos y clientes."""

from modelos.producto import Producto
from modelos.cliente import Cliente
from typing import List


class Restaurante:
    """Clase de servicio que administra productos y clientes.

    Contiene métodos para registrar, listar y buscar elementos.
    Se cargan datos de ejemplo en el constructor para facilitar pruebas didácticas.
    """

    def __init__(self) -> None:
        self.productos: List[Producto] = []
        self.clientes: List[Cliente] = []
        # Cargar datos de ejemplo
        self._cargar_ejemplo()

    def _cargar_ejemplo(self) -> None:
        # Productos de ejemplo
        try:
            p1 = Producto("Lomo saltado", "Plato fuerte", 25.0, True)
            p2 = Producto("Ceviche", "Entrada", 18.5, True)
            p3 = Producto("Chicha morada", "Bebida", 6.0, True)
            self.registrar_producto(p1)
            self.registrar_producto(p2)
            self.registrar_producto(p3)
        except Exception:
            # si hay problemas con los ejemplos, se ignoran para no romper la inicialización
            pass

        # Clientes de ejemplo
        c1 = Cliente(nombre="Ana Pérez", correo="ana.perez@example.com", id_cliente="C001")
        c2 = Cliente(nombre="Luis Gómez", correo="luis.gomez@example.com", id_cliente="C002")
        self.registrar_cliente(c1)
        self.registrar_cliente(c2)

    # Métodos para productos
    def registrar_producto(self, producto: Producto) -> None:
        """Registra un producto si no existe otro con el mismo nombre (insensible a mayúsculas)."""
        if any(p.nombre.lower() == producto.nombre.lower() for p in self.productos):
            raise ValueError(f"Ya existe un producto con el nombre '{producto.nombre}'.")
        self.productos.append(producto)

    def listar_productos(self) -> List[Producto]:
        return list(self.productos)

    def buscar_producto(self, nombre: str) -> List[Producto]:
        nombre = nombre.strip().lower()
        return [p for p in self.productos if nombre in p.nombre.lower()]

    # Métodos para clientes
    def registrar_cliente(self, cliente: Cliente) -> None:
        if any(c.id_cliente == cliente.id_cliente for c in self.clientes):
            raise ValueError(f"Ya existe un cliente con id '{cliente.id_cliente}'.")
        self.clientes.append(cliente)

    def listar_clientes(self) -> List[Cliente]:
        return list(self.clientes)

    def buscar_cliente(self, termino: str) -> List[Cliente]:
        termino = termino.strip().lower()
        return [c for c in self.clientes if termino in c.nombre.lower() or termino in c.correo.lower() or termino in c.id_cliente.lower()]

