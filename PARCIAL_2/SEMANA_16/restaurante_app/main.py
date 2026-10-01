import sys
from pathlib import Path
import tkinter as tk

# Asegurar que el directorio de restaurante_app esté en el PYTHONPATH
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

try:
    from restaurante_app.servicios.restaurante_servicio import RestauranteServicio
    from restaurante_app.ui.login_view import LoginView
    from restaurante_app.ui.main_view import MainView
except ModuleNotFoundError:
    from servicios.restaurante_servicio import RestauranteServicio
    from ui.login_view import LoginView
    from ui.main_view import MainView


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Restaurante App - Semana 16")
        self.root.geometry("1260x780")
        self.root.minsize(1040, 660)

        # Establecer ícono de la aplicación desde la carpeta assets
        self.icon_img = None
        icon_path = APP_DIR / "assets" / "icon_app.png"
        if icon_path.exists():
            try:
                self.icon_img = tk.PhotoImage(file=str(icon_path))
                self.root.iconphoto(True, self.icon_img)
            except Exception as exc:
                print(f"No se pudo asignar el ícono de ventana: {exc}")

        self.servicio = RestauranteServicio()
        self.login_view = LoginView(self.root, self.servicio, self.mostrar_main_view)
        self.main_view = MainView(self.root, self.servicio, self.mostrar_login_view)

        self.mostrar_login_view()

    def mostrar_login_view(self) -> None:
        self.servicio.cerrar_sesion()
        self.main_view.pack_forget()
        self.login_view.pack(fill="both", expand=True)
        self.login_view.limpiar()
        self.root.title("Restaurante App - Semana 16 | Iniciar Sesión")

    def mostrar_main_view(self) -> None:
        self.login_view.pack_forget()
        self.main_view.pack(fill="both", expand=True)
        self.main_view.actualizar_sesion_activa()
        self.main_view.refrescar_todo()
        self.root.title("Restaurante App - Semana 16 | Panel Principal")


def main() -> None:
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
