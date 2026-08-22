from __future__ import annotations
from typing import Dict, List, Optional
from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio


class Restaurante:
    """Servicio que administra productos y clientes con persistencia en JSON.

        Internamente los productos y clientes se almacenan como diccionarios
    (clave -> valor) donde la clave es el identificador único
        (código del producto o identificación del cliente).
    """

    SISTEMA_INFO: tuple = ("RestauranteApp", "Semana 10")

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        base = Path(__file__).parent.parent
        self._base_dir = base if base_dir is None else Path(base_dir)
        self._archivo = ArchivoServicio(self._base_dir)

        # colección interna: codigo -> Producto
        self._productos: Dict[str, Producto] = {}
        self._clientes: Dict[str, Usuario] = {}

        # cargar productos desde el archivo
        raw = self._archivo.cargar_productos()
        for entry in raw:
            try:
                producto = Producto.from_dict(entry)
                self._productos[producto.codigo] = producto
            except KeyError as e:
                print(f"Registro de producto omitido por clave faltante: {e}")
            except ValueError as e:
                print(f"Registro de producto inválido y omitido: {e}")

    def _persistir_productos(self) -> None:
        try:
            lista = [p.to_dict() for p in self._productos.values()]
            self._archivo.guardar_productos(lista)
        except PermissionError:
            print("No hay permisos para escribir productos.json. Los cambios no se guardaron.")

    def registrar_producto(self, producto: Producto) -> bool:
        if producto.codigo in self._productos:
            return False
        self._productos[producto.codigo] = producto
        self._persistir_productos()
        return True

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        return self._productos.get(codigo)

    def actualizar_producto(self, codigo: str, *, nombre: Optional[str] = None,
                            categoria: Optional[str] = None, precio: Optional[float] = None) -> bool:
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

    def registrar_cliente(self, usuario: Usuario) -> bool:
        if usuario.identificacion in self._clientes:
            return False
        self._clientes[usuario.identificacion] = usuario
        return True

    def buscar_cliente(self, identificacion: str) -> Optional[Usuario]:
        return self._clientes.get(identificacion)

    def actualizar_cliente(self, identificacion: str, *, nombre: Optional[str] = None,
                           correo: Optional[str] = None) -> bool:
        usuario = self._clientes.get(identificacion)
        if not usuario:
            return False
        if nombre is not None and nombre != "":
            usuario.nombre = nombre
        if correo is not None and correo != "":
            usuario.correo = correo
        return True

    def eliminar_cliente(self, identificacion: str) -> bool:
        if identificacion not in self._clientes:
            return False
        del self._clientes[identificacion]
        return True

    def listar_clientes(self) -> List[str]:
        return [u.mostrar_informacion() for u in self._clientes.values()]

    @staticmethod
    def _producto_a_dict(producto: Producto) -> Dict:
        return {
            "codigo": producto.codigo,
            "nombre": producto.nombre,
            "categoria": producto.categoria,
            "precio": float(producto.precio),
        }

    @staticmethod
    def _dict_a_producto(data: Optional[Dict]) -> Optional[Producto]:
        if not data:
            return None
        try:
            return Producto(
                codigo=str(data.get("codigo", "")),
                nombre=str(data.get("nombre", "")),
                categoria=str(data.get("categoria", "")),
                precio=float(data.get("precio", 0.0)),
            )
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _cliente_a_dict(cliente: Cliente) -> Dict:
        return {
                "identificacion": cliente.identificacion,
                "nombre": cliente.nombre,
                "correo": cliente.correo,
        }

    @staticmethod
    def _dict_a_cliente(data: Optional[Dict]) -> Optional[Cliente]:
        if not data:
            return None
        try:
            return Cliente(
                identificacion=str(data.get("identificacion", "")),
                nombre=str(data.get("nombre", "")),
                correo=str(data.get("correo", "")),
            )
        except (TypeError, ValueError):
            return None


