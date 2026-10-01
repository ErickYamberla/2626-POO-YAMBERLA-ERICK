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
    """
    Servicio central del restaurante para la lógica de negocio, validaciones y persistencia.
    Semana 16: Control de sesión activa, validación de roles y gestión de usuarios (CRUD)
    asegurando el flujo: evento -> callback -> servicio -> persistencia -> respuesta.
    """

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        base = Path(__file__).resolve().parent.parent if base_dir is None else Path(base_dir)
        self._archivo = ArchivoServicio(base)
        self._productos: Dict[str, Producto] = {}
        self._usuarios: Dict[str, Usuario] = {}
        self._ventas: List[Venta] = []
        self.usuario_actual: Optional[Usuario] = None
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
    # Gestión de Usuarios, Sesión y Autenticación (Semana 16)
    # ----------------------------------------------------
    def validar_acceso(self, usuario: str, password: str) -> bool:
        """Valida credenciales y almacena el usuario autenticado en la sesión actual."""
        usuario_obj = self.buscar_usuario(usuario)
        if usuario_obj is None:
            return False
        if usuario_obj.password == password.strip():
            self.usuario_actual = usuario_obj
            return True
        return False

    def cerrar_sesion(self) -> None:
        """Limpia el usuario actualmente autenticado al cerrar sesión."""
        self.usuario_actual = None

    def obtener_usuario_actual(self) -> Optional[Usuario]:
        """Retorna el usuario con sesión activa en el sistema."""
        return self.usuario_actual

    def es_administrador(self) -> bool:
        """Verifica si el usuario con sesión activa posee el rol de Administrador."""
        return self.usuario_actual is not None and self.usuario_actual.rol == "Administrador"

    def buscar_usuario(self, clave_o_id: str) -> Optional[Usuario]:
        """Busca un usuario por su nombre de usuario o por su identificador único (id)."""
        if not clave_o_id:
            return None
        termino = str(clave_o_id).strip()
        # Búsqueda directa por clave de diccionario (usuario)
        if termino in self._usuarios:
            return self._usuarios[termino]
        # Búsqueda por id o usuario ignorando mayúsculas
        termino_lower = termino.lower()
        for u in self._usuarios.values():
            if u.id.lower() == termino_lower or u.usuario.lower() == termino_lower:
                return u
        return None

    def generar_id_usuario(self) -> str:
        """Genera un código correlativo único para nuevos usuarios: USR-001, USR-002, etc."""
        numeros = []
        for u in self._usuarios.values():
            if u.id.startswith("USR-") and u.id[4:].isdigit():
                numeros.append(int(u.id[4:]))
        siguiente = max(numeros) + 1 if numeros else 1
        return f"USR-{siguiente:03d}"

    def registrar_usuario(self, usuario: Usuario) -> Tuple[bool, str]:
        """
        Registra un nuevo usuario en el sistema.
        Valida que el identificador/usuario no esté duplicado y persiste en usuarios.json.
        """
        clave = usuario.usuario.strip()
        if not clave:
            return False, "El nombre de usuario es obligatorio."

        if clave in self._usuarios:
            return False, f"El usuario '{clave}' ya se encuentra registrado."

        # Asignar ID correlativo si no tiene uno asignado
        if not usuario.id or usuario.id == usuario.usuario or not usuario.id.startswith("USR-"):
            usuario.id = self.generar_id_usuario()

        self._usuarios[clave] = usuario
        self._guardar_usuarios()
        return True, f"Usuario '{clave}' ({usuario.nombre}) registrado con rol '{usuario.rol}'."

    def actualizar_usuario(self, clave_o_id: str, *, password: Optional[str] = None,
                           nombre: Optional[str] = None, correo: Optional[str] = None,
                           rol: Optional[str] = None) -> Tuple[bool, str]:
        """
        Actualiza los datos de un usuario existente.
        Evita que el administrador autenticado se quite sus propios privilegios.
        Persiste los cambios en usuarios.json.
        """
        usuario_actual = self.buscar_usuario(clave_o_id)
        if usuario_actual is None:
            return False, f"No existe el usuario '{clave_o_id}' en el sistema."

        if password is not None and password.strip() != "":
            usuario_actual.password = password.strip()
        if nombre is not None and nombre.strip() != "":
            usuario_actual.nombre = nombre.strip()
        if correo is not None and correo.strip() != "":
            usuario_actual.correo = correo.strip()

        if rol is not None and rol.strip() != "":
            rol_limpio = rol.strip().capitalize()
            if rol_limpio in Usuario.ROLES_PERMITIDOS:
                # Regla de seguridad: Si es la cuenta en sesión activa, no degradar a Empleado o Cliente
                if self.usuario_actual and self.usuario_actual.usuario == usuario_actual.usuario and rol_limpio != "Administrador":
                    return False, "No puede retirar el rol de Administrador a su propia sesión activa."
                usuario_actual.rol = rol_limpio

        self._guardar_usuarios()
        return True, f"Usuario '{usuario_actual.usuario}' actualizado exitosamente."

    def eliminar_usuario(self, clave_o_id: str) -> Tuple[bool, str]:
        """
        Elimina un usuario del sistema bajo reglas de negocio estrictas.
        Regla de seguridad crítica: No permite eliminar la cuenta de la sesión activa.
        Persiste los cambios en usuarios.json.
        """
        clave = (clave_o_id or "").strip()
        if not clave:
            return False, "Debe especificar el usuario a eliminar."

        usuario_obj = self.buscar_usuario(clave)
        if usuario_obj is None:
            return False, f"El usuario '{clave}' no existe en el sistema."

        # Regla de seguridad: Impedir eliminar la cuenta activa
        if self.usuario_actual and self.usuario_actual.usuario == usuario_obj.usuario:
            return False, "No es posible eliminar la cuenta del usuario administrador actualmente autenticado en la sesión."

        del self._usuarios[usuario_obj.usuario]
        self._guardar_usuarios()
        return True, f"Usuario '{usuario_obj.usuario}' ({usuario_obj.nombre}) eliminado satisfactoriamente."

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
    # Gestión de Ventas (Eventos y Persistencia)
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
            f"para {usuario.nombre} por $ {total_venta:.2f}."
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
