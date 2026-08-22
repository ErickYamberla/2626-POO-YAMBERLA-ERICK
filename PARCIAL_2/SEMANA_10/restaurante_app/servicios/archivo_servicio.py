from pathlib import Path
import json
from typing import List, Dict, Any, Optional


class ArchivoServicio:
    """Servicio encargado de leer y escribir productos en JSON dentro de datos/."""

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        base = Path(__file__).parent.parent if base_dir is None else Path(base_dir)
        self._datos_dir = base / "datos"
        self._datos_dir.mkdir(parents=True, exist_ok=True)
        self._productos_file = self._datos_dir / "productos.json"

    def cargar_productos(self) -> List[Dict[str, Any]]:
        try:
            if not self._productos_file.exists():
                return []
            with self._productos_file.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            # admitir tanto lista como diccionario (versiones previas usan dict codigo->registro)
            if isinstance(data, dict):
                # convertir a lista de registros
                return list(data.values())
            if not isinstance(data, list):
                print("Formato inválido en productos.json: se esperaba lista o diccionario.")
                return []
            return data
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Error: productos.json tiene formato JSON inválido. Se omiten registros.")
            return []
        except PermissionError:
            print("Error: sin permisos para leer productos.json.")
            raise
        except OSError as e:
            print(f"Error al leer productos.json: {e}")
            return []

    def guardar_productos(self, productos: List[Dict[str, Any]]) -> None:
        try:
            with self._productos_file.open("w", encoding="utf-8") as fh:
                json.dump(productos, fh, ensure_ascii=False, indent=2)
        except PermissionError:
            raise
        except OSError as e:
            print(f"Error al escribir productos.json: {e}")
