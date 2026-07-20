from dataclasses import dataclass


@dataclass
class Producto:
    codigo: str
    nombre: str
    categoria: str
    precio: float

    def mostrar_informacion(self) -> str:
        """Retorna una representación legible del producto."""
        return (
            f"[Producto] Código: {self.codigo} | Nombre: {self.nombre} | "
            f"Categoría: {self.categoria} | Precio: S/. {self.precio:.2f}"
        )

