"""Punto de entrada del sistema de restaurante.

Presenta un menú interactivo por consola para registrar, listar y buscar productos y clientes.
"""

from servicios.restaurante import Restaurante
from modelos.producto import Producto
from modelos.cliente import Cliente


def mostrar_menu() -> None:
    print("\n" + "=" * 40)
    print("\tSISTEMA DE RESTAURANTE")
    print("=" * 40)
    print("1. Registrar producto")
    print("2. Listar productos")
    print("3. Buscar producto")
    print("-" * 40)
    print("4. Registrar cliente")
    print("5. Listar clientes")
    print("6. Buscar cliente")
    print("-" * 40)
    print("7. Salir")


def solicitar_datos_producto() -> Producto:
    print("\nRegistrar nuevo producto:")
    while True:
        nombre = input("Nombre: ").strip()
        if not nombre:
            print("El nombre no puede estar vacío. Intente de nuevo.")
            continue
        break
    while True:
        categoria = input("Categoría: ").strip()
        if not categoria:
            print("La categoría no puede estar vacía. Intente de nuevo.")
            continue
        break
    while True:
        precio_str = input("Precio (ej. 12.50): ").strip()
        try:
            precio = float(precio_str)
            if precio <= 0:
                print("El precio debe ser mayor que cero.")
                continue
        except ValueError:
            print("Precio inválido. Ingrese un número válido.")
            continue
        break
    disponible_str = input("Disponible? (s/N): ").strip().lower()
    disponible = disponible_str == "s" or disponible_str == "si"
    return Producto(nombre=nombre, categoria=categoria, precio=precio, disponible=disponible)


def solicitar_datos_cliente() -> Cliente:
    print("\nRegistrar nuevo cliente:")
    while True:
        nombre = input("Nombre completo: ").strip()
        if not nombre:
            print("El nombre no puede estar vacío.")
            continue
        break
    while True:
        correo = input("Correo: ").strip()
        if not correo:
            print("El correo no puede estar vacío.")
            continue
        break
    while True:
        id_cliente = input("ID cliente (ej. C003): ").strip()
        if not id_cliente:
            print("El ID no puede estar vacío.")
            continue
        break
    return Cliente(nombre=nombre, correo=correo, id_cliente=id_cliente)


def ejecutar() -> None:
    servicio = Restaurante()
    print("Bienvenido al sistema. Se han cargado datos de ejemplo para probar.")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            try:
                producto = solicitar_datos_producto()
                servicio.registrar_producto(producto)
                print("Producto registrado correctamente:")
                print(producto.mostrar_informacion())
            except Exception as e:
                print(f"Error al registrar producto: {e}")

        elif opcion == "2":
            productos = servicio.listar_productos()
            print(f"\nSe encontraron {len(productos)} productos:")
            for p in productos:
                print(" - ", p.mostrar_informacion())

        elif opcion == "3":
            termino = input("Ingrese nombre o parte del nombre a buscar: ").strip()
            resultados = servicio.buscar_producto(termino)
            print(f"\nResultados ({len(resultados)}):")
            for p in resultados:
                print(" - ", p.mostrar_informacion())

        elif opcion == "4":
            try:
                cliente = solicitar_datos_cliente()
                servicio.registrar_cliente(cliente)
                print("Cliente registrado correctamente:")
                print(cliente)
            except Exception as e:
                print(f"Error al registrar cliente: {e}")

        elif opcion == "5":
            clientes = servicio.listar_clientes()
            print(f"\nSe encontraron {len(clientes)} clientes:")
            for c in clientes:
                print(f" - {c.nombre} | {c.correo} | ID: {c.id_cliente}")

        elif opcion == "6":
            termino = input("Ingrese nombre, correo o id a buscar: ").strip()
            resultados = servicio.buscar_cliente(termino)
            print(f"\nResultados ({len(resultados)}):")
            for c in resultados:
                print(f" - {c.nombre} | {c.correo} | ID: {c.id_cliente}")

        elif opcion == "7":
            print("Saliendo. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    ejecutar()

