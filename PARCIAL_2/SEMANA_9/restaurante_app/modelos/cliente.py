from dataclasses import dataclass


@dataclass
class Cliente:
    identificacion: str
    nombre: str
    correo: str

    def mostrar_informacion(self) -> str:
        """Retorna una representación legible del cliente."""
        return (
            f"[Cliente] ID: {self.identificacion} | Nombre: {self.nombre} | "
            f"Correo: {self.correo}"
        )

