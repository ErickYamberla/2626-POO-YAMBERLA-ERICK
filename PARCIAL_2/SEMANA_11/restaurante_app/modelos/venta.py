from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class Venta:
    usuario_id: str
    producto_codigo: str
    cantidad: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": int(self.cantidad),
        }

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["Venta"]:
        if not data:
            return None
        try:
            return cls(
                usuario_id=str(data.get("usuario_id", "")),
                producto_codigo=str(data.get("producto_codigo", "")),
                cantidad=int(data.get("cantidad", 0)),
            )
        except (TypeError, ValueError):
            return None
