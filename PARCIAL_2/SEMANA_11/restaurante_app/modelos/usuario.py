from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class Usuario:
    identificacion: str
    nombre: str
    correo: str

    def __post_init__(self) -> None:
        if not isinstance(self.identificacion, str) or self.identificacion.strip() == "":
            raise ValueError("La identificación es obligatoria")
        if not isinstance(self.nombre, str) or self.nombre.strip() == "":
            raise ValueError("El nombre es obligatorio")
        if not isinstance(self.correo, str):
            self.correo = str(self.correo or "")

    def mostrar_informacion(self) -> str:
        return (
            f"[Usuario] ID: {self.identificacion} | Nombre: {self.nombre} | "
            f"Correo: {self.correo}"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
        }

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["Usuario"]:
        if not data:
            return None
        try:
            return cls(
                identificacion=str(data.get("identificacion", "")),
                nombre=str(data.get("nombre", "")),
                correo=str(data.get("correo", "")),
            )
        except (TypeError, ValueError):
            return None
