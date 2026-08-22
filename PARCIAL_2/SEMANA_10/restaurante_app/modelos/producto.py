from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Producto:
    codigo: str
    nombre: str
    categoria: str
    precio: float

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

    def mostrar_informacion(self) -> str:
        """Retorna una representación legible del producto."""
        return (
            f"[Producto] Código: {self.codigo} | Nombre: {self.nombre} | "
            f"Categoría: {self.categoria} | Precio: S/. {self.precio:.2f}"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": float(self.precio),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Producto":
        return cls(
            codigo=str(data["codigo"]),
            nombre=str(data["nombre"]),
            categoria=str(data.get("categoria", "")),
            precio=float(data["precio"]),
        )
