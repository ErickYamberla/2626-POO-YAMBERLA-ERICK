from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Usuario:
    usuario: str
    password: str
    nombre: str
    correo: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.usuario, str) or self.usuario.strip() == "":
            raise ValueError("El usuario es obligatorio")
        if not isinstance(self.password, str) or self.password.strip() == "":
            raise ValueError("La contrasena es obligatoria")
        if not isinstance(self.nombre, str) or self.nombre.strip() == "":
            raise ValueError("El nombre es obligatorio")
        self.usuario = self.usuario.strip()
        self.password = self.password.strip()
        self.nombre = self.nombre.strip()
        self.correo = str(self.correo or "").strip()

    def mostrar_informacion(self) -> str:
        return (
            f"[Usuario] Usuario: {self.usuario} | Nombre: {self.nombre} | "
            f"Correo: {self.correo}"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "usuario": self.usuario,
            "contrasena": self.password,
            "nombre": self.nombre,
            "correo": self.correo,
        }

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["Usuario"]:
        if not data:
            return None
        password = data.get("password", data.get("contrasena", ""))
        try:
            return cls(
                usuario=str(data.get("usuario", "")).strip(),
                password=str(password).strip(),
                nombre=str(data.get("nombre", "")).strip(),
                correo=str(data.get("correo", "")).strip(),
            )
        except (TypeError, ValueError):
            return None
