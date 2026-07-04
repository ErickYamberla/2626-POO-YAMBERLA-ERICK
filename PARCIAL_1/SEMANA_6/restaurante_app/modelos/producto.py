"""
Módulo producto.py
Contiene la clase base Producto con atributos comunes y un atributo encapsulado __precio.
"""

class Producto:
    """Clase padre que representa un producto general del restaurante."""

    def __init__(self, nombre: str, precio: float, disponible: bool = True):
        # Atributos públicos
        self.nombre = nombre
        # Atributo encapsulado (privado): precio
        self.__precio = float(precio)
        self.disponible = bool(disponible)

    # Método de acceso al precio (getter)
    def obtener_precio(self) -> float:
        return self.__precio

    # Método de modificación del precio (setter) con validación
    def cambiar_precio(self, nuevo_precio: float) -> None:
        nuevo_precio = float(nuevo_precio)
        if nuevo_precio <= 0:
            raise ValueError("El precio debe ser un valor mayor que cero.")
        self.__precio = nuevo_precio

    def mostrar_informacion(self) -> None:
        """Muestra información genérica del producto. Se sobrescribe en las clases hijas."""
        estado = "Disponible" if self.disponible else "No disponible"
        print(f"Producto: {self.nombre}")
        print(f"Precio: S/. {self.obtener_precio():.2f}")
        print(f"Estado: {estado}")

