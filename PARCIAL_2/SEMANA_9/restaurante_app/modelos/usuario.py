from dataclasses import dataclass


@dataclass
class Usuario:
    identificacion: str
    nombre: str
    correo: str

    def mostrar_informacion(self) -> str:
        """Retorna una representación legible del usuario."""
        return (
            f"[Usuario] ID: {self.identificacion} | Nombre: {self.nombre} | "
            f"Correo: {self.correo}"
        )
