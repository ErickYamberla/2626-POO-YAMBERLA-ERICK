from dataclasses import dataclass
from typing import Any, Dict


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
        if not isinstance(self.categoria, str):
            self.categoria = str(self.categoria or "")
        try:
            self.precio = float(self.precio)
        except (TypeError, ValueError):
            raise ValueError("El precio del producto es inválido")
        if self.precio < 0:
            raise ValueError("El precio del producto no puede ser negativo")
        try:
            self.stock = int(self.stock)
        except (TypeError, ValueError):
            raise ValueError("El stock del producto es inválido")
        if self.stock < 0:
            raise ValueError("El stock del producto no puede ser negativo")

    def mostrar_informacion(self) -> str:
        return (
            f"[Producto] Código: {self.codigo} | Nombre: {self.nombre} | "
            f"Categoría: {self.categoria} | Precio: S/. {self.precio:.2f} | "
            f"Stock: {self.stock}"
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
