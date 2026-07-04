"""
Punto de entrada de la aplicación restaurante_app.
Se crean algunos objetos Platillo y Bebida, se agregan al servicio Restaurante y se muestran.
"""

from modelos.platillo import Platillo
from modelos.bebida import Bebida
from servicios.restaurante import Restaurante


def main() -> None:
	# Crear instancia del servicio Restaurante
	mi_restaurante = Restaurante("La Buena Sazón")

	# Crear platillos (al menos 2)
	lomo_saltado = Platillo(nombre="Lomo Saltado", precio=25.50, calorias=650, tipo="Principal", tiempo_preparacion=20)
	ceviche = Platillo(nombre="Ceviche", precio=22.00, calorias=420, tipo="Entrada", tiempo_preparacion=15)

	# Crear bebidas (al menos 2)
	limonada = Bebida(nombre="Limonada", precio=6.50, volumen_ml=350, tamano="Mediana", tipo_bebida="Sin alcohol")
	cerveza = Bebida(nombre="Cerveza IPA", precio=12.00, volumen_ml=500, tamano="Grande", tipo_bebida="Con alcohol")

	# Agregar productos al restaurante
	mi_restaurante.agregar_producto(lomo_saltado)
	mi_restaurante.agregar_producto(ceviche)
	mi_restaurante.agregar_producto(limonada)
	mi_restaurante.agregar_producto(cerveza)

	# Mostrar productos: aquí se evidencia el polimorfismo
	mi_restaurante.mostrar_productos()


if __name__ == "__main__":
	main()


