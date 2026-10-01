from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Usuario:
    """
    Modelo de Usuario para el sistema del restaurante.
    Semana 16: Incorpora el identificador y el atributo rol para diferenciar
    entre Administrador, Empleado y Cliente.
    """
    usuario: str
    password: str
    nombre: str
    correo: str = ""
    rol: str = "Cliente"
    id: str = ""

    ROLES_PERMITIDOS = ("Administrador", "Empleado", "Cliente")

    def __post_init__(self) -> None:
        if not isinstance(self.usuario, str) or self.usuario.strip() == "":
            raise ValueError("El nombre de usuario es obligatorio.")
        if not isinstance(self.password, str) or self.password.strip() == "":
            raise ValueError("La contraseña es obligatoria.")
        if not isinstance(self.nombre, str) or self.nombre.strip() == "":
            raise ValueError("El nombre del usuario es obligatorio.")

        self.usuario = self.usuario.strip()
        self.password = self.password.strip()
        self.nombre = self.nombre.strip()
        self.correo = str(self.correo or "").strip()

        # Normalizar y validar el rol
        rol_limpio = str(self.rol or "").strip().capitalize()
        if rol_limpio in self.ROLES_PERMITIDOS:
            self.rol = rol_limpio
        else:
            self.rol = "Cliente"

        # Identificador por defecto si no se especifica
        if not self.id:
            self.id = self.usuario

    def mostrar_informacion(self) -> str:
        return (
            f"[Usuario {self.id}] {self.nombre} ({self.usuario}) | "
            f"Rol: {self.rol} | Correo: {self.correo or 'N/A'}"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "usuario": self.usuario,
            "contrasena": self.password,
            "nombre": self.nombre,
            "correo": self.correo,
            "rol": self.rol,
        }

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["Usuario"]:
        if not data:
            return None
        password = data.get("password", data.get("contrasena", ""))
        usuario_clave = str(data.get("usuario", "")).strip()
        id_val = str(data.get("id", usuario_clave)).strip()
        rol_val = str(data.get("rol", "Cliente")).strip()

        try:
            return cls(
                id=id_val,
                usuario=usuario_clave,
                password=str(password).strip(),
                nombre=str(data.get("nombre", "")).strip(),
                correo=str(data.get("correo", "")).strip(),
                rol=rol_val,
            )
        except (TypeError, ValueError):
            return None
