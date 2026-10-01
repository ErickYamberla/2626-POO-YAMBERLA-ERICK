from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Venta:
    codigo: str
    usuario: str
    producto_codigo: str
    producto_nombre: str
    cantidad: int
    precio_unitario: float
    total: float
    fecha: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.codigo, str) or self.codigo.strip() == "":
            raise ValueError("El código de venta es obligatorio")
        if not isinstance(self.usuario, str) or self.usuario.strip() == "":
            raise ValueError("El usuario/cliente es obligatorio")
        if not isinstance(self.producto_codigo, str) or self.producto_codigo.strip() == "":
            raise ValueError("El código del producto es obligatorio")
        if not isinstance(self.producto_nombre, str) or self.producto_nombre.strip() == "":
            raise ValueError("El nombre del producto es obligatorio")

        try:
            self.cantidad = int(self.cantidad)
        except (TypeError, ValueError):
            raise ValueError("La cantidad debe ser un número entero válido")
        if self.cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser mayor a 0")

        try:
            self.precio_unitario = float(self.precio_unitario)
        except (TypeError, ValueError):
            raise ValueError("El precio unitario es inválido")
        if self.precio_unitario < 0:
            raise ValueError("El precio unitario no puede ser negativo")

        try:
            self.total = float(self.total)
        except (TypeError, ValueError):
            self.total = round(self.cantidad * self.precio_unitario, 2)
        if self.total < 0:
            raise ValueError("El total de la venta no puede ser negativo")

        if not self.fecha or self.fecha.strip() == "":
            self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.fecha = self.fecha.strip()

    def mostrar_informacion(self) -> str:
        return (
            f"[Venta] Código: {self.codigo} | Fecha: {self.fecha} | "
            f"Usuario: {self.usuario} | Producto: {self.producto_nombre} ({self.producto_codigo}) | "
            f"Cantidad: {self.cantidad} | P.Unit: $ {self.precio_unitario:.2f} | "
            f"Total: $ {self.total:.2f}"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "codigo": self.codigo,
            "usuario": self.usuario,
            "producto_codigo": self.producto_codigo,
            "producto_nombre": self.producto_nombre,
            "cantidad": int(self.cantidad),
            "precio_unitario": float(self.precio_unitario),
            "total": float(self.total),
            "fecha": self.fecha,
        }

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["Venta"]:
        if not data:
            return None
        try:
            return cls(
                codigo=str(data.get("codigo", "")).strip(),
                usuario=str(data.get("usuario", "")).strip(),
                producto_codigo=str(data.get("producto_codigo", "")).strip(),
                producto_nombre=str(data.get("producto_nombre", "")).strip(),
                cantidad=int(data.get("cantidad", 1)),
                precio_unitario=float(data.get("precio_unitario", 0.0)),
                total=float(data.get("total", 0.0)),
                fecha=str(data.get("fecha", "")).strip(),
            )
        except (TypeError, ValueError):
            return None
