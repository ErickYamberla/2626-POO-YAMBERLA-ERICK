from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from restaurante_app.modelos.producto import Producto
    from restaurante_app.modelos.usuario import Usuario
    from restaurante_app.modelos.venta import Venta
    from restaurante_app.servicios.archivo_servicio import ArchivoServicio
except ModuleNotFoundError:
    from modelos.producto import Producto
    from modelos.usuario import Usuario
    from modelos.venta import Venta
    from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """Servicio del restaurante para validar acceso y gestionar productos, usuarios y ventas."""

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        base = Path(__file__).resolve().parent.parent if base_dir is None else Path(base_dir)
        self._archivo = ArchivoServicio(base)
        self._productos: Dict[str, Producto] = {}
        self._usuarios: Dict[str, Usuario] = {}
        self._ventas: List[Venta] = []
        self._cargar_datos()

    def _cargar_datos(self) -> None:
        for entrada in self._archivo.cargar_productos():
            try:
                producto = Producto.from_dict(entrada)
                if producto:
                    self._productos[producto.codigo] = producto
            except (KeyError, ValueError) as exc:
                print(f"Registro de producto omitido: {exc}")

        for entrada in self._archivo.cargar_usuarios():
            try:
                usuario = Usuario.from_dict(entrada)
                if usuario:
                    self._usuarios[usuario.usuario] = usuario
            except (KeyError, ValueError) as exc:
                print(f"Registro de usuario omitido: {exc}")

        for entrada in self._archivo.cargar_ventas():
            try:
                venta = Venta.from_dict(entrada)
                if venta:
                    self._ventas.append(venta)
            except (KeyError, ValueError) as exc:
                print(f"Registro de venta omitido: {exc}")

    def _guardar_productos(self) -> None:
        self._archivo.guardar_productos([producto.to_dict() for producto in self._productos.values()])

    def _guardar_usuarios(self) -> None:
        self._archivo.guardar_usuarios([usuario.to_dict() for usuario in self._usuarios.values()])

    def _guardar_ventas(self) -> None:
        self._archivo.guardar_ventas([venta.to_dict() for venta in self._ventas])

    # ----------------------------------------------------
    # Gestión de Usuarios y Autenticación
    # ----------------------------------------------------
    def validar_acceso(self, usuario: str, password: str) -> bool:
        usuario_obj = self._usuarios.get(usuario.strip())
        if usuario_obj is None:
            return False
        return usuario_obj.password == password.strip()

    def buscar_usuario(self, usuario: str) -> Optional[Usuario]:
        if usuario is None:
            return None
        return self._usuarios.get(usuario.strip())

    def registrar_usuario(self, usuario: Usuario) -> bool:
        clave = usuario.usuario.strip()
        if clave in self._usuarios:
            return False
        self._usuarios[clave] = usuario
        self._guardar_usuarios()
        return True

    def actualizar_usuario(self, usuario: str, *, password: Optional[str] = None,
                           nombre: Optional[str] = None, correo: Optional[str] = None) -> bool:
        clave = (usuario or "").strip()
        usuario_actual = self._usuarios.get(clave)
        if usuario_actual is None:
            return False

        if password is not None and password.strip() != "":
            usuario_actual.password = password.strip()
        if nombre is not None and nombre.strip() != "":
            usuario_actual.nombre = nombre.strip()
        if correo is not None and correo.strip() != "":
            usuario_actual.correo = correo.strip()

        self._guardar_usuarios()
        return True

    def eliminar_usuario(self, usuario: str) -> bool:
        clave = (usuario or "").strip()
        if clave not in self._usuarios:
            return False
        del self._usuarios[clave]
        self._guardar_usuarios()
        return True

    def listar_usuarios(self) -> List[Usuario]:
        return list(self._usuarios.values())

    def obtener_usuarios_texto(self) -> List[str]:
        if not self._usuarios:
            return ["No hay usuarios registrados."]
        return [usuario.mostrar_informacion() for usuario in self._usuarios.values()]

    # ----------------------------------------------------
    # Gestión de Productos
    # ----------------------------------------------------
    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        if codigo is None:
            return None
        return self._productos.get(codigo.strip())

    def registrar_producto(self, producto: Producto) -> bool:
        if producto.codigo in self._productos:
            return False
        self._productos[producto.codigo] = producto
        self._guardar_productos()
        return True

    def actualizar_producto(self, codigo: str, *, nombre: Optional[str] = None,
                            categoria: Optional[str] = None,
                            precio: Optional[float] = None,
                            stock: Optional[int] = None) -> bool:
        producto = self._productos.get((codigo or "").strip())
        if producto is None:
            return False

        if nombre is not None and nombre.strip() != "":
            producto.nombre = nombre.strip()
        if categoria is not None and categoria.strip() != "":
            producto.categoria = categoria.strip()
        if precio is not None:
            try:
                precio_nuevo = float(precio)
                if precio_nuevo < 0:
                    raise ValueError("El precio no puede ser negativo")
                producto.precio = precio_nuevo
            except (TypeError, ValueError):
                return False
        if stock is not None:
            try:
                stock_nuevo = int(stock)
                if stock_nuevo < 0:
                    raise ValueError("El stock no puede ser negativo")
                producto.stock = stock_nuevo
            except (TypeError, ValueError):
                return False

        self._guardar_productos()
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        clave = (codigo or "").strip()
        if clave not in self._productos:
            return False
        del self._productos[clave]
        self._guardar_productos()
        return True

    def listar_productos(self) -> List[Producto]:
        return list(self._productos.values())

    def obtener_productos_texto(self) -> List[str]:
        if not self._productos:
            return ["No hay productos registrados."]
        return [producto.mostrar_informacion() for producto in self._productos.values()]

    # ----------------------------------------------------
    # Gestión de Ventas (Semana 15 - Eventos y Persistencia)
    # ----------------------------------------------------
    def generar_codigo_venta(self) -> str:
        """Genera un código consecutivo único para la venta: V001, V002, etc."""
        numeros = []
        for venta in self._ventas:
            code = venta.codigo.strip()
            if code.startswith("V") and code[1:].isdigit():
                numeros.append(int(code[1:]))
        siguiente = max(numeros) + 1 if numeros else 1
        return f"V{siguiente:03d}"

    def registrar_venta(self, usuario_clave: str, producto_codigo: str, cantidad: int) -> Tuple[bool, str, Optional[Venta]]:
        """
        Valida las reglas de negocio de la venta y persiste la operación.
        - Comprueba existencia de usuario.
        - Comprueba existencia de producto.
        - Comprueba stock disponible.
        - Descuenta stock del producto.
        - Guarda tanto ventas como productos actualizados.
        """
        usuario = self.buscar_usuario(usuario_clave)
        if usuario is None:
            return False, f"El cliente/usuario '{usuario_clave}' no existe en el sistema.", None

        producto = self.buscar_producto(producto_codigo)
        if producto is None:
            return False, f"El producto con código '{producto_codigo}' no existe en el menú.", None

        try:
            cant = int(cantidad)
        except (TypeError, ValueError):
            return False, "La cantidad a vender debe ser un número entero válido.", None

        if cant <= 0:
            return False, "La cantidad a vender debe ser mayor a 0.", None

        if producto.stock < cant:
            return (
                False,
                f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock}, Solicitado: {cant}.",
                None,
            )

        codigo_venta = self.generar_codigo_venta()
        total_venta = round(cant * producto.precio, 2)

        try:
            nueva_venta = Venta(
                codigo=codigo_venta,
                usuario=usuario.usuario,
                producto_codigo=producto.codigo,
                producto_nombre=producto.nombre,
                cantidad=cant,
                precio_unitario=producto.precio,
                total=total_venta,
            )
        except ValueError as err:
            return False, f"Error en los datos de la venta: {err}", None

        # Descontar stock del producto
        producto.stock -= cant

        # Persistir venta y producto actualizado
        self._ventas.append(nueva_venta)
        self._guardar_ventas()
        self._guardar_productos()

        mensaje_exito = (
            f"Venta {codigo_venta} registrada con éxito: {cant}x {producto.nombre} "
            f"para {usuario.nombre} por S/. {total_venta:.2f}."
        )
        return True, mensaje_exito, nueva_venta

    def listar_ventas(self) -> List[Venta]:
        return list(self._ventas)

    def buscar_venta(self, codigo: str) -> Optional[Venta]:
        for venta in self._ventas:
            if venta.codigo.strip() == (codigo or "").strip():
                return venta
        return None

    def obtener_total_recaudado(self) -> float:
        return sum(v.total for v in self._ventas)

    def obtener_ventas_texto(self) -> List[str]:
        if not self._ventas:
            return ["No hay ventas registradas."]
        return [v.mostrar_informacion() for v in self._ventas]
