"""
modelos/producto.py
Clase Producto que representa un producto del restaurante (plato o bebida).
"""

class Producto:
    """Representa un producto del restaurante.

    Atributos:
        id (int): Identificador único del producto.
        nombre (str): Nombre del producto.
        descripcion (str): Breve descripción.
        precio (float): Precio en moneda local.
        tipo (str): 'plato' o 'bebida' u otro tipo categórico.
    """

    def __init__(self, id: int, nombre: str, descripcion: str, precio: float, tipo: str = "plato"):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = float(precio)
        self.tipo = tipo

    def __str__(self) -> str:
        # Representación legible del producto
        return f"Producto(id={self.id}, nombre='{self.nombre}', tipo='{self.tipo}', precio={self.precio:.2f})"

    def info(self) -> str:
        """Devuelve una cadena con información detallada del producto."""
        return f"{self.nombre} ({self.tipo}) - {self.descripcion} : ${self.precio:.2f}"

