"""
Módulo platillo.py
Contiene la clase Platillo que hereda de Producto y añade atributos específicos.
"""

from .producto import Producto


class Platillo(Producto):
    """Representa un platillo (comida) del restaurante."""

    def __init__(self, nombre: str, precio: float, calorias: int, tipo: str, tiempo_preparacion: int, disponible: bool = True):
        # Reutilizamos el constructor de la clase padre para nombre, precio y disponible
        super().__init__(nombre, precio, disponible)
        # Atributos específicos de Platillo
        self.calorias = int(calorias)
        self.tipo = tipo  # ej. 'Entrada', 'Principal', 'Postre'
        self.tiempo_preparacion = int(tiempo_preparacion)  # minutos

    # Sobrescribimos mostrar_informacion para demostrar polimorfismo
    def mostrar_informacion(self) -> None:
        print(f"Platillo: {self.nombre}")
        print(f"Tipo: {self.tipo} | Calorías: {self.calorias} kcal | Tiempo: {self.tiempo_preparacion} min")
        print(f"Precio: S/. {self.obtener_precio():.2f}")
        print(f"Disponibilidad: {'Sí' if self.disponible else 'No'}")

