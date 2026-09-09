import tkinter as tk
from tkinter import ttk


class MainView(tk.Frame):
    def __init__(self, parent, restaurante_servicio, on_logout):
        super().__init__(parent, bg="#f3f4f6")
        self.restaurante_servicio = restaurante_servicio
        self.on_logout = on_logout

        self.toolbar = tk.Frame(self, bg="#111827", padx=10, pady=10)
        self.toolbar.pack(fill="x")

        ttk.Button(self.toolbar, text="Productos", command=self.mostrar_productos).pack(side="left", padx=(0, 8))
        ttk.Button(self.toolbar, text="Usuarios", command=self.mostrar_usuarios).pack(side="left", padx=(0, 8))
        ttk.Button(self.toolbar, text="Ventas (pendiente)", command=self.mostrar_ventas_pendiente).pack(side="left", padx=(0, 8))
        ttk.Button(self.toolbar, text="Cerrar sesión", command=self.on_logout).pack(side="right")

        self.contenido = tk.Text(self, height=20, width=100, wrap="word", state="disabled")
        self.contenido.pack(fill="both", expand=True, padx=20, pady=20)

        self.mostrar_productos()

    def _mostrar_texto(self, texto: str) -> None:
        self.contenido.config(state="normal")
        self.contenido.delete("1.0", tk.END)
        self.contenido.insert(tk.END, texto)
        self.contenido.config(state="disabled")

    def mostrar_productos(self) -> None:
        productos = self.restaurante_servicio.obtener_productos_texto()
        texto = "\n".join(productos)
        self._mostrar_texto("Productos registrados:\n\n" + texto)

    def mostrar_usuarios(self) -> None:
        usuarios = self.restaurante_servicio.obtener_usuarios_texto()
        texto = "\n".join(usuarios)
        self._mostrar_texto("Usuarios registrados:\n\n" + texto)

    def mostrar_ventas_pendiente(self) -> None:
        self._mostrar_texto("Ventas\n\nEsta funcionalidad aún está pendiente de desarrollo en esta versión gráfica.")
