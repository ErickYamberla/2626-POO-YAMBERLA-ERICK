"""
Módulo bebida.py
Contiene la clase Bebida que hereda de Producto y añade atributos específicos.
"""

from .producto import Producto


class Bebida(Producto):
    """Representa una bebida disponible en el restaurante."""

    def __init__(self, nombre: str, precio: float, volumen_ml: int, tamano: str, tipo_bebida: str, disponible: bool = True):
        super().__init__(nombre, precio, disponible)
        # Atributos específicos de Bebida
        self.volumen_ml = int(volumen_ml)
        self.tamano = tamano  # ej. 'Pequeña', 'Mediana', 'Grande'
        self.tipo_bebida = tipo_bebida  # ej. 'Sin alcohol', 'Con alcohol', 'Caliente'

    def mostrar_informacion(self) -> None:
        print(f"Bebida: {self.nombre}")
        print(f"Tipo: {self.tipo_bebida} | Tamaño: {self.tamano} | Volumen: {self.volumen_ml} ml")
        print(f"Precio: S/. {self.obtener_precio():.2f}")
        print(f"Disponibilidad: {'Sí' if self.disponible else 'No'}")

