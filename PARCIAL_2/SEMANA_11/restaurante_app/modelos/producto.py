from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Producto:
    codigo: str
    nombre: str
    categoria: str
    precio: float
    stock: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.codigo, str) or self.codigo.strip() == "":
            raise ValueError("El código del producto es obligatorio")
        if not isinstance(self.nombre, str) or self.nombre.strip() == "":
            raise ValueError("El nombre del producto es obligatorio")
        try:
            self.precio = float(self.precio)
        except (TypeError, ValueError):
            raise ValueError("Precio inválido para el producto")
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo")
        try:
            self.stock = int(self.stock)
        except (TypeError, ValueError):
            raise ValueError("Stock inválido para el producto")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")

    def mostrar_informacion(self) -> str:
        return (
            f"[Producto] Código: {self.codigo} | Nombre: {self.nombre} | "
            f"Categoría: {self.categoria} | Precio: S/. {self.precio:.2f} | Stock: {self.stock}"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": float(self.precio),
            "stock": int(self.stock),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Producto":
        return cls(
            codigo=str(data["codigo"]),
            nombre=str(data["nombre"]),
            categoria=str(data.get("categoria", "")),
            precio=float(data.get("precio", 0.0)),
            stock=int(data.get("stock", 0)),
        )

    def vender(self, cantidad: int) -> None:
        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            raise ValueError("Cantidad inválida para la venta")
        if cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser mayor que cero")
        if cantidad > self.stock:
            raise ValueError("Stock insuficiente")
        self.stock -= cantidad
