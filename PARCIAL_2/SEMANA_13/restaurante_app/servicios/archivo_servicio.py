from pathlib import Path
import json
from typing import Any, Dict, List, Optional


class ArchivoServicio:
    """Servicio encargado de leer y escribir productos y usuarios en JSON."""

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        base = Path(__file__).resolve().parent.parent if base_dir is None else Path(base_dir)
        self._datos_dir = base / "datos"
        self._datos_dir.mkdir(parents=True, exist_ok=True)
        self._productos_file = self._datos_dir / "productos.json"
        self._usuarios_file = self._datos_dir / "usuarios.json"

    def _cargar_json(self, path: Path) -> List[Dict[str, Any]]:
        try:
            if not path.exists():
                return []
            with path.open("r", encoding="utf-8-sig") as file_handler:
                data = json.load(file_handler)
            if isinstance(data, dict):
                return list(data.values())
            if not isinstance(data, list):
                print(f"Formato inválido en {path.name}: se esperaba lista o diccionario.")
                return []
            return data
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"Error: {path.name} tiene formato JSON inválido. Se omiten registros.")
            return []
        except PermissionError:
            print(f"Error: sin permisos para leer {path.name}.")
            raise
        except OSError as exc:
            print(f"Error al leer {path.name}: {exc}")
            return []

    def _guardar_json(self, path: Path, elementos: List[Dict[str, Any]]) -> None:
        try:
            with path.open("w", encoding="utf-8") as file_handler:
                json.dump(elementos, file_handler, ensure_ascii=False, indent=2)
        except PermissionError:
            raise
        except OSError as exc:
            print(f"Error al escribir {path.name}: {exc}")

    def cargar_productos(self) -> List[Dict[str, Any]]:
        return self._cargar_json(self._productos_file)

    def guardar_productos(self, productos: List[Dict[str, Any]]) -> None:
        self._guardar_json(self._productos_file, productos)

    def cargar_usuarios(self) -> List[Dict[str, Any]]:
        return self._cargar_json(self._usuarios_file)

    def guardar_usuarios(self, usuarios: List[Dict[str, Any]]) -> None:
        self._guardar_json(self._usuarios_file, usuarios)
