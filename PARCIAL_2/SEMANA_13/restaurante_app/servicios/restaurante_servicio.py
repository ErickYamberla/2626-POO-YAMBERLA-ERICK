from pathlib import Path
from typing import Dict, List, Optional

try:
    from restaurante_app.modelos.producto import Producto
    from restaurante_app.modelos.usuario import Usuario
    from restaurante_app.servicios.archivo_servicio import ArchivoServicio
except ModuleNotFoundError:
    from modelos.producto import Producto
    from modelos.usuario import Usuario
    from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """Servicio del restaurante para validar acceso y consultar los datos base."""

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        base = Path(__file__).resolve().parent.parent if base_dir is None else Path(base_dir)
        self._archivo = ArchivoServicio(base)
        self._productos: Dict[str, Producto] = {}
        self._usuarios: Dict[str, Usuario] = {}
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

    def validar_acceso(self, usuario: str, password: str) -> bool:
        usuario_obj = self._usuarios.get(usuario.strip())
        if usuario_obj is None:
            return False
        return usuario_obj.password == password.strip()

    def buscar_usuario(self, usuario: str) -> Optional[Usuario]:
        return self._usuarios.get(usuario.strip())

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        return self._productos.get(codigo.strip())

    def listar_usuarios(self) -> List[Usuario]:
        return list(self._usuarios.values())

    def listar_productos(self) -> List[Producto]:
        return list(self._productos.values())

    def obtener_usuarios_texto(self) -> List[str]:
        if not self._usuarios:
            return ["No hay usuarios registrados."]
        return [usuario.mostrar_informacion() for usuario in self._usuarios.values()]

    def obtener_productos_texto(self) -> List[str]:
        if not self._productos:
            return ["No hay productos registrados."]
        return [producto.mostrar_informacion() for producto in self._productos.values()]
