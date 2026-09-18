import tkinter as tk
from tkinter import ttk


class LoginView(tk.Frame):
    def __init__(self, parent, restaurante_servicio, on_login):
        super().__init__(parent, bg="#f2f4f8", padx=30, pady=40)
        self.restaurante_servicio = restaurante_servicio
        self.on_login = on_login

        self.configure(borderwidth=2, relief="flat")
        self.card = tk.Frame(self, bg="white", padx=30, pady=30)
        self.card.pack(fill="both", expand=True)

        title = tk.Label(
            self.card,
            text="Restaurante App",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#1f2937",
        )
        title.pack(pady=(0, 20))

        subtitle = tk.Label(
            self.card,
            text="Iniciar sesi?n",
            font=("Arial", 11),
            bg="white",
            fg="#4b5563",
        )
        subtitle.pack(pady=(0, 20))

        tk.Label(self.card, text="Usuario:", bg="white", anchor="w").pack(fill="x", pady=(8, 2))
        self.usuario_entry = ttk.Entry(self.card, width=40)
        self.usuario_entry.pack(fill="x", pady=(0, 10))

        tk.Label(self.card, text="Contrase?a:", bg="white", anchor="w").pack(fill="x", pady=(8, 2))
        self.password_entry = ttk.Entry(self.card, width=40, show="*")
        self.password_entry.pack(fill="x", pady=(0, 12))

        self.login_button = ttk.Button(self.card, text="Ingresar", command=self.iniciar_sesion)
        self.login_button.pack(fill="x", pady=(8, 8))

        self.mensaje_var = tk.StringVar(value="")
        self.mensaje_label = tk.Label(
            self.card,
            textvariable=self.mensaje_var,
            bg="white",
            fg="#dc2626",
            wraplength=280,
            justify="center",
        )
        self.mensaje_label.pack(fill="x", pady=(8, 0))

        self.usuario_entry.focus_set()

    def iniciar_sesion(self) -> None:
        usuario = self.usuario_entry.get().strip()
        password = self.password_entry.get().strip()

        if not usuario or not password:
            self.mensaje_var.set("Debe completar usuario y contrase?a.")
            return

        if self.restaurante_servicio.validar_acceso(usuario, password):
            self.mensaje_var.set("Acceso correcto.")
            self.on_login()
            return

        self.mensaje_var.set("Usuario o contrase?a incorrectos.")

    def limpiar(self) -> None:
        self.usuario_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.mensaje_var.set("")
        self.usuario_entry.focus_set()
