"""Punto de entrada del sistema restaurante_app.

Al ejecutarse muestra un menú interactivo para registrar/listar productos, bebidas y clientes.
También explica de forma didáctica los principios SOLID aplicados al software.
"""
from typing import Optional

from modelos.producto import Producto
from modelos.bebida import Bebida
from modelos.cliente import Cliente
from servicios.restaurante import Restaurante


def mostrar_menu() -> None:
    print("=" * 40)
    print("        SISTEMA DE RESTAURANTE")
    print("=" * 40)
    print("1. Registrar producto")
    print("2. Registrar bebida")
    print("3. Registrar cliente")
    print("-" * 40)
    print("4. Listar productos")
    print("5. Listar clientes")
    print("-" * 40)
    print("6. Explicar principios SOLID")
    print("7. Salir")


def solicitar_input(prompt: str, tipo: Optional[type] = str):
    valor = input(prompt).strip()
    if tipo is float:
        try:
            return float(valor)
        except ValueError:
            print("Valor inválido, se usará 0.0")
            return 0.0
    return valor


def explicar_solid() -> None:
    print("\nExplicación didáctica de los principios SOLID aplicada al restaurante:\n")
    print("S - Responsabilidad única (SRP):")
    print("  - Cada clase tiene una única responsabilidad: Producto/Bebida modelan datos, Cliente almacena datos de cliente,")
    print("    Restaurante gestiona colecciones y operaciones, y main.py se encarga solo de la interacción con el usuario.\n")
    print("O - Abierto/Cerrado (OCP):")
    print("  - La clase Bebida extiende Producto añadiendo atributos y comportamiento sin modificar la lógica del servicio Restaurante.")
    print("    Restaurante trabaja con la interfaz común (mostrar_informacion), por lo que nuevas subclases pueden añadirse sin cambiarlo.\n")
    print("L - Sustitución de Liskov (LSP):")
    print("  - Una Bebida puede usarse donde se espera un Producto. Restaurante invoca mostrar_informacion() sin preguntar el tipo concreto,")
    print("    y cada subclase devuelve su propia representación, manteniendo el comportamiento esperado.\n")
    print("Nota: I (Segregación de interfaces) y D (Inversión de dependencias) se consideran conceptualmente en el diseño modular,")
    print("pero no son exigidos en la implementación básica de esta actividad.\n")


def main() -> None:
    servicio = Restaurante()

    while True:
        mostrar_menu()
        opcion = solicitar_input("Seleccione una opción: ")

        if opcion == "1":
            codigo = solicitar_input("Código: ")
            nombre = solicitar_input("Nombre: ")
            categoria = solicitar_input("Categoría: ")
            precio = solicitar_input("Precio: ", float)
            producto = Producto(codigo=codigo, nombre=nombre, categoria=categoria, precio=precio)
            if servicio.registrar_producto(producto):
                print("Producto registrado correctamente.")
            else:
                print("Error: ya existe un producto con ese código.")

        elif opcion == "2":
            codigo = solicitar_input("Código: ")
            nombre = solicitar_input("Nombre: ")
            categoria = solicitar_input("Categoría: ")
            precio = solicitar_input("Precio: ", float)
            tamano = solicitar_input("Tamaño (p.ej. 500ml): ")
            presentacion = solicitar_input("Presentación (p.ej. Botella): ")
            bebida = Bebida(codigo=codigo, nombre=nombre, categoria=categoria, precio=precio, tamano=tamano, presentacion=presentacion)
            if servicio.registrar_producto(bebida):
                print("Bebida registrada correctamente.")
            else:
                print("Error: ya existe un producto con ese código.")

        elif opcion == "3":
            identificacion = solicitar_input("Identificación: ")
            nombre = solicitar_input("Nombre: ")
            correo = solicitar_input("Correo: ")
            cliente = Cliente(identificacion=identificacion, nombre=nombre, correo=correo)
            if servicio.registrar_cliente(cliente):
                print("Cliente registrado correctamente.")
            else:
                print("Error: ya existe un cliente con esa identificación.")

        elif opcion == "4":
            productos = servicio.listar_productos()
            if not productos:
                print("No hay productos registrados.")
            else:
                print("\nListado de productos:")
                for info in productos:
                    print(info)

        elif opcion == "5":
            clientes = servicio.listar_clientes()
            if not clientes:
                print("No hay clientes registrados.")
            else:
                print("\nListado de clientes:")
                for info in clientes:
                    print(info)

        elif opcion == "6":
            explicar_solid()

        elif opcion == "7":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()


