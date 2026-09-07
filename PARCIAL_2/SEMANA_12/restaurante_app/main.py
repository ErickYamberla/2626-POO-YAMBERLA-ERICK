"""Punto de entrada del sistema restaurante_app - Semana 11.

Menú interactivo que utiliza el servicio Restaurante para toda la gestión de
productos, usuarios y ventas. main.py no modifica directamente las colecciones internas
del servicio; sólo solicita datos y delega operaciones.
"""
from typing import Optional

from modelos.producto import Producto
from modelos.usuario import Usuario
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
    print("6. Registrar usuario")
    print("7. Buscar usuario")
    print("8. Actualizar usuario")
    print("9. Eliminar usuario")
    print("10. Listar usuarios")
    print("-" * 40)
    print("11. Mostrar categorías")
    print("12. Registrar Venta")
    print("13. Consultar ventas por usuario")
    print("14. Salir")


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
            codigo = solicitar_input("Código: ")
            nombre = solicitar_input("Nombre: ")
            categoria = solicitar_input("Categoría: ")
            try:
                precio = float(solicitar_input("Precio: "))
            except ValueError:
                print("Precio inválido. Operación cancelada.")
                continue
            try:
                stock = int(solicitar_input("Stock inicial: "))
            except ValueError:
                print("Stock inválido. Se usará 0.")
                stock = 0
            producto = Producto(codigo=codigo, nombre=nombre, categoria=categoria, precio=precio, stock=stock)
            if servicio.registrar_producto(producto):
                print("Producto registrado correctamente.")
            else:
                print("Error: ya existe un producto con ese código.")

        elif opcion == "2":
            codigo = solicitar_input("Código del producto a buscar: ")
            encontrado = servicio.buscar_producto(codigo)
            if encontrado:
                print("Producto encontrado:")
                print(encontrado.mostrar_informacion())
            else:
                print("Producto no encontrado.")

        elif opcion == "3":
            codigo = solicitar_input("Código del producto a actualizar: ")
            if not servicio.buscar_producto(codigo):
                print("No existe un producto con ese código.")
                continue
            nombre = solicitar_input("Nuevo nombre (ENTER para mantener): ")
            categoria = solicitar_input("Nueva categoría (ENTER para mantener): ")
            precio_str = solicitar_input("Nuevo precio (ENTER para mantener): ")
            stock_str = solicitar_input("Nuevo stock (ENTER para mantener): ")
            precio = None
            stock = None
            if precio_str != "":
                try:
                    precio = float(precio_str)
                except ValueError:
                    print("Precio inválido; no se actualizará el precio.")
            if stock_str != "":
                try:
                    stock = int(stock_str)
                except ValueError:
                    print("Stock inválido; no se actualizará el stock.")
            if servicio.actualizar_producto(codigo, nombre=nombre or None, categoria=categoria or None, precio=precio, stock=stock):
                print("Producto actualizado.")
            else:
                print("Error al actualizar el producto.")

        elif opcion == "4":
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
            usuario = Usuario(identificacion=identificacion, nombre=nombre, correo=correo)
            if servicio.registrar_usuario(usuario):
                print("Usuario registrado correctamente.")
            else:
                print("Error: ya existe un usuario con esa identificación.")

        elif opcion == "7":
            identificacion = solicitar_input("Identificación del usuario a buscar: ")
            encontrado = servicio.buscar_usuario(identificacion)
            if encontrado:
                print("Usuario encontrado:")
                print(encontrado.mostrar_informacion())
            else:
                print("Usuario no encontrado.")

        elif opcion == "8":
            identificacion = solicitar_input("Identificación del usuario a actualizar: ")
            if not servicio.buscar_usuario(identificacion):
                print("No existe un usuario con esa identificación.")
                continue
            nombre = solicitar_input("Nuevo nombre (ENTER para mantener): ")
            correo = solicitar_input("Nuevo correo (ENTER para mantener): ")
            if servicio.actualizar_usuario(identificacion, nombre=nombre or None, correo=correo or None):
                print("Usuario actualizado.")
            else:
                print("Error al actualizar el usuario.")

        elif opcion == "9":
            identificacion = solicitar_input("Identificación del usuario a eliminar: ")
            confirmado = solicitar_input("Confirma eliminación? (s/N): ")
            if confirmado.lower() == "s":
                if servicio.eliminar_usuario(identificacion):
                    print("Usuario eliminado.")
                else:
                    print("No se encontró el usuario.")
            else:
                print("Operación cancelada.")

        elif opcion == "10":
            usuarios = servicio.listar_usuarios()
            if not usuarios:
                print("No hay usuarios registrados.")
            else:
                print("\nListado de usuarios:")
                for info in usuarios:
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
            identificacion = solicitar_input("Identificación del comprador: ")
            codigo = solicitar_input("Código del producto a vender: ")
            try:
                cantidad = int(solicitar_input("Cantidad a vender: "))
            except ValueError:
                print("Cantidad inválida. Operación cancelada.")
                continue
            ok = servicio.registrar_venta(codigo, identificacion, cantidad)
            if ok:
                print("Venta registrada correctamente. El stock del producto fue descontado.")
            else:
                print("No se pudo realizar la venta. Verifique usuario, producto o stock.")

        elif opcion == "13":
            identificacion = solicitar_input("Identificación del usuario: ")
            ventas = servicio.ventas_por_usuario(identificacion)
            if not ventas:
                print("No hay ventas registradas para este usuario.")
            else:
                print("\nVentas del usuario:")
                for v in ventas:
                    prod = servicio.buscar_producto(v.producto_codigo)
                    nombre_prod = prod.nombre if prod else "<desconocido>"
                    print(f"Producto: {v.producto_codigo} | Nombre: {nombre_prod} | Cantidad: {v.cantidad}")

        elif opcion == "14":
            print("Saliendo...")
            break

        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
