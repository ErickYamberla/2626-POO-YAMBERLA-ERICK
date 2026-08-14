from __future__ import annotations
from typing import Dict, List, Optional
from pathlib import Path
import json

from modelos.producto import Producto
from modelos.cliente import Cliente


class Restaurante:
    """Servicio que administra productos y clientes con persistencia en JSON.

        Internamente los productos y clientes se almacenan como diccionarios
    (clave -> valor) donde la clave es el identificador único
        (código del producto o identificación del cliente).
    """

    # Información estable del sistema representada como tupla
    SISTEMA_INFO: tuple = ("RestauranteApp", "Semana 9")

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        base = Path(__file__).parent.parent
        self._data_dir = (base / "data") if data_dir is None else Path(data_dir)
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._productos_file = self._data_dir / "productos.json"
        self._clientes_file = self._data_dir / "clientes.json"

        # cargar estructuras desde archivos JSON (diccionarios)
        self._productos: Dict[str, Dict] = self._cargar_json(self._productos_file)
        self._clientes: Dict[str, Dict] = self._cargar_json(self._clientes_file)

    # ---------- helpers para JSON ----------
    def _cargar_json(self, path: Path) -> Dict[str, Dict]:
        try:
            if not path.exists():
                return {}
            with path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            if not isinstance(data, dict):
                return {}
            return data
        except (json.JSONDecodeError, OSError):
            return {}

    def _guardar_json(self, path: Path, data: Dict[str, Dict]) -> None:
        with path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)

    # ---------- productos ----------
    def registrar_producto(self, producto: Producto) -> bool:
        """Registra un producto si su código no existe (clave → valor)."""
        if producto.codigo in self._productos:
            return False
        self._productos[producto.codigo] = self._producto_a_dict(producto)
        self._guardar_json(self._productos_file, self._productos)
        return True

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        entry = self._productos.get(codigo)
        return self._dict_a_producto(entry) if entry else None

    def actualizar_producto(self, codigo: str, *, nombre: Optional[str] = None,
                            categoria: Optional[str] = None, precio: Optional[float] = None) -> bool:
        if codigo not in self._productos:
            return False
        if nombre is not None and nombre != "":
            self._productos[codigo]["nombre"] = nombre
        if categoria is not None and categoria != "":
            self._productos[codigo]["categoria"] = categoria
        if precio is not None:
            try:
                self._productos[codigo]["precio"] = float(precio)
            except (TypeError, ValueError):
                pass
        self._guardar_json(self._productos_file, self._productos)
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        if codigo not in self._productos:
            return False
        del self._productos[codigo]
        self._guardar_json(self._productos_file, self._productos)
        return True

    def listar_productos(self) -> List[str]:
        """Devuelve las representaciones legibles de los productos.

        No se exponen las estructuras internas; se utiliza el servicio para formatear.
        """
        resultados: List[str] = []
        for info in self._productos.values():
            p = self._dict_a_producto(info)
            if p:
                resultados.append(p.mostrar_informacion())
        return resultados

    def mostrar_categorias(self) -> List[str]:
        categorias = {info.get("categoria") for info in self._productos.values() if info.get("categoria")}
        return sorted(categorias)

    # ---------- clientes ----------
    def registrar_cliente(self, cliente: Cliente) -> bool:
        if cliente.identificacion in self._clientes:
            return False
        self._clientes[cliente.identificacion] = self._cliente_a_dict(cliente)
        self._guardar_json(self._clientes_file, self._clientes)
        return True

    def buscar_cliente(self, identificacion: str) -> Optional[Cliente]:
        entry = self._clientes.get(identificacion)
        return self._dict_a_cliente(entry) if entry else None

    def actualizar_cliente(self, identificacion: str, *, nombre: Optional[str] = None,
                           correo: Optional[str] = None) -> bool:
        if identificacion not in self._clientes:
            return False
        if nombre is not None and nombre != "":
            self._clientes[identificacion]["nombre"] = nombre
        if correo is not None and correo != "":
            self._clientes[identificacion]["correo"] = correo
        self._guardar_json(self._clientes_file, self._clientes)
        return True

    def eliminar_cliente(self, identificacion: str) -> bool:
        if identificacion not in self._clientes:
            return False
        del self._clientes[identificacion]
        self._guardar_json(self._clientes_file, self._clientes)
        return True

    def listar_clientes(self) -> List[str]:
        resultados: List[str] = []
        for info in self._clientes.values():
            u = self._dict_a_cliente(info)
            if u:
                resultados.append(u.mostrar_informacion())
        return resultados

    # ---------- utilitarios de conversión ----------
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


