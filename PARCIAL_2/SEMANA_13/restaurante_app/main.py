import tkinter as tk

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
        self.root.title("Restaurante App - Semana 13")
        self.root.geometry("900x520")
        self.root.minsize(700, 440)

        self.servicio = RestauranteServicio()
        self.login_view = LoginView(self.root, self.servicio, self.mostrar_main_view)
        self.main_view = MainView(self.root, self.servicio, self.mostrar_login_view)

        self.mostrar_login_view()

    def mostrar_login_view(self) -> None:
        self.main_view.pack_forget()
        self.login_view.pack(fill="both", expand=True)
        self.login_view.limpiar()
        self.root.title("Restaurante App - Login")

    def mostrar_main_view(self) -> None:
        self.login_view.pack_forget()
        self.main_view.pack(fill="both", expand=True)
        self.main_view.mostrar_productos()
        self.root.title("Restaurante App - Panel principal")


def main() -> None:
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
