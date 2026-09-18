import tkinter as tk
from tkinter import ttk

try:
    from restaurante_app.modelos.producto import Producto
    from restaurante_app.modelos.usuario import Usuario
except ModuleNotFoundError:
    from modelos.producto import Producto
    from modelos.usuario import Usuario


class MainView(tk.Frame):
    def __init__(self, parent, restaurante_servicio, on_logout):
        super().__init__(parent, bg="#edf2ff")
        self.restaurante_servicio = restaurante_servicio
        self.on_logout = on_logout

        self.toolbar = tk.Frame(self, bg="#111827", padx=16, pady=12)
        self.toolbar.pack(fill="x")

        title = tk.Label(
            self.toolbar,
            text="Restaurante App - Semana 14",
            fg="white",
            bg="#111827",
            font=("Arial", 12, "bold"),
        )
        title.pack(side="left")

        ttk.Button(self.toolbar, text="Inicio", command=self.mostrar_inicio).pack(side="right", padx=(0, 8))
        ttk.Button(self.toolbar, text="Productos", command=self.mostrar_productos).pack(side="right", padx=(0, 8))
        ttk.Button(self.toolbar, text="Usuarios", command=self.mostrar_usuarios).pack(side="right", padx=(0, 8))
        ttk.Button(self.toolbar, text="Cerrar sesi?n", command=self.on_logout).pack(side="right", padx=(0, 8))

        self.workspace = tk.Frame(self, bg="#edf2ff", padx=16, pady=16)
        self.workspace.pack(fill="both", expand=True)

        # Sections (do not pack yet)
        self.dashboard = None

        # Product section
        self.product_section = tk.Frame(self.workspace, bg="#edf2ff")
        self.product_panel = tk.Frame(self.product_section, bg="#edf2ff")
        # ensure the product panel is visible when the product section is shown
        self.product_panel.pack(fill="both", expand=True)
        self.form_container = tk.LabelFrame(self.product_panel, text="Formulario de productos", bg="white", padx=12, pady=12)
        self.form_container.pack(side="left", fill="y", padx=(0, 16))
        self.tabla_container = tk.LabelFrame(self.product_panel, text="Listado de productos", bg="white", padx=10, pady=10)
        self.tabla_container.pack(side="left", fill="both", expand=True)

        # User section
        self.user_section = tk.Frame(self.workspace, bg="#edf2ff")
        self.user_form_container = tk.LabelFrame(self.user_section, text="Formulario de usuarios", bg="white", padx=12, pady=12)
        self.user_form_container.pack(side="left", fill="y", padx=(0, 16))
        self.user_list_container = tk.LabelFrame(self.user_section, text="Usuarios registrados", bg="white", padx=10, pady=10)
        self.user_list_container.pack(side="left", fill="both", expand=True)

        # Variables
        self.codigo_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.stock_var = tk.StringVar()
        self.usuario_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.user_nombre_var = tk.StringVar()
        self.user_correo_var = tk.StringVar()

        # Configure forms and tables
        self._configurar_formulario_producto()
        self._configurar_tabla()
        self._configurar_formulario_usuario()
        # Usuarios: usar Treeview para mostrar encabezados y columnas como en Productos
        columns = ("usuario", "nombre", "correo")
        self.user_tree = ttk.Treeview(self.user_list_container, columns=columns, show="headings", height=18)
        self.user_tree.heading("usuario", text="Usuario")
        self.user_tree.heading("nombre", text="Nombre")
        self.user_tree.heading("correo", text="Correo")
        self.user_tree.column("usuario", width=120, anchor="center")
        self.user_tree.column("nombre", width=200, anchor="w")
        self.user_tree.column("correo", width=220, anchor="w")
        user_scroll = ttk.Scrollbar(self.user_list_container, orient="vertical", command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=user_scroll.set)
        self.user_tree.pack(side="left", fill="both", expand=True)
        user_scroll.pack(side="right", fill="y")

        self.status_var = tk.StringVar(value="Sistema listo.")
        self.status_label = tk.Label(self, textvariable=self.status_var, bg="#edf2ff", fg="#1f2937", anchor="w")
        self.status_label.pack(fill="x", padx=16, pady=(0, 10))

        self.mostrar_inicio()

    def _configurar_formulario_producto(self) -> None:
        campos = [
            ("Codigo", self.codigo_var),
            ("Nombre", self.nombre_var),
            ("Categoria", self.categoria_var),
            ("Precio", self.precio_var),
            ("Stock", self.stock_var),
        ]

        for label_text, variable in campos:
            label = tk.Label(self.form_container, text=f"{label_text}:", bg="white", anchor="w")
            label.pack(fill="x", pady=(0, 4))
            entry = ttk.Entry(self.form_container, textvariable=variable, width=28)
            entry.pack(fill="x", pady=(0, 10))
            if label_text == "Codigo":
                self.codigo_entry = entry
            elif label_text == "Nombre":
                self.nombre_entry = entry
            elif label_text == "Categoria":
                self.categoria_entry = entry
            elif label_text == "Precio":
                self.precio_entry = entry
            elif label_text == "Stock":
                self.stock_entry = entry

        button_frame = tk.Frame(self.form_container, bg="white")
        button_frame.pack(fill="x", pady=(6, 0))
        ttk.Button(button_frame, text="Registrar", command=self.registrar_producto).pack(fill="x", pady=(0, 6))
        ttk.Button(button_frame, text="Cargar", command=self.consultar_producto).pack(fill="x", pady=(0, 6))
        ttk.Button(button_frame, text="Actualizar", command=self.actualizar_producto).pack(fill="x", pady=(0, 6))
        ttk.Button(button_frame, text="Eliminar", command=self.eliminar_producto).pack(fill="x")

    def _configurar_formulario_usuario(self) -> None:
        campos = [
            ("Usuario", self.usuario_var),
            ("Contrase?a", self.password_var),
            ("Nombre", self.user_nombre_var),
            ("Correo", self.user_correo_var),
        ]

        for label_text, variable in campos:
            label = tk.Label(self.user_form_container, text=f"{label_text}:", bg="white", anchor="w")
            label.pack(fill="x", pady=(0, 4))
            if label_text == "Contrase?a":
                entry = ttk.Entry(self.user_form_container, textvariable=variable, show="*", width=30)
            else:
                entry = ttk.Entry(self.user_form_container, textvariable=variable, width=30)
            entry.pack(fill="x", pady=(0, 8))
            if label_text == "Usuario":
                self.user_usuario_entry = entry
            elif label_text == "Contrase?a":
                self.user_password_entry = entry
            elif label_text == "Nombre":
                self.user_nombre_entry = entry
            elif label_text == "Correo":
                self.user_correo_entry = entry

        button_frame = tk.Frame(self.user_form_container, bg="white")
        button_frame.pack(fill="x", pady=(6, 0))
        ttk.Button(button_frame, text="Registrar", command=self.registrar_usuario).pack(fill="x", pady=(0, 6))
        ttk.Button(button_frame, text="Cargar", command=self.consultar_usuario).pack(fill="x", pady=(0, 6))
        ttk.Button(button_frame, text="Actualizar", command=self.actualizar_usuario).pack(fill="x", pady=(0, 6))
        ttk.Button(button_frame, text="Eliminar", command=self.eliminar_usuario).pack(fill="x")

    def _configurar_tabla(self) -> None:
        columns = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tree = ttk.Treeview(self.tabla_container, columns=columns, show="headings", height=18)
        self.tree.heading("codigo", text="Codigo")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("stock", text="Stock")

        self.tree.column("codigo", width=90, anchor="center")
        self.tree.column("nombre", width=180, anchor="w")
        self.tree.column("categoria", width=150, anchor="w")
        self.tree.column("precio", width=100, anchor="center")
        self.tree.column("stock", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(self.tabla_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._actualizar_tabla()

    def _mostrar_estado(self, mensaje: str, error: bool = False) -> None:
        self.status_var.set(mensaje)
        self.status_label.config(fg="#7f1d1d" if error else "#1f2937")

    def _mostrar_seccion(self, seccion: tk.Frame) -> None:
        # hide all main sections then show the requested one
        for widget in (self.dashboard, self.product_section, self.user_section):
            try:
                if widget is not None:
                    widget.pack_forget()
            except Exception:
                pass
        seccion.pack(fill="both", expand=True)

    def _limpiar_formulario(self) -> None:
        self.codigo_var.set("")
        self.nombre_var.set("")
        self.categoria_var.set("")
        self.precio_var.set("")
        self.stock_var.set("")
        if hasattr(self, "codigo_entry"):
            self.codigo_entry.focus_set()

    def _limpiar_formulario_usuario(self) -> None:
        self.usuario_var.set("")
        self.password_var.set("")
        self.user_nombre_var.set("")
        self.user_correo_var.set("")
        if hasattr(self, "user_usuario_entry"):
            self.user_usuario_entry.focus_set()

    def _actualizar_tabla(self) -> None:
        if not hasattr(self, "tree"):
            return
        for item in self.tree.get_children():
            self.tree.delete(item)

        productos = self.restaurante_servicio.listar_productos()
        for producto in productos:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    producto.codigo,
                    producto.nombre,
                    producto.categoria,
                    f"S/. {producto.precio:.2f}",
                    producto.stock,
                ),
            )

        if not productos:
            self.tree.insert("", tk.END, values=("-", "-", "-", "-", "-"))

    def _actualizar_dashboard(self) -> None:
        if not hasattr(self, "total_productos_label"):
            return
        self.total_productos_label.config(text=f"Productos: {len(self.restaurante_servicio.listar_productos())}")
        self.total_usuarios_label.config(text=f"Usuarios: {len(self.restaurante_servicio.listar_usuarios())}")

    def mostrar_inicio(self) -> None:
        # remove existing dashboard if present, hide other sections and show a fresh dashboard
        if hasattr(self, "dashboard") and self.dashboard is not None:
            try:
                self.dashboard.destroy()
            except Exception:
                pass
        self.dashboard = tk.Frame(self.workspace, bg="#edf2ff")
        # hide other sections and show dashboard
        self._mostrar_seccion(self.dashboard)

        title = tk.Label(self.dashboard, text="Panel principal del restaurante", font=("Arial", 18, "bold"), bg="#edf2ff", fg="#1f2937")
        title.pack(anchor="w", pady=(0, 16))

        subtitle = tk.Label(
            self.dashboard,
            text="Administraci?n r?pida de productos y usuarios del sistema.",
            bg="#edf2ff",
            fg="#4b5563",
            justify="left",
        )
        subtitle.pack(anchor="w", pady=(0, 20))

        cards = tk.Frame(self.dashboard, bg="#edf2ff")
        cards.pack(fill="x")

        self.total_productos_label = tk.Label(cards, text="Productos: 0", bg="#dbeafe", fg="#1d4ed8", font=("Arial", 11, "bold"), padx=18, pady=14, relief="solid", borderwidth=1)
        self.total_productos_label.pack(side="left", padx=(0, 16), fill="y")

        self.total_usuarios_label = tk.Label(cards, text="Usuarios: 0", bg="#dcfce7", fg="#15803d", font=("Arial", 11, "bold"), padx=18, pady=14, relief="solid", borderwidth=1)
        self.total_usuarios_label.pack(side="left", fill="y")

        info = tk.Label(
            self.dashboard,
            text="Usa los botones de navegaci?n para ir a Productos o Usuarios y gestionar la informaci?n del restaurante.",
            bg="#fff7ed",
            fg="#9a5b00",
            justify="left",
            wraplength=650,
            padx=16,
            pady=14,
            relief="solid",
            borderwidth=1,
        )
        info.pack(fill="x", pady=(24, 0))

        self._actualizar_dashboard()
        self._mostrar_estado("Bienvenido al sistema de restaurante.")

    def mostrar_productos(self) -> None:
        self._actualizar_tabla()
        self._mostrar_seccion(self.product_section)
        self._mostrar_estado("Secci?n de productos activa.")

    def mostrar_usuarios(self) -> None:
        self._mostrar_usuarios_lista()
        self._mostrar_seccion(self.user_section)
        self._mostrar_estado("Secci?n de usuarios activa.")

    def _mostrar_usuarios_lista(self) -> None:
        # llenar el Treeview de usuarios con columnas: usuario, nombre, correo
        if not hasattr(self, "user_tree"):
            return
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)

        usuarios = self.restaurante_servicio.listar_usuarios()
        for usuario in usuarios:
            try:
                self.user_tree.insert("", tk.END, values=(usuario.usuario, usuario.nombre, usuario.correo))
            except Exception:
                # compatibilidad si listar_usuarios devuelve strings
                self.user_tree.insert("", tk.END, values=(str(usuario), "", ""))

        if not usuarios:
            self.user_tree.insert("", tk.END, values=("-", "-", "-"))

    def refrescar_todo(self) -> None:
        self._actualizar_tabla()
        self._mostrar_usuarios_lista()
        self._actualizar_dashboard()
        self._limpiar_formulario()
        self._limpiar_formulario_usuario()
        self.mostrar_inicio()

    def consultar_producto(self) -> None:
        codigo = self.codigo_var.get().strip()
        if not codigo:
            self._mostrar_estado("Debe ingresar el c?digo para consultar.", error=True)
            return

        producto = self.restaurante_servicio.buscar_producto(codigo)
        if producto is None:
            self._mostrar_estado(f"No existe un producto con c?digo {codigo}.", error=True)
            return

        self.codigo_var.set(producto.codigo)
        self.nombre_var.set(producto.nombre)
        self.categoria_var.set(producto.categoria)
        self.precio_var.set(str(producto.precio))
        self.stock_var.set(str(producto.stock))
        self._mostrar_estado(f"Producto {producto.codigo} cargado correctamente.")

    def registrar_producto(self) -> None:
        try:
            codigo = self.codigo_var.get().strip()
            nombre = self.nombre_var.get().strip()
            categoria = self.categoria_var.get().strip()
            precio = float(self.precio_var.get().strip())
            stock = int(self.stock_var.get().strip())
        except ValueError:
            self._mostrar_estado("Complete todos los campos con valores v?lidos.", error=True)
            return

        if not codigo or not nombre or not categoria:
            self._mostrar_estado("C?digo, nombre y categor?a son obligatorios.", error=True)
            return

        try:
            producto = Producto(codigo=codigo, nombre=nombre, categoria=categoria, precio=precio, stock=stock)
            if not self.restaurante_servicio.registrar_producto(producto):
                self._mostrar_estado(f"El producto {codigo} ya existe.", error=True)
                return
        except ValueError as exc:
            self._mostrar_estado(str(exc), error=True)
            return

        self._actualizar_tabla()
        self._actualizar_dashboard()
        self._limpiar_formulario()
        self._mostrar_estado(f"Producto {codigo} registrado correctamente.")

    def actualizar_producto(self) -> None:
        codigo = self.codigo_var.get().strip()
        if not codigo:
            self._mostrar_estado("Ingrese el c?digo del producto a actualizar.", error=True)
            return

        try:
            nombre = self.nombre_var.get().strip() or None
            categoria = self.categoria_var.get().strip() or None
            precio = float(self.precio_var.get().strip()) if self.precio_var.get().strip() else None
            stock = int(self.stock_var.get().strip()) if self.stock_var.get().strip() else None
        except ValueError:
            self._mostrar_estado("Verifique el formato de precio y stock.", error=True)
            return

        if self.restaurante_servicio.actualizar_producto(codigo, nombre=nombre, categoria=categoria, precio=precio, stock=stock):
            self._actualizar_tabla()
            self._actualizar_dashboard()
            self._mostrar_estado(f"Producto {codigo} actualizado correctamente.")
        else:
            self._mostrar_estado(f"No se encontr? el producto {codigo}.", error=True)

    def eliminar_producto(self) -> None:
        codigo = self.codigo_var.get().strip()
        if not codigo:
            self._mostrar_estado("Ingrese el c?digo del producto a eliminar.", error=True)
            return

        if self.restaurante_servicio.eliminar_producto(codigo):
            self._actualizar_tabla()
            self._actualizar_dashboard()
            self._limpiar_formulario()
            self._mostrar_estado(f"Producto {codigo} eliminado correctamente.")
        else:
            self._mostrar_estado(f"No se encontr? el producto {codigo}.", error=True)

    def consultar_usuario(self) -> None:
        usuario = self.usuario_var.get().strip()
        if not usuario:
            self._mostrar_estado("Debe ingresar el usuario para consultar.", error=True)
            return

        usuario_obj = self.restaurante_servicio.buscar_usuario(usuario)
        if usuario_obj is None:
            self._mostrar_estado(f"No existe el usuario {usuario}.", error=True)
            return

        self.usuario_var.set(usuario_obj.usuario)
        self.password_var.set(usuario_obj.password)
        self.user_nombre_var.set(usuario_obj.nombre)
        self.user_correo_var.set(usuario_obj.correo)
        self._mostrar_estado(f"Usuario {usuario_obj.usuario} cargado correctamente.")

    def registrar_usuario(self) -> None:
        usuario = self.usuario_var.get().strip()
        password = self.password_var.get().strip()
        nombre = self.user_nombre_var.get().strip()
        correo = self.user_correo_var.get().strip()

        if not usuario or not password or not nombre:
            self._mostrar_estado("Usuario, contrase?a y nombre son obligatorios.", error=True)
            return

        try:
            usuario_obj = Usuario(usuario=usuario, password=password, nombre=nombre, correo=correo)
            if not self.restaurante_servicio.registrar_usuario(usuario_obj):
                self._mostrar_estado(f"El usuario {usuario} ya existe.", error=True)
                return
        except ValueError as exc:
            self._mostrar_estado(str(exc), error=True)
            return

        self._mostrar_usuarios_lista()
        self._actualizar_dashboard()
        self._limpiar_formulario_usuario()
        self._mostrar_estado(f"Usuario {usuario} registrado correctamente.")

    def actualizar_usuario(self) -> None:
        usuario = self.usuario_var.get().strip()
        if not usuario:
            self._mostrar_estado("Ingrese el usuario a actualizar.", error=True)
            return

        if self.restaurante_servicio.buscar_usuario(usuario) is None:
            self._mostrar_estado(f"No existe el usuario {usuario}.", error=True)
            return

        password = self.password_var.get().strip() or None
        nombre = self.user_nombre_var.get().strip() or None
        correo = self.user_correo_var.get().strip() or None

        if self.restaurante_servicio.actualizar_usuario(usuario, password=password, nombre=nombre, correo=correo):
            self._mostrar_usuarios_lista()
            self._actualizar_dashboard()
            self._mostrar_estado(f"Usuario {usuario} actualizado correctamente.")
        else:
            self._mostrar_estado(f"No se pudo actualizar el usuario {usuario}.", error=True)

    def eliminar_usuario(self) -> None:
        usuario = self.usuario_var.get().strip()
        if not usuario:
            self._mostrar_estado("Ingrese el usuario a eliminar.", error=True)
            return

        if self.restaurante_servicio.eliminar_usuario(usuario):
            self._mostrar_usuarios_lista()
            self._actualizar_dashboard()
            self._limpiar_formulario_usuario()
            self._mostrar_estado(f"Usuario {usuario} eliminado correctamente.")
        else:
            self._mostrar_estado(f"No existe el usuario {usuario}.", error=True)
