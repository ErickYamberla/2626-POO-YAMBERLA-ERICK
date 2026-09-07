from __future__ import annotations
from typing import Dict, List, Optional
from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class Restaurante:
    """Servicio que administra productos, usuarios y ventas con persistencia en JSON."""

    SISTEMA_INFO: tuple = ("RestauranteApp", "Semana 11")

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        base = Path(__file__).parent.parent
        self._base_dir = base if base_dir is None else Path(base_dir)
        self._archivo = ArchivoServicio(self._base_dir)

        # colecciones internas
        self._productos: Dict[str, Producto] = {}
        self._usuarios: Dict[str, Usuario] = {}
        self._ventas: List[Venta] = []
        # índices auxiliares en memoria
        # mapea identificacion_usuario -> lista de ventas (mejora consultas por usuario)
        self._ventas_por_usuario: Dict[str, List[Venta]] = {}

        # cargar productos
        raw_p = self._archivo.cargar_productos()
        for entry in raw_p:
            try:
                producto = Producto.from_dict(entry)
                self._productos[producto.codigo] = producto
            except KeyError as e:
                print(f"Registro de producto omitido por clave faltante: {e}")
            except ValueError as e:
                print(f"Registro de producto inválido y omitido: {e}")

        # cargar usuarios
        raw_u = self._archivo.cargar_usuarios()
        for entry in raw_u:
            try:
                usuario = Usuario.from_dict(entry)
                if usuario:
                    self._usuarios[usuario.identificacion] = usuario
            except KeyError as e:
                print(f"Registro de usuario omitido por clave faltante: {e}")
            except ValueError as e:
                print(f"Registro de usuario inválido y omitido: {e}")

        # cargar ventas
        raw_v = self._archivo.cargar_ventas()
        for entry in raw_v:
            try:
                venta = Venta.from_dict(entry)
                if venta:
                    self._ventas.append(venta)
                    # actualizar índice por usuario
                    self._ventas_por_usuario.setdefault(venta.usuario_id, []).append(venta)
            except KeyError as e:
                print(f"Registro de venta omitido por clave faltante: {e}")
            except ValueError as e:
                print(f"Registro de venta inválido y omitido: {e}")

    # persistencia
    def _persistir_productos(self) -> None:
        try:
            lista = [p.to_dict() for p in self._productos.values()]
            self._archivo.guardar_productos(lista)
        except PermissionError:
            print("No hay permisos para escribir productos.json. Los cambios no se guardaron.")

    def _persistir_usuarios(self) -> None:
        try:
            lista = [u.to_dict() for u in self._usuarios.values()]
            self._archivo.guardar_usuarios(lista)
        except PermissionError:
            print("No hay permisos para escribir usuarios.json. Los cambios no se guardaron.")

    def _persistir_ventas(self) -> None:
        try:
            lista = [v.to_dict() for v in self._ventas]
            self._archivo.guardar_ventas(lista)
        except PermissionError:
            print("No hay permisos para escribir ventas.json. Los cambios no se guardaron.")

    # productos
    def registrar_producto(self, producto: Producto) -> bool:
        if producto.codigo in self._productos:
            return False
        self._productos[producto.codigo] = producto
        self._persistir_productos()
        return True

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        return self._productos.get(codigo)

    def actualizar_producto(self, codigo: str, *, nombre: Optional[str] = None,
                            categoria: Optional[str] = None, precio: Optional[float] = None,
                            stock: Optional[int] = None) -> bool:
        producto = self._productos.get(codigo)
        if not producto:
            return False
        if nombre is not None and nombre != "":
            producto.nombre = nombre
        if categoria is not None and categoria != "":
            producto.categoria = categoria
        if precio is not None:
            try:
                precio_val = float(precio)
                if precio_val < 0:
                    raise ValueError("Precio negativo")
                producto.precio = precio_val
            except (TypeError, ValueError):
                print("Precio inválido; no se actualizó el precio.")
        if stock is not None:
            try:
                stock_val = int(stock)
                if stock_val < 0:
                    raise ValueError("Stock negativo")
                producto.stock = stock_val
            except (TypeError, ValueError):
                print("Stock inválido; no se actualizó el stock.")
        self._persistir_productos()
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        if codigo not in self._productos:
            return False
        del self._productos[codigo]
        self._persistir_productos()
        return True

    def listar_productos(self) -> List[str]:
        return [p.mostrar_informacion() for p in self._productos.values()]

    def mostrar_categorias(self) -> List[str]:
        categorias = {p.categoria for p in self._productos.values() if p.categoria}
        return sorted(categorias)

    # usuarios
    def registrar_usuario(self, usuario: Usuario) -> bool:
        if usuario.identificacion in self._usuarios:
            return False
        self._usuarios[usuario.identificacion] = usuario
        self._persistir_usuarios()
        return True

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        return self._usuarios.get(identificacion)

    def actualizar_usuario(self, identificacion: str, *, nombre: Optional[str] = None,
                            correo: Optional[str] = None) -> bool:
        usuario = self._usuarios.get(identificacion)
        if not usuario:
            return False
        if nombre is not None and nombre != "":
            usuario.nombre = nombre
        if correo is not None and correo != "":
            usuario.correo = correo
        self._persistir_usuarios()
        return True

    def eliminar_usuario(self, identificacion: str) -> bool:
        if identificacion not in self._usuarios:
            return False
        del self._usuarios[identificacion]
        self._persistir_usuarios()
        return True

    def listar_usuarios(self) -> List[str]:
        return [u.mostrar_informacion() for u in self._usuarios.values()]

    # ventas
    def registrar_venta(self, codigo_producto: str, identificacion_usuario: str, cantidad: int) -> bool:
        return self.vender_producto(codigo_producto, identificacion_usuario, cantidad)

    def vender_producto(self, codigo_producto: str, identificacion_usuario: str, cantidad: int) -> bool:
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)
        if usuario is None or producto is None:
            return False
        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            return False
        if cantidad <= 0 or producto.stock < cantidad:
            return False
        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        # registrar venta en la lista principal
        self._ventas.append(venta)
        # actualizar índice auxiliar por usuario
        self._ventas_por_usuario.setdefault(usuario.identificacion, []).append(venta)
        try:
            producto.vender(cantidad)
        except ValueError:
            # revertir en lista principal
            self._ventas.pop()
            # revertir en índice auxiliar
            lst = self._ventas_por_usuario.get(usuario.identificacion)
            if lst:
                try:
                    lst.pop()
                    if not lst:
                        del self._ventas_por_usuario[usuario.identificacion]
                except IndexError:
                    pass
            return False
        self._persistir_ventas()
        self._persistir_productos()
        return True

    def ventas_por_usuario(self, identificacion_usuario: str) -> List[Venta]:
        # consulta optimizada usando el índice en memoria construido al cargar y actualizar ventas
        return list(self._ventas_por_usuario.get(identificacion_usuario, []))

    # utilitarios para conversiones (compatibilidad con versiones previas)
    @staticmethod
    def _producto_a_dict(producto: Producto) -> Dict:
        return producto.to_dict()

    @staticmethod
    def _dict_a_producto(data: Optional[Dict]) -> Optional[Producto]:
        if not data:
            return None
        try:
            return Producto.from_dict(data)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _usuario_a_dict(usuario: Usuario) -> Dict:
        return usuario.to_dict()

    @staticmethod
    def _dict_a_usuario(data: Optional[Dict]) -> Optional[Usuario]:
        return Usuario.from_dict(data)
