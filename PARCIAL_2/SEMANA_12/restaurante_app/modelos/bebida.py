from dataclasses import dataclass
from .producto import Producto


@dataclass
class Bebida(Producto):
    tamano: str  # p.ej. '330ml', '500ml'
    presentacion: str  # p.ej. 'Lata', 'Botella'

    def mostrar_informacion(self) -> str:
        """Sobrescribe mostrar_informacion para incluir atributos de bebida.

        Mantiene la firma de Producto para cumplir LSP.
        """
        base = super().mostrar_informacion()
        return f"{base} | Tamaño: {self.tamano} | Presentación: {self.presentacion}"

