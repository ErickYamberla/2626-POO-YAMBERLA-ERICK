import tkinter as tk
from tkinter import ttk
from pathlib import Path


class LoginView(tk.Frame):
    def __init__(self, parent, restaurante_servicio, on_login):
        super().__init__(parent, bg="#f3f4f6", padx=20, pady=20)
        self.restaurante_servicio = restaurante_servicio
        self.on_login = on_login

        self.assets_dir = Path(__file__).resolve().parent.parent / "assets"

        # Contenedor centrado tipo tarjeta
        self.card = tk.Frame(self, bg="white", padx=36, pady=30, relief="solid", borderwidth=1)
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # Cargar logo de la carpeta assets
        self.logo_image = None
        logo_path = self.assets_dir / "logo.png"
        if logo_path.exists():
            try:
                self.logo_image = tk.PhotoImage(file=str(logo_path))
                logo_label = tk.Label(self.card, image=self.logo_image, bg="white")
                logo_label.pack(pady=(0, 10))
            except Exception as e:
                print(f"No se pudo cargar el logo: {e}")

        title = tk.Label(
            self.card,
            text="Restaurante App",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#111827",
        )
        title.pack(pady=(0, 2))

        subtitle = tk.Label(
            self.card,
            text="Gestión Integral de Productos y Ventas",
            font=("Segoe UI", 10),
            bg="white",
            fg="#6b7280",
        )
        subtitle.pack(pady=(0, 16))

        # Campos de formulario
        tk.Label(self.card, text="Usuario:", font=("Segoe UI", 9, "bold"), bg="white", fg="#374151", anchor="w").pack(fill="x", pady=(4, 2))
        self.usuario_entry = ttk.Entry(self.card, width=38, font=("Segoe UI", 10))
        self.usuario_entry.pack(fill="x", pady=(0, 8))

        tk.Label(self.card, text="Contraseña:", font=("Segoe UI", 9, "bold"), bg="white", fg="#374151", anchor="w").pack(fill="x", pady=(4, 2))
        self.password_entry = ttk.Entry(self.card, width=38, show="*", font=("Segoe UI", 10))
        self.password_entry.pack(fill="x", pady=(0, 14))

        # Botón de ingreso con callback command=
        self.login_button = ttk.Button(self.card, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.login_button.pack(fill="x", pady=(4, 8), ipady=3)

        # Mensaje de retroalimentación
        self.mensaje_var = tk.StringVar(value="")
        self.mensaje_label = tk.Label(
            self.card,
            textvariable=self.mensaje_var,
            bg="white",
            fg="#dc2626",
            font=("Segoe UI", 9),
            wraplength=320,
            justify="center",
        )
        self.mensaje_label.pack(fill="x", pady=(4, 10))

        # Panel informativo con las credenciales solicitadas por el usuario
        credenciales_frame = tk.LabelFrame(
            self.card,
            text=" 🔑 Credenciales para iniciar sesión ",
            bg="#f8fafc",
            fg="#0f172a",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=8,
            relief="groove",
            borderwidth=1,
        )
        credenciales_frame.pack(fill="x", pady=(6, 0))

        texto_credenciales = (
            "• admin      |  admin123   (Administrador General)\n"
            "• carlos     |  carlos456  (Carlos Gómez)\n"
            "• empleado  |  1234       (Empleado de Turno)\n"
            "• erick      |  erick2026  (Erick Yamberla)"
        )
        self.credenciales_label = tk.Label(
            credenciales_frame,
            text=texto_credenciales,
            font=("Consolas", 8),
            bg="#f8fafc",
            fg="#334155",
            justify="left",
            anchor="w",
        )
        self.credenciales_label.pack(fill="x", pady=(2, 4))

        # Atajo rápido: presionar Enter para iniciar sesión
        self.usuario_entry.bind("<Return>", lambda e: self.iniciar_sesion())
        self.password_entry.bind("<Return>", lambda e: self.iniciar_sesion())

        self.usuario_entry.focus_set()

    def iniciar_sesion(self) -> None:
        usuario = self.usuario_entry.get().strip()
        password = self.password_entry.get().strip()

        if not usuario or not password:
            self.mensaje_var.set("Debe completar usuario y contraseña.")
            self.mensaje_label.config(fg="#dc2626")
            return

        if self.restaurante_servicio.validar_acceso(usuario, password):
            self.mensaje_var.set("Acceso concedido.")
            self.mensaje_label.config(fg="#16a34a")
            self.on_login()
            return

        self.mensaje_var.set("Usuario o contraseña incorrectos.")
        self.mensaje_label.config(fg="#dc2626")

    def limpiar(self) -> None:
        self.usuario_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.mensaje_var.set("")
        self.usuario_entry.focus_set()
