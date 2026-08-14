"""Punto de entrada del sistema restaurante_app - Semana 9.

Menú interactivo que utiliza el servicio Restaurante para toda la gestión de
productos y clientes. main.py no modifica directamente las colecciones internas
 del servicio; sólo solicita datos y delega operaciones.
"""
from typing import Optional

from modelos.producto import Producto
from modelos.cliente import Cliente
from servicios.restaurante import Restaurante


def mostrar_menu() -> None:
    print("=" * 40)
    print("        SISTEMA DE RESTAURANTE")
    print("=" * 40)
    print("1. Registrar producto")
    print("2. Buscar producto")
    print("3. Actualizar producto")
    print("4. Eliminar producto")
    print("5. Listar productos")
    print("-" * 40)
    print("6. Registrar cliente")
    print("7. Buscar cliente")
    print("8. Actualizar cliente")
    print("9. Eliminar cliente")
    print("10. Listar clientes")
    print("-" * 40)
    print("11. Mostrar categorías")
    print("12. Salir")


def solicitar_input(prompt: str, tipo: Optional[type] = str):
    valor = input(prompt).strip()
    if tipo is float:
        try:
            return float(valor)
        except ValueError:
            print("Valor inválido, se usará 0.0")
            return 0.0
    return valor


def main() -> None:
    servicio = Restaurante()

    while True:
        mostrar_menu()
        opcion = solicitar_input("Seleccione una opción: ")

        if opcion == "1":
            # Registrar producto
            codigo = solicitar_input("Código: ")
            nombre = solicitar_input("Nombre: ")
            categoria = solicitar_input("Categoría: ")
            try:
                precio = float(solicitar_input("Precio: "))
            except ValueError:
                print("Precio inválido. Operación cancelada.")
                continue
            producto = Producto(codigo=codigo, nombre=nombre, categoria=categoria, precio=precio)
            if servicio.registrar_producto(producto):
                print("Producto registrado correctamente.")
            else:
                print("Error: ya existe un producto con ese código.")

        elif opcion == "2":
            # Buscar producto
            codigo = solicitar_input("Código del producto a buscar: ")
            encontrado = servicio.buscar_producto(codigo)
            if encontrado:
                print("Producto encontrado:")
                print(encontrado.mostrar_informacion())
            else:
                print("Producto no encontrado.")

        elif opcion == "3":
            # Actualizar producto
            codigo = solicitar_input("Código del producto a actualizar: ")
            if not servicio.buscar_producto(codigo):
                print("No existe un producto con ese código.")
                continue
            nombre = solicitar_input("Nuevo nombre (ENTER para mantener): ")
            categoria = solicitar_input("Nueva categoría (ENTER para mantener): ")
            precio_str = solicitar_input("Nuevo precio (ENTER para mantener): ")
            precio = None
            if precio_str != "":
                try:
                    precio = float(precio_str)
                except ValueError:
                    print("Precio inválido; no se actualizará el precio.")
            if servicio.actualizar_producto(codigo, nombre=nombre or None, categoria=categoria or None, precio=precio):
                print("Producto actualizado.")
            else:
                print("Error al actualizar el producto.")

        elif opcion == "4":
            # Eliminar producto
            codigo = solicitar_input("Código del producto a eliminar: ")
            confirmado = solicitar_input("Confirma eliminación? (s/N): ")
            if confirmado.lower() == "s":
                if servicio.eliminar_producto(codigo):
                    print("Producto eliminado.")
                else:
                    print("No se encontró el producto.")
            else:
                print("Operación cancelada.")

        elif opcion == "5":
            productos = servicio.listar_productos()
            if not productos:
                print("No hay productos registrados.")
            else:
                print("\nListado de productos:")
                for info in productos:
                    print(info)

        elif opcion == "6":
            identificacion = solicitar_input("Identificación: ")
            nombre = solicitar_input("Nombre: ")
            correo = solicitar_input("Correo: ")
            cliente = Cliente(identificacion=identificacion, nombre=nombre, correo=correo)
            if servicio.registrar_cliente(cliente):
                print("Cliente registrado correctamente.")
            else:
                print("Error: ya existe un cliente con esa identificación.")

        elif opcion == "7":
            identificacion = solicitar_input("Identificación del cliente a buscar: ")
            encontrado = servicio.buscar_cliente(identificacion)
            if encontrado:
                print("Cliente encontrado:")
                print(encontrado.mostrar_informacion())
            else:
                print("Cliente no encontrado.")

        elif opcion == "8":
            identificacion = solicitar_input("Identificación del cliente a actualizar: ")
            if not servicio.buscar_cliente(identificacion):
                print("No existe un cliente con esa identificación.")
                continue
            nombre = solicitar_input("Nuevo nombre (ENTER para mantener): ")
            correo = solicitar_input("Nuevo correo (ENTER para mantener): ")
            if servicio.actualizar_cliente(identificacion, nombre=nombre or None, correo=correo or None):
                print("Cliente actualizado.")
            else:
                print("Error al actualizar el cliente.")

        elif opcion == "9":
            identificacion = solicitar_input("Identificación del cliente a eliminar: ")
            confirmado = solicitar_input("Confirma eliminación? (s/N): ")
            if confirmado.lower() == "s":
                if servicio.eliminar_cliente(identificacion):
                    print("Cliente eliminado.")
                else:
                    print("No se encontró el cliente.")
            else:
                print("Operación cancelada.")

        elif opcion == "10":
            clientes = servicio.listar_clientes()
            if not clientes:
                print("No hay clientes registrados.")
            else:
                print("\nListado de clientes:")
                for info in clientes:
                    print(info)

        elif opcion == "11":
            categorias = servicio.mostrar_categorias()
            if not categorias:
                print("No hay categorías disponibles.")
            else:
                print("\nCategorías de productos:")
                for c in categorias:
                    print(f"- {c}")

        elif opcion == "12":
            print("Saliendo...")
            break

        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()


