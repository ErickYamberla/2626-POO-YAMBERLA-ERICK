"""
Programa: Programación Tradicional - registro de mascotas

Este programa utiliza únicamente variables y funciones (no clases u objetos)
para:
- Registrar información de una o varias mascotas mediante entrada por teclado.
- Mostrar la información registrada de forma organizada.

Comentarios están escritos en español para facilitar el aprendizaje.
"""

def solicitar_datos_mascota():
	"""Pide al usuario los datos de una mascota y los devuelve como diccionario.

	Se usan variables sencillas para almacenar cada campo. La función valida
	que la edad ingresada sea un número entero mayor o igual a 0.
	"""
	nombre = input("Nombre de la mascota: ").strip()
	especie = input("Especie (por ejemplo: perro, gato): ").strip()

	# Validamos que la edad sea un entero no negativo. Si el usuario ingresa
	# un valor inválido, volvemos a pedir la edad hasta obtener un valor correcto.
	while True:
		edad_input = input("Edad (años): ").strip()
		try:
			edad = int(edad_input)
			if edad < 0:
				print("La edad no puede ser negativa. Intenta de nuevo.")
				continue
			break
		except ValueError:
			print("Por favor ingresa un número entero para la edad.")

	# Otros datos opcionales
	color = input("Color: ").strip()
	duenio = input("Nombre del dueño: ").strip()

	# Devolvemos los datos en un diccionario para facilitar su manejo.
	mascota = {
		"nombre": nombre,
		"especie": especie,
		"edad": edad,
		"color": color,
		"duenio": duenio,
	}
	return mascota


def mostrar_mascota(mascota, indice=None):
	"""Muestra en pantalla la información de una mascota de forma organizada.

	El parámetro `indice` es opcional y sirve para numerar la mascota cuando
	hay varias registradas.
	"""
	encabezado = f"Mascota #{indice}" if indice is not None else "Mascota"
	print("\n" + "=" * 40)
	print(encabezado)
	print("-" * 40)
	print(f"Nombre : {mascota.get('nombre', '')}")
	print(f"Especie: {mascota.get('especie', '')}")
	print(f"Edad   : {mascota.get('edad', '')} años")
	print(f"Color  : {mascota.get('color', '')}")
	print(f"Dueño  : {mascota.get('duenio', '')}")
	print("=" * 40 + "\n")


def main():
	"""Función principal que controla el flujo del programa.

	Permite registrar varias mascotas preguntando al usuario si desea
	continuar. Usa una lista para almacenar cada mascota (cada una es un
	diccionario), y muestra todas las mascotas registradas al finalizar.
	"""
	print("Programa: Registro de mascotas (programación tradicional)")
	mascotas = []  # Lista donde guardaremos cada registro de mascota

	while True:
		mascota = solicitar_datos_mascota()
		mascotas.append(mascota)

		# Preguntamos si se desea ingresar otra mascota. Aceptamos 's' o 'n'.
		while True:
			opc = input("¿Deseas registrar otra mascota? (s/n): ").strip().lower()
			if opc in ("s", "n"):
				break
			print("Respuesta no válida. Escribe 's' para sí o 'n' para no.")

		if opc == "n":
			break

	# Mostrar todas las mascotas registradas
	print("\nResumen de mascotas registradas:")
	for i, m in enumerate(mascotas, start=1):
		mostrar_mascota(m, indice=i)


if __name__ == "__main__":
	main()


