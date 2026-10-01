import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from typing import Optional

try:
    from restaurante_app.modelos.producto import Producto
    from restaurante_app.modelos.usuario import Usuario
    from restaurante_app.modelos.venta import Venta
except ModuleNotFoundError:
    from modelos.producto import Producto
    from modelos.usuario import Usuario
    from modelos.venta import Venta


class MainView(tk.Frame):
    """
    Vista principal de la aplicación Restaurante App.
    Semana 16: Evoluciona la sección de Usuarios aplicando el ciclo completo de eventos:
    Interacción -> Evento -> bind() -> Callback -> Servicio -> Persistencia -> Respuesta Visual.
    Incorpora soporte de roles (Administrador, Empleado, Cliente) y control de acceso.
    """

    def __init__(self, parent, restaurante_servicio, on_logout):
        super().__init__(parent, bg="#edf2ff")
        self.restaurante_servicio = restaurante_servicio
        self.on_logout = on_logout

        self.assets_dir = Path(__file__).resolve().parent.parent / "assets"
        self._icons = {}
        self._cargar_iconos()

        # ------------------------------------------------------------------
        # Barra superior / Toolbar
        # ------------------------------------------------------------------
        self.toolbar = tk.Frame(self, bg="#111827", padx=16, pady=10)
        self.toolbar.pack(fill="x")

        title_frame = tk.Frame(self.toolbar, bg="#111827")
        title_frame.pack(side="left")

        if "app" in self._icons:
            tk.Label(title_frame, image=self._icons["app"], bg="#111827").pack(side="left", padx=(0, 10))

        title = tk.Label(
            title_frame,
            text="Restaurante App - Semana 16",
            fg="white",
            bg="#111827",
            font=("Segoe UI", 13, "bold"),
        )
        title.pack(side="left")

        # Botones de navegación (Inicio, Ventas, Productos, Usuarios, Salir)
        self.nav_buttons = {}
        nav_buttons_config = [
            ("Cerrar sesión", self.on_logout, "logout", "logout"),
            ("Usuarios", self.mostrar_usuarios, "usuarios", "usuarios"),
            ("Productos", self.mostrar_productos, "productos", "productos"),
            ("Ventas", self.mostrar_ventas, "ventas", "ventas"),
            ("Inicio", self.mostrar_inicio, "inicio", "inicio"),
        ]

        for text, cmd, icon_key, ref_key in nav_buttons_config:
            btn_kwargs = {"text": f" {text} ", "command": cmd}
            if icon_key in self._icons:
                btn_kwargs["image"] = self._icons[icon_key]
                btn_kwargs["compound"] = "left"
            btn = ttk.Button(self.toolbar, **btn_kwargs)
            btn.pack(side="right", padx=(0, 6))
            self.nav_buttons[ref_key] = btn

        # Indicador visual de la sesión activa y rol
        self.user_session_label = tk.Label(
            self.toolbar,
            text="👤 Sin sesión activa",
            fg="#93c5fd",
            bg="#111827",
            font=("Segoe UI", 9, "bold"),
            padx=10,
        )
        self.user_session_label.pack(side="right", padx=(0, 12))

        # ------------------------------------------------------------------
        # Espacio de trabajo principal
        # ------------------------------------------------------------------
        self.workspace = tk.Frame(self, bg="#edf2ff", padx=16, pady=14)
        self.workspace.pack(fill="both", expand=True)

        # Variables de formulario de Productos
        self.codigo_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.stock_var = tk.StringVar()

        # Variables de formulario de Usuarios (Semana 16)
        self.user_id_var = tk.StringVar()
        self.usuario_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.user_nombre_var = tk.StringVar()
        self.user_correo_var = tk.StringVar()
        self.user_rol_var = tk.StringVar(value="Cliente")
        self.user_rol_info_var = tk.StringVar(value="Rol Cliente: Registro de comensales para historial y ventas.")

        # Variables de formulario de Ventas
        self.venta_usuario_sel = tk.StringVar()
        self.venta_producto_sel = tk.StringVar()
        self.venta_cantidad_var = tk.StringVar(value="1")
        self.venta_cantidad_var.trace_add("write", lambda *args: self._recalcular_total_venta())

        # Contenedores de secciones
        self.dashboard = None
        self._construir_seccion_ventas()
        self._construir_seccion_productos()
        self._construir_seccion_usuarios()

        # Barra de estado inferior (Retroalimentación visual del sistema)
        self.status_var = tk.StringVar(value="Sistema iniciado correctamente.")
        self.status_bar = tk.Frame(self, bg="#e2e8f0", padx=16, pady=6)
        self.status_bar.pack(fill="x", side="bottom")

        self.status_label = tk.Label(
            self.status_bar,
            textvariable=self.status_var,
            bg="#e2e8f0",
            fg="#1f2937",
            font=("Segoe UI", 9),
            anchor="w",
        )
        self.status_label.pack(fill="x")

        # Cargar pantalla inicial
        self.mostrar_inicio()

    def _cargar_iconos(self) -> None:
        """Carga de manera segura los íconos de la carpeta assets."""
        nombres = {
            "app": "icon_app.png",
            "inicio": "icon_inicio.png",
            "ventas": "icon_ventas.png",
            "productos": "icon_productos.png",
            "usuarios": "icon_usuarios.png",
            "logout": "icon_logout.png",
            "check": "icon_check.png",
        }
        for key, fname in nombres.items():
            path = self.assets_dir / fname
            if path.exists():
                try:
                    self._icons[key] = tk.PhotoImage(file=str(path))
                except Exception as exc:
                    print(f"No se pudo cargar el ícono {fname}: {exc}")

    def _mostrar_estado(self, mensaje: str, error: bool = False) -> None:
        """Actualiza la barra de estado inferior con respuesta visual inmediata."""
        self.status_var.set(mensaje)
        self.status_label.config(
            fg="#b91c1c" if error else "#047857",
            font=("Segoe UI", 9, "bold" if error else "normal"),
        )

    def _mostrar_seccion(self, seccion: tk.Frame) -> None:
        for widget in (self.dashboard, self.sales_section, self.product_section, self.user_section):
            try:
                if widget is not None:
                    widget.pack_forget()
            except Exception:
                pass
        seccion.pack(fill="both", expand=True)

    def actualizar_sesion_activa(self) -> None:
        """
        Sincroniza el indicador de sesión activa y aplica el control de acceso
        según el rol del usuario autenticado (Administrador vs Empleado/Cliente).
        """
        usuario = self.restaurante_servicio.obtener_usuario_actual()
        if usuario:
            es_admin = self.restaurante_servicio.es_administrador()
            color = "#86efac" if es_admin else "#fde047"
            self.user_session_label.config(
                text=f"👤 {usuario.usuario} ({usuario.nombre}) | Rol: {usuario.rol}",
                fg=color,
            )
            if "usuarios" in self.nav_buttons:
                if es_admin:
                    self.nav_buttons["usuarios"].state(["!disabled"])
                else:
                    self.nav_buttons["usuarios"].state(["disabled"])
        else:
            self.user_session_label.config(text="👤 Sin sesión activa", fg="#9ca3af")
            if "usuarios" in self.nav_buttons:
                self.nav_buttons["usuarios"].state(["disabled"])

    # ==================================================================
    # 1. SECCIÓN INICIO / DASHBOARD
    # ==================================================================
    def mostrar_inicio(self) -> None:
        if hasattr(self, "dashboard") and self.dashboard is not None:
            try:
                self.dashboard.destroy()
            except Exception:
                pass

        self.dashboard = tk.Frame(self.workspace, bg="#edf2ff")
        self._mostrar_seccion(self.dashboard)

        header_frame = tk.Frame(self.dashboard, bg="#edf2ff")
        header_frame.pack(fill="x", pady=(0, 16))

        title = tk.Label(
            header_frame,
            text="Bienvenido al Sistema Restaurante App",
            font=("Segoe UI", 18, "bold"),
            bg="#edf2ff",
            fg="#0f172a",
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            header_frame,
            text="Semana 16: Manejo integral de eventos en formularios y tablas con control de roles.",
            font=("Segoe UI", 10),
            bg="#edf2ff",
            fg="#475569",
        )
        subtitle.pack(anchor="w", pady=(4, 0))

        # Tarjetas de resumen estadístico
        cards = tk.Frame(self.dashboard, bg="#edf2ff")
        cards.pack(fill="x", pady=(8, 14))

        tot_prod = len(self.restaurante_servicio.listar_productos())
        tot_user = len(self.restaurante_servicio.listar_usuarios())
        tot_ventas = len(self.restaurante_servicio.listar_ventas())
        recaudado = self.restaurante_servicio.obtener_total_recaudado()

        card_data = [
            ("Productos en Carta", f"{tot_prod} disponibles", "#dbeafe", "#1e40af"),
            ("Usuarios / Clientes", f"{tot_user} registrados", "#dcfce7", "#166534"),
            ("Ventas Realizadas", f"{tot_ventas} órdenes", "#fef3c7", "#92400e"),
            ("Total Recaudado", f"$ {recaudado:.2f}", "#f3e8ff", "#6b21a8"),
        ]

        for titulo, valor, bg_col, fg_col in card_data:
            c = tk.Frame(cards, bg=bg_col, padx=18, pady=12, relief="solid", borderwidth=1)
            c.pack(side="left", padx=(0, 14), fill="y")
            tk.Label(c, text=titulo, font=("Segoe UI", 10, "bold"), bg=bg_col, fg=fg_col).pack(anchor="w")
            tk.Label(c, text=valor, font=("Segoe UI", 13, "bold"), bg=bg_col, fg="#0f172a").pack(anchor="w", pady=(2, 0))

        # Panel explicativo breve y amigable para el usuario
        events_panel = tk.LabelFrame(
            self.dashboard,
            text=" 🧾 Guía rápida de uso ",
            bg="white",
            fg="#0f172a",
            font=("Segoe UI", 11, "bold"),
            padx=16,
            pady=14,
            relief="solid",
            borderwidth=1,
        )
        events_panel.pack(fill="both", expand=True, pady=(8, 0))

        guia_texto = (
            "Bienvenido/a al Restaurante App. Aquí una guía rápida para comenzar:\n\n"
            "1. Ventas: Registrar pedidos y generar recibos rápidamente.\n"
            "2. Productos: Agregar, editar o eliminar ítems del menú.\n"
            "3. Usuarios: Gestionar cuentas (solo Administrador puede acceder).\n"
            "4. Barra de estado: Verás mensajes de confirmación y errores en la parte inferior.\n"
            "5. Cerrar sesión: Usa 'Cerrar sesión' cuando termines para proteger la cuenta.\n\n"
            "Si tienes dudas, consulta al administrador o revisa la documentación del proyecto. ¡Buen trabajo!"
        )
        tk.Label(
            events_panel,
            text=guia_texto,
            font=("Segoe UI", 10),
            bg="white",
            fg="#334155",
            justify="left",
            anchor="nw",
        ).pack(fill="both", expand=True)

    # ==================================================================
    # 2. SECCIÓN VENTAS (Semana 15 - Conservada)
    # ==================================================================
    def _construir_seccion_ventas(self) -> None:
        self.sales_section = tk.Frame(self.workspace, bg="#edf2ff")

        # Contenedor izquierdo: Formulario de Registro de Venta
        self.ventas_form_container = tk.LabelFrame(
            self.sales_section,
            text=" Registrar Nueva Venta ",
            bg="white",
            fg="#0f172a",
            font=("Segoe UI", 10, "bold"),
            padx=16,
            pady=14,
            relief="solid",
            borderwidth=1,
        )
        self.ventas_form_container.pack(side="left", fill="y", padx=(0, 14))

        # 1. Selector de Cliente/Usuario
        tk.Label(self.ventas_form_container, text="Seleccione Cliente / Usuario:", font=("Segoe UI", 9, "bold"), bg="white", fg="#374151", anchor="w").pack(fill="x", pady=(2, 2))
        self.combo_usuario = ttk.Combobox(self.ventas_form_container, textvariable=self.venta_usuario_sel, state="readonly", width=36, font=("Segoe UI", 9))
        self.combo_usuario.pack(fill="x", pady=(0, 6))
        self.combo_usuario.bind("<<ComboboxSelected>>", self._on_usuario_cambiado)

        # Ficha del Cliente
        self.card_cliente = tk.Frame(self.ventas_form_container, bg="#f8fafc", padx=10, pady=6, relief="groove", borderwidth=1)
        self.card_cliente.pack(fill="x", pady=(0, 10))
        self.lbl_cli_usuario = tk.Label(self.card_cliente, text="Usuario: -", font=("Segoe UI", 8), bg="#f8fafc", fg="#475569", anchor="w")
        self.lbl_cli_usuario.pack(fill="x")
        self.lbl_cli_nombre = tk.Label(self.card_cliente, text="Nombre: -", font=("Segoe UI", 8, "bold"), bg="#f8fafc", fg="#1e293b", anchor="w")
        self.lbl_cli_nombre.pack(fill="x")
        self.lbl_cli_correo = tk.Label(self.card_cliente, text="Correo: -", font=("Segoe UI", 8), bg="#f8fafc", fg="#64748b", anchor="w")
        self.lbl_cli_correo.pack(fill="x")

        # 2. Selector de Producto
        tk.Label(self.ventas_form_container, text="Seleccione Producto:", font=("Segoe UI", 9, "bold"), bg="white", fg="#374151", anchor="w").pack(fill="x", pady=(4, 2))
        self.combo_producto = ttk.Combobox(self.ventas_form_container, textvariable=self.venta_producto_sel, state="readonly", width=36, font=("Segoe UI", 9))
        self.combo_producto.pack(fill="x", pady=(0, 6))
        self.combo_producto.bind("<<ComboboxSelected>>", self._on_producto_cambiado)

        # Ficha del Producto
        self.card_producto = tk.Frame(self.ventas_form_container, bg="#f8fafc", padx=10, pady=6, relief="groove", borderwidth=1)
        self.card_producto.pack(fill="x", pady=(0, 10))
        self.lbl_prod_codigo = tk.Label(self.card_producto, text="Código: -", font=("Segoe UI", 8), bg="#f8fafc", fg="#475569", anchor="w")
        self.lbl_prod_codigo.pack(fill="x")
        self.lbl_prod_nombre = tk.Label(self.card_producto, text="Nombre: -", font=("Segoe UI", 8, "bold"), bg="#f8fafc", fg="#1e293b", anchor="w")
        self.lbl_prod_nombre.pack(fill="x")
        self.lbl_prod_cat = tk.Label(self.card_producto, text="Categoría: -", font=("Segoe UI", 8), bg="#f8fafc", fg="#64748b", anchor="w")
        self.lbl_prod_cat.pack(fill="x")
        self.lbl_prod_precio = tk.Label(self.card_producto, text="Precio: $ 0.00", font=("Segoe UI", 8, "bold"), bg="#f8fafc", fg="#059669", anchor="w")
        self.lbl_prod_precio.pack(fill="x")
        self.lbl_prod_stock = tk.Label(self.card_producto, text="Stock Disponible: 0", font=("Segoe UI", 8), bg="#f8fafc", fg="#d97706", anchor="w")
        self.lbl_prod_stock.pack(fill="x")

        # 3. Cantidad a vender
        tk.Label(self.ventas_form_container, text="Cantidad a Vender:", font=("Segoe UI", 9, "bold"), bg="white", fg="#374151", anchor="w").pack(fill="x", pady=(4, 2))
        self.spin_cantidad = ttk.Spinbox(self.ventas_form_container, from_=1, to=999, textvariable=self.venta_cantidad_var, width=12, font=("Segoe UI", 10))
        self.spin_cantidad.pack(anchor="w", pady=(0, 10))

        # Total estimado
        total_frame = tk.Frame(self.ventas_form_container, bg="#eff6ff", padx=10, pady=8, relief="solid", borderwidth=1)
        total_frame.pack(fill="x", pady=(6, 12))
        tk.Label(total_frame, text="TOTAL A PAGAR:", font=("Segoe UI", 9, "bold"), bg="#eff6ff", fg="#1e40af").pack(side="left")
        self.lbl_total_estimado = tk.Label(total_frame, text="$ 0.00", font=("Segoe UI", 12, "bold"), bg="#eff6ff", fg="#1d4ed8")
        self.lbl_total_estimado.pack(side="right")

        # Botón Registrar Venta (command=)
        btn_kwargs = {"text": " Registrar Venta ", "command": self.registrar_venta}
        if "check" in self._icons:
            btn_kwargs["image"] = self._icons["check"]
            btn_kwargs["compound"] = "left"
        self.btn_registrar_venta = ttk.Button(self.ventas_form_container, **btn_kwargs)
        self.btn_registrar_venta.pack(fill="x", pady=(0, 6), ipady=3)

        ttk.Button(self.ventas_form_container, text="Limpiar Formulario de Venta", command=self._limpiar_formulario_venta).pack(fill="x")

        # Contenedor derecho: Historial de Ventas (Treeview)
        self.ventas_tabla_container = tk.LabelFrame(
            self.sales_section,
            text=" Historial de Ventas Registradas ",
            bg="white",
            fg="#0f172a",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=10,
            relief="solid",
            borderwidth=1,
        )
        self.ventas_tabla_container.pack(side="left", fill="both", expand=True)

        columns_ventas = ("codigo", "fecha", "usuario", "cliente_nombre", "producto", "cantidad", "precio_u", "total")
        self.tree_ventas = ttk.Treeview(self.ventas_tabla_container, columns=columns_ventas, show="headings", height=18)
        self.tree_ventas.heading("codigo", text="Código")
        self.tree_ventas.heading("fecha", text="Fecha y Hora")
        self.tree_ventas.heading("usuario", text="Cliente / Usuario")
        self.tree_ventas.heading("cliente_nombre", text="Nombre Cliente")
        self.tree_ventas.heading("producto", text="Producto Vendido")
        self.tree_ventas.heading("cantidad", text="Cant.")
        self.tree_ventas.heading("precio_u", text="P. Unitario")
        self.tree_ventas.heading("total", text="Total")

        self.tree_ventas.column("codigo", width=80, anchor="center")
        self.tree_ventas.column("fecha", width=140, anchor="center")
        self.tree_ventas.column("usuario", width=110, anchor="w")
        self.tree_ventas.column("cliente_nombre", width=140, anchor="w")
        self.tree_ventas.column("producto", width=140, anchor="w")
        self.tree_ventas.column("cantidad", width=60, anchor="center")
        self.tree_ventas.column("precio_u", width=90, anchor="center")
        self.tree_ventas.column("total", width=90, anchor="center")

        scroll_ventas = ttk.Scrollbar(self.ventas_tabla_container, orient="vertical", command=self.tree_ventas.yview)
        self.tree_ventas.configure(yscrollcommand=scroll_ventas.set)
        self.tree_ventas.pack(side="left", fill="both", expand=True)
        scroll_ventas.pack(side="right", fill="y")

        self.ventas_summary_bar = tk.Frame(self.ventas_tabla_container, bg="white", pady=6)
        self.ventas_summary_bar.pack(fill="x", side="bottom")
        self.lbl_ventas_resumen = tk.Label(
            self.ventas_summary_bar,
            text="Total Ventas: 0 | Recaudación Acumulada: $ 0.00",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#1e40af",
            anchor="e",
        )
        self.lbl_ventas_resumen.pack(fill="x")

    def mostrar_ventas(self) -> None:
        self._recargar_comboboxes_venta()
        self._actualizar_tabla_ventas()
        self._mostrar_seccion(self.sales_section)
        self._mostrar_estado("Sección de Ventas activa. Seleccione usuario, producto y registre la venta.")

    def _recargar_comboboxes_venta(self) -> None:
        """Carga en los select box los usuarios y productos con detalles actualizados."""
        usuarios = self.restaurante_servicio.listar_usuarios()
        user_values = [
            f"{u.usuario} - {u.nombre} [{u.rol}]"
            for u in usuarios
        ]
        self.combo_usuario["values"] = user_values

        productos = self.restaurante_servicio.listar_productos()
        prod_values = [
            f"{p.codigo} - {p.nombre} | $ {p.precio:.2f} | Stock: {p.stock}"
            for p in productos
        ]
        self.combo_producto["values"] = prod_values

    def _extraer_clave_usuario_combo(self) -> str:
        seleccion = self.venta_usuario_sel.get().strip()
        if " - " in seleccion:
            return seleccion.split(" - ")[0].strip()
        return seleccion

    def _extraer_codigo_producto_combo(self) -> str:
        seleccion = self.venta_producto_sel.get().strip()
        if " - " in seleccion:
            return seleccion.split(" - ")[0].strip()
        return seleccion

    def _on_usuario_cambiado(self, event=None) -> None:
        user_key = self._extraer_clave_usuario_combo()
        usuario = self.restaurante_servicio.buscar_usuario(user_key)
        if usuario:
            self.lbl_cli_usuario.config(text=f"Usuario: {usuario.usuario}")
            self.lbl_cli_nombre.config(text=f"Nombre: {usuario.nombre} ({usuario.rol})")
            self.lbl_cli_correo.config(text=f"Correo: {usuario.correo or 'N/A'}")
        else:
            self.lbl_cli_usuario.config(text="Usuario: -")
            self.lbl_cli_nombre.config(text="Nombre: -")
            self.lbl_cli_correo.config(text="Correo: -")

    def _on_producto_cambiado(self, event=None) -> None:
        prod_code = self._extraer_codigo_producto_combo()
        producto = self.restaurante_servicio.buscar_producto(prod_code)
        if producto:
            self.lbl_prod_codigo.config(text=f"Código: {producto.codigo}")
            self.lbl_prod_nombre.config(text=f"Nombre: {producto.nombre}")
            self.lbl_prod_cat.config(text=f"Categoría: {producto.categoria}")
            self.lbl_prod_precio.config(text=f"Precio: $ {producto.precio:.2f}")
            self.lbl_prod_stock.config(text=f"Stock Disponible: {producto.stock} unidades")
        else:
            self.lbl_prod_codigo.config(text="Código: -")
            self.lbl_prod_nombre.config(text="Nombre: -")
            self.lbl_prod_cat.config(text="Categoría: -")
            self.lbl_prod_precio.config(text="Precio: $ 0.00")
            self.lbl_prod_stock.config(text="Stock Disponible: 0")

        self._recalcular_total_venta()

    def _recalcular_total_venta(self) -> None:
        prod_code = self._extraer_codigo_producto_combo()
        producto = self.restaurante_servicio.buscar_producto(prod_code)
        if not producto:
            self.lbl_total_estimado.config(text="$ 0.00")
            return

        try:
            cant = int(self.venta_cantidad_var.get())
            if cant <= 0:
                self.lbl_total_estimado.config(text="$ 0.00")
                return
            tot = cant * producto.precio
            self.lbl_total_estimado.config(text=f"$ {tot:.2f}")
        except ValueError:
            self.lbl_total_estimado.config(text="$ 0.00")

    def registrar_venta(self) -> None:
        """Callback del botón Registrar Venta (command=self.registrar_venta)."""
        user_key = self._extraer_clave_usuario_combo()
        prod_code = self._extraer_codigo_producto_combo()
        cantidad_str = self.venta_cantidad_var.get().strip()

        if not user_key:
            self._mostrar_estado("Error: Debe seleccionar un cliente/usuario.", error=True)
            return

        if not prod_code:
            self._mostrar_estado("Error: Debe seleccionar un producto del menú.", error=True)
            return

        try:
            cantidad = int(cantidad_str)
        except ValueError:
            self._mostrar_estado("Error: La cantidad debe ser un número entero.", error=True)
            return

        exito, mensaje, venta_obj = self.restaurante_servicio.registrar_venta(user_key, prod_code, cantidad)

        if not exito:
            self._mostrar_estado(mensaje, error=True)
            return

        self._actualizar_tabla_ventas()
        self._actualizar_tabla()
        self._recargar_comboboxes_venta()
        self._limpiar_formulario_venta()
        self._mostrar_estado(mensaje)

    def _actualizar_tabla_ventas(self) -> None:
        if not hasattr(self, "tree_ventas"):
            return
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)

        ventas = self.restaurante_servicio.listar_ventas()
        for v in ventas:
            # Intentar resolver el nombre completo del cliente a partir del usuario almacenado en la venta
            usuario_obj = self.restaurante_servicio.buscar_usuario(v.usuario)
            cliente_nombre = usuario_obj.nombre if usuario_obj else "-"
            self.tree_ventas.insert(
                "",
                tk.END,
                values=(
                    v.codigo,
                    v.fecha,
                    v.usuario,
                    cliente_nombre,
                    v.producto_nombre,
                    v.cantidad,
                    f"$ {v.precio_unitario:.2f}",
                    f"$ {v.total:.2f}",
                ),
            )

        total_rec = self.restaurante_servicio.obtener_total_recaudado()
        self.lbl_ventas_resumen.config(
            text=f"Total Ventas: {len(ventas)} órdenes | Recaudación Acumulada: $ {total_rec:.2f}"
        )

    def _limpiar_formulario_venta(self) -> None:
        self.venta_usuario_sel.set("")
        self.venta_producto_sel.set("")
        self.venta_cantidad_var.set("1")
        self._on_usuario_cambiado()
        self._on_producto_cambiado()
        self._mostrar_estado("Formulario de venta restablecido.")

    # ==================================================================
    # 3. SECCIÓN PRODUCTOS (Conservada)
    # ==================================================================
    def _construir_seccion_productos(self) -> None:
        self.product_section = tk.Frame(self.workspace, bg="#edf2ff")

        self.form_container = tk.LabelFrame(
            self.product_section,
            text=" Formulario de Productos ",
            bg="white",
            fg="#0f172a",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=12,
            relief="solid",
            borderwidth=1,
        )
        self.form_container.pack(side="left", fill="y", padx=(0, 14))

        self.tabla_container = tk.LabelFrame(
            self.product_section,
            text=" Listado de Productos en Carta ",
            bg="white",
            fg="#0f172a",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=10,
            relief="solid",
            borderwidth=1,
        )
        self.tabla_container.pack(side="left", fill="both", expand=True)

        campos = [
            ("Código", self.codigo_var),
            ("Nombre", self.nombre_var),
            ("Categoría", self.categoria_var),
            ("Precio ($)", self.precio_var),
            ("Stock", self.stock_var),
        ]

        for label_text, variable in campos:
            label = tk.Label(self.form_container, text=f"{label_text}:", font=("Segoe UI", 9, "bold"), bg="white", fg="#374151", anchor="w")
            label.pack(fill="x", pady=(0, 2))
            entry = ttk.Entry(self.form_container, textvariable=variable, width=28, font=("Segoe UI", 10))
            entry.pack(fill="x", pady=(0, 8))
            if label_text.startswith("Código"):
                self.codigo_entry = entry

        btn_prod_frame = tk.Frame(self.form_container, bg="white")
        btn_prod_frame.pack(fill="x", pady=(6, 0))

        ttk.Button(btn_prod_frame, text="Registrar Producto", command=self.registrar_producto).pack(fill="x", pady=(0, 6))
        ttk.Button(btn_prod_frame, text="Cargar por Código", command=self.consultar_producto).pack(fill="x", pady=(0, 6))
        ttk.Button(btn_prod_frame, text="Actualizar Producto", command=self.actualizar_producto).pack(fill="x", pady=(0, 6))
        ttk.Button(btn_prod_frame, text="Eliminar Producto", command=self.eliminar_producto).pack(fill="x", pady=(0, 6))
        ttk.Button(btn_prod_frame, text="Limpiar Campos", command=self._limpiar_formulario).pack(fill="x")

        columns = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tree = ttk.Treeview(self.tabla_container, columns=columns, show="headings", height=18)
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Nombre del Producto")
        self.tree.heading("categoria", text="Categoría")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("stock", text="Stock")

        self.tree.column("codigo", width=80, anchor="center")
        self.tree.column("nombre", width=190, anchor="w")
        self.tree.column("categoria", width=140, anchor="w")
        self.tree.column("precio", width=100, anchor="center")
        self.tree.column("stock", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(self.tabla_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def mostrar_productos(self) -> None:
        self._actualizar_tabla()
        self._mostrar_seccion(self.product_section)
        self._mostrar_estado("Sección de productos activa.")

    def _actualizar_tabla(self) -> None:
        if not hasattr(self, "tree"):
            return
        for item in self.tree.get_children():
            self.tree.delete(item)

        productos = self.restaurante_servicio.listar_productos()
        for p in productos:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    p.codigo,
                    p.nombre,
                    p.categoria,
                    f"$ {p.precio:.2f}",
                    p.stock,
                ),
            )

        if not productos:
            self.tree.insert("", tk.END, values=("-", "No hay productos registrados", "-", "-", "-"))

    def consultar_producto(self) -> None:
        codigo = self.codigo_var.get().strip()
        if not codigo:
            self._mostrar_estado("Debe ingresar un código para consultar.", error=True)
            return

        producto = self.restaurante_servicio.buscar_producto(codigo)
        if producto is None:
            self._mostrar_estado(f"No existe el producto con código '{codigo}'.", error=True)
            return

        self.nombre_var.set(producto.nombre)
        self.categoria_var.set(producto.categoria)
        self.precio_var.set(str(producto.precio))
        self.stock_var.set(str(producto.stock))
        self._mostrar_estado(f"Producto '{producto.codigo}' ({producto.nombre}) cargado.")

    def registrar_producto(self) -> None:
        codigo = self.codigo_var.get().strip()
        nombre = self.nombre_var.get().strip()
        categoria = self.categoria_var.get().strip()
        precio_str = self.precio_var.get().strip()
        stock_str = self.stock_var.get().strip()

        if not codigo or not nombre or not categoria or not precio_str or not stock_str:
            self._mostrar_estado("Todos los campos de producto son obligatorios.", error=True)
            return

        try:
            precio = float(precio_str)
            stock = int(stock_str)
            producto = Producto(codigo=codigo, nombre=nombre, categoria=categoria, precio=precio, stock=stock)
            if not self.restaurante_servicio.registrar_producto(producto):
                self._mostrar_estado(f"El producto con código '{codigo}' ya existe.", error=True)
                return
        except ValueError as exc:
            self._mostrar_estado(str(exc), error=True)
            return

        self._actualizar_tabla()
        self._recargar_comboboxes_venta()
        self._limpiar_formulario()
        self._mostrar_estado(f"Producto '{codigo}' ({nombre}) registrado exitosamente.")

    def actualizar_producto(self) -> None:
        codigo = self.codigo_var.get().strip()
        if not codigo:
            self._mostrar_estado("Ingrese el código del producto a actualizar.", error=True)
            return

        try:
            nombre = self.nombre_var.get().strip() or None
            categoria = self.categoria_var.get().strip() or None
            precio = float(self.precio_var.get().strip()) if self.precio_var.get().strip() else None
            stock = int(self.stock_var.get().strip()) if self.stock_var.get().strip() else None
        except ValueError:
            self._mostrar_estado("Verifique el formato numérico de precio y stock.", error=True)
            return

        if self.restaurante_servicio.actualizar_producto(codigo, nombre=nombre, categoria=categoria, precio=precio, stock=stock):
            self._actualizar_tabla()
            self._recargar_comboboxes_venta()
            self._mostrar_estado(f"Producto '{codigo}' actualizado correctamente.")
        else:
            self._mostrar_estado(f"No se encontró el producto '{codigo}'.", error=True)

    def eliminar_producto(self) -> None:
        codigo = self.codigo_var.get().strip()
        if not codigo:
            self._mostrar_estado("Ingrese el código del producto a eliminar.", error=True)
            return

        if self.restaurante_servicio.eliminar_producto(codigo):
            self._actualizar_tabla()
            self._recargar_comboboxes_venta()
            self._limpiar_formulario()
            self._mostrar_estado(f"Producto '{codigo}' eliminado satisfactoriamente.")
        else:
            self._mostrar_estado(f"No se encontró el producto '{codigo}'.", error=True)

    def _limpiar_formulario(self) -> None:
        self.codigo_var.set("")
        self.nombre_var.set("")
        self.categoria_var.set("")
        self.precio_var.set("")
        self.stock_var.set("")
        if hasattr(self, "codigo_entry"):
            self.codigo_entry.focus_set()

    # ==================================================================
    # 4. SECCIÓN USUARIOS (Semana 16: Eventos en Tabla y Formulario)
    # ==================================================================
    def _construir_seccion_usuarios(self) -> None:
        self.user_section = tk.Frame(self.workspace, bg="#edf2ff")

        # Contenedor izquierdo: Formulario de Usuario
        self.user_form_container = tk.LabelFrame(
            self.user_section,
            text=" Formulario de Usuarios ",
            bg="white",
            fg="#0f172a",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=12,
            relief="solid",
            borderwidth=1,
        )
        self.user_form_container.pack(side="left", fill="y", padx=(0, 14))

        # Contenedor derecho: Directorio de Usuarios (Treeview)
        self.user_list_container = tk.LabelFrame(
            self.user_section,
            text=" Directorio de Usuarios Registrados (Treeview) ",
            bg="white",
            fg="#0f172a",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=10,
            relief="solid",
            borderwidth=1,
        )
        self.user_list_container.pack(side="left", fill="both", expand=True)

        # 1. Campo Identificador (ID)
        tk.Label(
            self.user_form_container,
            text="Identificador (ID):",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#374151",
            anchor="w",
        ).pack(fill="x", pady=(0, 2))
        self.user_id_entry = ttk.Entry(
            self.user_form_container,
            textvariable=self.user_id_var,
            width=32,
            font=("Segoe UI", 10),
            state="readonly",
        )
        self.user_id_entry.pack(fill="x", pady=(0, 6))

        # 2. Campo Usuario
        tk.Label(
            self.user_form_container,
            text="Nombre de Usuario:",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#374151",
            anchor="w",
        ).pack(fill="x", pady=(0, 2))
        self.user_usuario_entry = ttk.Entry(
            self.user_form_container,
            textvariable=self.usuario_var,
            width=32,
            font=("Segoe UI", 10),
        )
        self.user_usuario_entry.pack(fill="x", pady=(0, 6))

        # 3. Campo Contraseña
        tk.Label(
            self.user_form_container,
            text="Contraseña:",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#374151",
            anchor="w",
        ).pack(fill="x", pady=(0, 2))
        self.user_password_entry = ttk.Entry(
            self.user_form_container,
            textvariable=self.password_var,
            show="*",
            width=32,
            font=("Segoe UI", 10),
        )
        self.user_password_entry.pack(fill="x", pady=(0, 6))

        # 4. Campo Nombre Completo
        tk.Label(
            self.user_form_container,
            text="Nombre Completo:",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#374151",
            anchor="w",
        ).pack(fill="x", pady=(0, 2))
        self.user_nombre_entry = ttk.Entry(
            self.user_form_container,
            textvariable=self.user_nombre_var,
            width=32,
            font=("Segoe UI", 10),
        )
        self.user_nombre_entry.pack(fill="x", pady=(0, 6))

        # 5. Campo Correo Electrónico
        tk.Label(
            self.user_form_container,
            text="Correo Electrónico:",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#374151",
            anchor="w",
        ).pack(fill="x", pady=(0, 2))
        self.user_correo_entry = ttk.Entry(
            self.user_form_container,
            textvariable=self.user_correo_var,
            width=32,
            font=("Segoe UI", 10),
        )
        self.user_correo_entry.pack(fill="x", pady=(0, 6))

        # 6. Campo Rol (ttk.Combobox con evento <<ComboboxSelected>>)
        tk.Label(
            self.user_form_container,
            text="Rol del Usuario:",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#374151",
            anchor="w",
        ).pack(fill="x", pady=(0, 2))
        self.user_rol_combo = ttk.Combobox(
            self.user_form_container,
            textvariable=self.user_rol_var,
            values=("Cliente", "Empleado", "Administrador"),
            state="readonly",
            width=30,
            font=("Segoe UI", 10),
        )
        self.user_rol_combo.pack(fill="x", pady=(0, 4))
        self.user_rol_combo.set("Cliente")
        # Evento virtual <<ComboboxSelected>> asociado mediante bind()
        self.user_rol_combo.bind("<<ComboboxSelected>>", self._on_combobox_rol_selected)

        # Etiqueta informativa que describe las atribuciones del rol seleccionado
        self.lbl_rol_info = tk.Label(
            self.user_form_container,
            textvariable=self.user_rol_info_var,
            font=("Segoe UI", 8, "italic"),
            bg="#f8fafc",
            fg="#475569",
            wraplength=230,
            justify="left",
            relief="groove",
            padx=6,
            pady=4,
        )
        self.lbl_rol_info.pack(fill="x", pady=(0, 8))

        # Panel informativo de eventos y atajos de teclado
        atajos_frame = tk.LabelFrame(
            self.user_form_container,
            text=" ⌨ Atajos de Eventos ",
            bg="#f1f5f9",
            fg="#1e293b",
            font=("Segoe UI", 8, "bold"),
            padx=8,
            pady=4,
            relief="groove",
        )
        atajos_frame.pack(fill="x", pady=(0, 8))
        tk.Label(
            atajos_frame,
            text="• Enter : Registrar usuario\n• Esc   : Limpiar y deseleccionar\n• Clic  : Cargar desde tabla",
            font=("Consolas", 8),
            bg="#f1f5f9",
            fg="#334155",
            justify="left",
            anchor="w",
        ).pack(fill="x")

        # Botones de acción vinculados mediante command=
        btn_usr_frame = tk.Frame(self.user_form_container, bg="white")
        btn_usr_frame.pack(fill="x", pady=(2, 0))

        ttk.Button(btn_usr_frame, text="Registrar Usuario", command=self.registrar_usuario).pack(fill="x", pady=(0, 5))
        ttk.Button(btn_usr_frame, text="Actualizar Usuario", command=self.actualizar_usuario).pack(fill="x", pady=(0, 5))
        ttk.Button(btn_usr_frame, text="Eliminar Usuario", command=self.eliminar_usuario).pack(fill="x", pady=(0, 5))
        ttk.Button(btn_usr_frame, text="Limpiar Formulario (Esc)", command=self._limpiar_formulario_usuario).pack(fill="x")

        # ------------------------------------------------------------------
        # Eventos de teclado asociados a los campos del formulario con bind()
        # ------------------------------------------------------------------
        # <Return>: Confirmar el registro reutilizando el método existente
        # <Escape>: Limpiar formulario y cancelar selección
        for entry_widget in (
            self.user_usuario_entry,
            self.user_password_entry,
            self.user_nombre_entry,
            self.user_correo_entry,
            self.user_rol_combo,
        ):
            entry_widget.bind("<Return>", self._on_return_registrar_usuario)
            entry_widget.bind("<Escape>", self._on_escape_limpiar_usuario)

        # ------------------------------------------------------------------
        # Directorio de Usuarios en Treeview
        # Columnas sin información sensible (se excluye la contraseña)
        # ------------------------------------------------------------------
        columns = ("id", "nombre", "usuario", "rol", "correo")
        self.user_tree = ttk.Treeview(self.user_list_container, columns=columns, show="headings", height=18)
        self.user_tree.heading("id", text="Identificador")
        self.user_tree.heading("nombre", text="Nombre Completo")
        self.user_tree.heading("usuario", text="Usuario")
        self.user_tree.heading("rol", text="Rol Asignado")
        self.user_tree.heading("correo", text="Correo Electrónico")

        self.user_tree.column("id", width=95, anchor="center")
        self.user_tree.column("nombre", width=180, anchor="w")
        self.user_tree.column("usuario", width=110, anchor="center")
        self.user_tree.column("rol", width=110, anchor="center")
        self.user_tree.column("correo", width=190, anchor="w")

        user_scroll = ttk.Scrollbar(self.user_list_container, orient="vertical", command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=user_scroll.set)
        self.user_tree.pack(side="left", fill="both", expand=True)
        user_scroll.pack(side="right", fill="y")

        # Asociar el evento virtual <<TreeviewSelect>> mediante bind()
        self.user_tree.bind("<<TreeviewSelect>>", self._on_treeview_usuario_select)
        self.user_tree.bind("<Escape>", self._on_escape_limpiar_usuario)

    # ------------------------------------------------------------------
    # Callbacks de Eventos (Semana 16)
    # ------------------------------------------------------------------
    def _on_treeview_usuario_select(self, event=None) -> None:
        """
        Callback para el evento virtual <<TreeviewSelect>>.
        Flujo:
        1. Obtiene la fila seleccionada en el Treeview.
        2. Extrae el identificador público del usuario.
        3. Consulta el objeto completo mediante RestauranteServicio (evitando exponer contraseñas en tabla).
        4. Carga todos los datos correspondientes en el formulario.
        5. Emite respuesta visual en la barra de estado.
        """
        seleccion = self.user_tree.selection()
        if not seleccion:
            return
        item_id = seleccion[0]
        valores = self.user_tree.item(item_id, "values")
        if not valores or valores[0] == "-":
            return

        identificador = str(valores[0]).strip()
        usuario_obj = self.restaurante_servicio.buscar_usuario(identificador)
        if usuario_obj is None and len(valores) > 2:
            usuario_obj = self.restaurante_servicio.buscar_usuario(str(valores[2]).strip())

        if usuario_obj:
            self.user_id_var.set(usuario_obj.id)
            self.usuario_var.set(usuario_obj.usuario)
            self.password_var.set(usuario_obj.password)
            self.user_nombre_var.set(usuario_obj.nombre)
            self.user_correo_var.set(usuario_obj.correo)
            self.user_rol_var.set(usuario_obj.rol)
            self._actualizar_info_rol(usuario_obj.rol)
            self._mostrar_estado(
                f"Evento <<TreeviewSelect>>: Usuario '{usuario_obj.usuario}' ({usuario_obj.rol}) "
                f"cargado en el formulario mediante consulta al servicio."
            )

    def _on_combobox_rol_selected(self, event=None) -> None:
        """
        Callback para el evento virtual <<ComboboxSelected>> del combobox de rol.
        Proporciona respuesta visual descriptiva inmediata sobre el rol seleccionado.
        """
        rol = self.user_rol_var.get().strip()
        self._actualizar_info_rol(rol)
        self._mostrar_estado(f"Evento <<ComboboxSelected>>: Rol seleccionado cambiado a '{rol}'.")

    def _actualizar_info_rol(self, rol: str) -> None:
        """Actualiza el texto descriptivo del rol seleccionado."""
        mensajes = {
            "Administrador": "Rol Administrador: Acceso total al sistema y gestión administrativa de usuarios.",
            "Empleado": "Rol Empleado: Acceso operativo a catálogo de productos y registro de ventas.",
            "Cliente": "Rol Cliente: Registro de comensales para fidelización y consultas de compras.",
        }
        info = mensajes.get(rol, f"Rol seleccionado: {rol}")
        self.user_rol_info_var.set(info)

    def _on_return_registrar_usuario(self, event=None) -> None:
        """
        Callback para el evento de teclado <Return>.
        Atajo funcional para registrar un usuario desde el formulario.
        Reutiliza registrar_usuario() para evitar duplicar lógica.
        """
        self._mostrar_estado("Evento <Return>: Atajo de teclado activado para registrar usuario.")
        self.registrar_usuario()

    def _on_escape_limpiar_usuario(self, event=None) -> None:
        """
        Callback para el evento de teclado <Escape>.
        Atajo funcional para limpiar el formulario, cancelar la selección y volver al estado inicial.
        Reutiliza _limpiar_formulario_usuario() para evitar duplicar lógica.
        """
        self._limpiar_formulario_usuario()
        self._mostrar_estado("Evento <Escape>: Formulario y selección de tabla restablecidos al estado inicial.")

    # ------------------------------------------------------------------
    # Métodos de Negocio de Usuarios vinculados a command=
    # ------------------------------------------------------------------
    def mostrar_usuarios(self) -> None:
        """
        Control de acceso: Solo el usuario Administrador puede ingresar a la gestión de usuarios.
        """
        if not self.restaurante_servicio.es_administrador():
            self._mostrar_estado("Acceso denegado: Únicamente el usuario Administrador puede gestionar usuarios.", error=True)
            messagebox.showwarning(
                "Acceso Restringido",
                "Únicamente los usuarios con rol de Administrador pueden acceder a la gestión de usuarios del restaurante."
            )
            return

        self._mostrar_usuarios_lista()
        self._mostrar_seccion(self.user_section)
        self._mostrar_estado("Gestión de Usuarios activa. Eventos disponibles: <<TreeviewSelect>>, <Return>, <Escape>, <<ComboboxSelected>>.")

    def _mostrar_usuarios_lista(self) -> None:
        """Puebla el Treeview de usuarios con datos actualizados desde el servicio."""
        if not hasattr(self, "user_tree"):
            return
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)

        usuarios = self.restaurante_servicio.listar_usuarios()
        for u in usuarios:
            self.user_tree.insert(
                "",
                tk.END,
                values=(u.id, u.nombre, u.usuario, u.rol, u.correo or "N/A"),
            )

        if not usuarios:
            self.user_tree.insert("", tk.END, values=("-", "No hay usuarios registrados", "-", "-", "-"))

    def registrar_usuario(self) -> None:
        """
        Registra un usuario delegando la validación y persistencia a RestauranteServicio.
        Reutilizado tanto por el botón Registrar (command=) como por la tecla <Return> (bind()).
        """
        usuario = self.usuario_var.get().strip()
        password = self.password_var.get().strip()
        nombre = self.user_nombre_var.get().strip()
        correo = self.user_correo_var.get().strip()
        rol = self.user_rol_var.get().strip() or "Cliente"

        if not usuario or not password or not nombre:
            self._mostrar_estado("Error: Usuario, contraseña y nombre son campos obligatorios.", error=True)
            messagebox.showwarning("Campos Requeridos", "Debe completar usuario, contraseña y nombre para registrar.")
            return

        try:
            nuevo_usuario = Usuario(
                usuario=usuario,
                password=password,
                nombre=nombre,
                correo=correo,
                rol=rol,
            )
            exito, mensaje = self.restaurante_servicio.registrar_usuario(nuevo_usuario)
        except ValueError as exc:
            self._mostrar_estado(str(exc), error=True)
            messagebox.showerror("Error de Validación", str(exc))
            return

        if exito:
            self._mostrar_usuarios_lista()
            self._recargar_comboboxes_venta()
            self._limpiar_formulario_usuario()
            self._mostrar_estado(mensaje)
            messagebox.showinfo("Registro Exitoso", mensaje)
        else:
            self._mostrar_estado(mensaje, error=True)
            messagebox.showwarning("Atención", mensaje)

    def actualizar_usuario(self) -> None:
        """
        Actualiza los datos del usuario especificado en el formulario.
        Delega reglas y persistencia a RestauranteServicio.
        """
        usuario = self.usuario_var.get().strip()
        if not usuario:
            self._mostrar_estado("Error: Ingrese el nombre de usuario o seleccione una fila para actualizar.", error=True)
            messagebox.showwarning("Atención", "Debe especificar el usuario que desea actualizar.")
            return

        password = self.password_var.get().strip() or None
        nombre = self.user_nombre_var.get().strip() or None
        correo = self.user_correo_var.get().strip() or None
        rol = self.user_rol_var.get().strip() or None

        exito, mensaje = self.restaurante_servicio.actualizar_usuario(
            usuario, password=password, nombre=nombre, correo=correo, rol=rol
        )
        if exito:
            self._mostrar_usuarios_lista()
            self._recargar_comboboxes_venta()
            self._mostrar_estado(mensaje)
            messagebox.showinfo("Actualización Exitosa", mensaje)
        else:
            self._mostrar_estado(mensaje, error=True)
            messagebox.showwarning("Error al Actualizar", mensaje)

    def eliminar_usuario(self) -> None:
        """
        Elimina un usuario del sistema previa confirmación obligatoria.
        Protege la cuenta administrativa actualmente en sesión para evitar eliminaciones accidentales.
        """
        usuario = self.usuario_var.get().strip()
        if not usuario:
            seleccion = self.user_tree.selection() if hasattr(self, "user_tree") else None
            if seleccion:
                valores = self.user_tree.item(seleccion[0], "values")
                if valores and valores[0] != "-":
                    usuario = str(valores[2]).strip() if len(valores) > 2 else str(valores[0]).strip()

        if not usuario:
            self._mostrar_estado("Error: Seleccione un usuario de la tabla para eliminar.", error=True)
            messagebox.showwarning("Atención", "Debe seleccionar un usuario de la tabla para eliminar.")
            return

        # Protección de cuenta en sesión activa
        usuario_actual = self.restaurante_servicio.obtener_usuario_actual()
        if usuario_actual and usuario_actual.usuario == usuario:
            self._mostrar_estado("Error: No es posible eliminar la cuenta del administrador en sesión activa.", error=True)
            messagebox.showerror(
                "Operación No Permitida",
                f"No puede eliminar la cuenta '{usuario}' porque corresponde a la sesión actualmente autenticada."
            )
            return

        # Confirmación previa
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar permanentemente al usuario '{usuario}'?\nEsta acción no se puede deshacer.",
            icon="warning",
        )
        if not confirmacion:
            self._mostrar_estado("Operación de eliminación cancelada por el usuario.")
            return

        exito, mensaje = self.restaurante_servicio.eliminar_usuario(usuario)
        if exito:
            self._mostrar_usuarios_lista()
            self._recargar_comboboxes_venta()
            self._limpiar_formulario_usuario()
            self._mostrar_estado(mensaje)
            messagebox.showinfo("Usuario Eliminado", mensaje)
        else:
            self._mostrar_estado(mensaje, error=True)
            messagebox.showerror("Error al Eliminar", mensaje)

    def _limpiar_formulario_usuario(self) -> None:
        """
        Limpia los campos del formulario de usuario, cancela la selección activa en el Treeview
        y devuelve el foco al campo inicial. Reutilizado por el botón Limpiar y por <Escape>.
        """
        self.user_id_var.set("")
        self.usuario_var.set("")
        self.password_var.set("")
        self.user_nombre_var.set("")
        self.user_correo_var.set("")
        self.user_rol_var.set("Cliente")
        self._actualizar_info_rol("Cliente")
        if hasattr(self, "user_tree"):
            seleccion = self.user_tree.selection()
            if seleccion:
                self.user_tree.selection_remove(seleccion)
        if hasattr(self, "user_usuario_entry"):
            self.user_usuario_entry.focus_set()

    # ==================================================================
    # 5. REFRESCAR TODO EL SISTEMA
    # ==================================================================
    def refrescar_todo(self) -> None:
        """Actualiza todas las vistas, tablas y selectores con los datos actuales."""
        self._actualizar_tabla()
        self._mostrar_usuarios_lista()
        self._actualizar_tabla_ventas()
        self._recargar_comboboxes_venta()
        self._limpiar_formulario()
        self._limpiar_formulario_usuario()
        self._limpiar_formulario_venta()
        self.mostrar_inicio()
