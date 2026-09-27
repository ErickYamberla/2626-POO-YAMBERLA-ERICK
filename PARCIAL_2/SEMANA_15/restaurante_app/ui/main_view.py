import tkinter as tk
from tkinter import ttk
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
            text="Restaurante App - Semana 15",
            fg="white",
            bg="#111827",
            font=("Segoe UI", 13, "bold"),
        )
        title.pack(side="left")

        # Botones de navegación (Inicio, Ventas, Productos, Usuarios, Salir)
        nav_buttons = [
            ("Cerrar sesión", self.on_logout, "logout"),
            ("Usuarios", self.mostrar_usuarios, "usuarios"),
            ("Productos", self.mostrar_productos, "productos"),
            ("Ventas", self.mostrar_ventas, "ventas"),
            ("Inicio", self.mostrar_inicio, "inicio"),
        ]

        for text, cmd, icon_key in nav_buttons:
            btn_kwargs = {"text": f" {text} ", "command": cmd}
            if icon_key in self._icons:
                btn_kwargs["image"] = self._icons[icon_key]
                btn_kwargs["compound"] = "left"
            btn = ttk.Button(self.toolbar, **btn_kwargs)
            btn.pack(side="right", padx=(0, 6))

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

        # Variables de formulario de Usuarios
        self.usuario_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.user_nombre_var = tk.StringVar()
        self.user_correo_var = tk.StringVar()

        # Variables de formulario de Ventas (Semana 15)
        self.venta_usuario_sel = tk.StringVar()
        self.venta_producto_sel = tk.StringVar()
        self.venta_cantidad_var = tk.StringVar(value="1")
        self.venta_cantidad_var.trace_add("write", lambda *args: self._recalcular_total_venta())

        # Contenedores de secciones
        self.dashboard = None
        self._construir_seccion_ventas()
        self._construir_seccion_productos()
        self._construir_seccion_usuarios()

        # Barra de estado inferior
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
        self.status_var.set(mensaje)
        self.status_label.config(fg="#b91c1c" if error else "#047857", font=("Segoe UI", 9, "bold" if error else "normal"))

    def _mostrar_seccion(self, seccion: tk.Frame) -> None:
        for widget in (self.dashboard, self.sales_section, self.product_section, self.user_section):
            try:
                if widget is not None:
                    widget.pack_forget()
            except Exception:
                pass
        seccion.pack(fill="both", expand=True)

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
            text="Panel de control principal - Guía de navegación y manual de operaciones del restaurante.",
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
            ("Total Recaudado", f"S/. {recaudado:.2f}", "#f3e8ff", "#6b21a8"),
        ]

        for titulo, valor, bg_col, fg_col in card_data:
            c = tk.Frame(cards, bg=bg_col, padx=18, pady=12, relief="solid", borderwidth=1)
            c.pack(side="left", padx=(0, 14), fill="y")
            tk.Label(c, text=titulo, font=("Segoe UI", 10, "bold"), bg=bg_col, fg=fg_col).pack(anchor="w")
            tk.Label(c, text=valor, font=("Segoe UI", 13, "bold"), bg=bg_col, fg="#0f172a").pack(anchor="w", pady=(2, 0))

        # Contenedor principal de la Guía / Manual de Uso del Sistema
        guide_frame = tk.LabelFrame(
            self.dashboard,
            text=" 📖 Manual de Uso y Guía Rápida del Sistema ",
            bg="white",
            fg="#0f172a",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=12,
            relief="solid",
            borderwidth=1,
        )
        guide_frame.pack(fill="both", expand=True, pady=(4, 0))

        grid_container = tk.Frame(guide_frame, bg="white")
        grid_container.pack(fill="both", expand=True)
        grid_container.columnconfigure(0, weight=1)
        grid_container.columnconfigure(1, weight=1)
        grid_container.rowconfigure(0, weight=1)
        grid_container.rowconfigure(1, weight=1)

        modulos = [
            (
                "🛒 Módulo de Ventas (Pedidos y Facturación)",
                "#f0fdf4",
                "#15803d",
                (
                    "• 1. Seleccione el Cliente/Usuario desde el selector desplegable.\n"
                    "• 2. Elija el Producto del menú: observará su precio, categoría y stock en tiempo real.\n"
                    "• 3. Indique la Cantidad requerida: el Total a Pagar se calculará automáticamente.\n"
                    "• 4. Presione 'Registrar Venta' para confirmar la transacción, descontar inventario y registrarla."
                ),
                0, 0
            ),
            (
                "🍽️ Módulo de Productos (Carta y Menú)",
                "#eff6ff",
                "#1d4ed8",
                (
                    "• 1. Registrar: Ingrese código, nombre, categoría, precio y stock para añadir productos a la carta.\n"
                    "• 2. Cargar por Código: Busque un producto para consultar sus detalles actuales.\n"
                    "• 3. Actualizar: Modifique precios o incremente el stock cuando reciba nuevo inventario.\n"
                    "• 4. Eliminar: Retire del menú productos agotados o descontinuados."
                ),
                0, 1
            ),
            (
                "👥 Módulo de Usuarios (Cuentas y Clientes)",
                "#faf5ff",
                "#7e22ce",
                (
                    "• 1. Registrar: Dé de alta clientes y personal del restaurante con sus datos de acceso.\n"
                    "• 2. Cargar: Busque por nombre de usuario para consultar correo o datos personales.\n"
                    "• 3. Actualizar: Modifique credenciales de acceso o datos de contacto según se requiera.\n"
                    "• 4. Eliminar: Dé de baja cuentas que ya no requieran acceso al sistema."
                ),
                1, 0
            ),
            (
                "💡 Consejos de Operación y Navegación",
                "#fffbeb",
                "#b45309",
                (
                    "• Barra superior: Cambie entre secciones usando los botones de navegación con íconos.\n"
                    "• Barra inferior: Revise los mensajes de estado en verde (éxito) o rojo (alertas y errores).\n"
                    "• Persistencia automática: Todas las ventas, productos y usuarios se guardan en tiempo real.\n"
                    "• Seguridad: Presione 'Cerrar sesión' al finalizar su turno para resguardar la aplicación."
                ),
                1, 1
            )
        ]

        for titulo, bg_color, title_color, descripcion, row, col in modulos:
            box = tk.Frame(grid_container, bg=bg_color, padx=12, pady=10, relief="solid", borderwidth=1)
            box.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

            tk.Label(
                box,
                text=titulo,
                font=("Segoe UI", 9, "bold"),
                bg=bg_color,
                fg=title_color,
                anchor="w",
            ).pack(fill="x", pady=(0, 4))

            tk.Label(
                box,
                text=descripcion,
                font=("Segoe UI", 8),
                bg=bg_color,
                fg="#334155",
                justify="left",
                anchor="w",
            ).pack(fill="both", expand=True)

        self._mostrar_estado("Panel principal cargado. Seleccione una sección en la barra superior.")

    # ==================================================================
    # 2. SECCIÓN VENTAS (Semana 15)
    # ==================================================================
    def _construir_seccion_ventas(self) -> None:
        self.sales_section = tk.Frame(self.workspace, bg="#edf2ff")

        # Contenedor izquierdo: Formulario de Registro de Venta
        self.sales_form_container = tk.LabelFrame(
            self.sales_section,
            text=" Registrar Nueva Venta ",
            bg="white",
            fg="#0f172a",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=12,
            relief="solid",
            borderwidth=1,
        )
        self.sales_form_container.pack(side="left", fill="y", padx=(0, 14))

        # --- Selección de Cliente / Usuario ---
        tk.Label(
            self.sales_form_container,
            text="Cliente / Usuario (Seleccionar):",
            bg="white",
            fg="#1f2937",
            font=("Segoe UI", 9, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(0, 2))

        self.combo_usuario = ttk.Combobox(
            self.sales_form_container,
            textvariable=self.venta_usuario_sel,
            state="readonly",
            width=36,
            font=("Segoe UI", 9),
        )
        self.combo_usuario.pack(fill="x", pady=(0, 6))
        self.combo_usuario.bind("<<ComboboxSelected>>", self._on_usuario_cambiado)

        # Ficha / Tarjeta de detalles del Cliente
        self.card_cliente = tk.Frame(self.sales_form_container, bg="#f8fafc", padx=10, pady=8, relief="groove", borderwidth=1)
        self.card_cliente.pack(fill="x", pady=(0, 10))

        self.lbl_cli_usuario = tk.Label(self.card_cliente, text="Usuario: -", font=("Segoe UI", 8), bg="#f8fafc", fg="#334155", anchor="w")
        self.lbl_cli_usuario.pack(fill="x")
        self.lbl_cli_nombre = tk.Label(self.card_cliente, text="Nombre: -", font=("Segoe UI", 8), bg="#f8fafc", fg="#334155", anchor="w")
        self.lbl_cli_nombre.pack(fill="x")
        self.lbl_cli_correo = tk.Label(self.card_cliente, text="Correo: -", font=("Segoe UI", 8), bg="#f8fafc", fg="#334155", anchor="w")
        self.lbl_cli_correo.pack(fill="x")

        # --- Selección de Producto ---
        tk.Label(
            self.sales_form_container,
            text="Producto del Menú (Seleccionar):",
            bg="white",
            fg="#1f2937",
            font=("Segoe UI", 9, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(0, 2))

        self.combo_producto = ttk.Combobox(
            self.sales_form_container,
            textvariable=self.venta_producto_sel,
            state="readonly",
            width=36,
            font=("Segoe UI", 9),
        )
        self.combo_producto.pack(fill="x", pady=(0, 6))
        self.combo_producto.bind("<<ComboboxSelected>>", self._on_producto_cambiado)

        # Ficha / Tarjeta de detalles del Producto
        self.card_producto = tk.Frame(self.sales_form_container, bg="#f8fafc", padx=10, pady=8, relief="groove", borderwidth=1)
        self.card_producto.pack(fill="x", pady=(0, 10))

        self.lbl_prod_codigo = tk.Label(self.card_producto, text="Código: -", font=("Segoe UI", 8), bg="#f8fafc", fg="#334155", anchor="w")
        self.lbl_prod_codigo.pack(fill="x")
        self.lbl_prod_nombre = tk.Label(self.card_producto, text="Nombre: -", font=("Segoe UI", 8), bg="#f8fafc", fg="#334155", anchor="w")
        self.lbl_prod_nombre.pack(fill="x")
        self.lbl_prod_cat = tk.Label(self.card_producto, text="Categoría: -", font=("Segoe UI", 8), bg="#f8fafc", fg="#334155", anchor="w")
        self.lbl_prod_cat.pack(fill="x")
        self.lbl_prod_precio = tk.Label(self.card_producto, text="Precio: S/. 0.00", font=("Segoe UI", 8, "bold"), bg="#f8fafc", fg="#1e40af", anchor="w")
        self.lbl_prod_precio.pack(fill="x")
        self.lbl_prod_stock = tk.Label(self.card_producto, text="Stock Disponible: 0", font=("Segoe UI", 8), bg="#f8fafc", fg="#166534", anchor="w")
        self.lbl_prod_stock.pack(fill="x")

        # --- Cantidad y Total Estimado ---
        calc_frame = tk.Frame(self.sales_form_container, bg="white")
        calc_frame.pack(fill="x", pady=(2, 10))

        tk.Label(calc_frame, text="Cantidad:", bg="white", font=("Segoe UI", 9, "bold"), fg="#1f2937").pack(side="left")
        self.spin_cantidad = ttk.Spinbox(
            calc_frame,
            from_=1,
            to=999,
            textvariable=self.venta_cantidad_var,
            width=8,
            font=("Segoe UI", 10),
        )
        self.spin_cantidad.pack(side="left", padx=(8, 0))

        # Cuadro de Total Calculado
        total_box = tk.Frame(self.sales_form_container, bg="#f0fdf4", padx=10, pady=8, relief="solid", borderwidth=1)
        total_box.pack(fill="x", pady=(0, 14))

        tk.Label(total_box, text="TOTAL A PAGAR:", font=("Segoe UI", 9, "bold"), bg="#f0fdf4", fg="#166534").pack(anchor="w")
        self.lbl_total_estimado = tk.Label(
            total_box,
            text="S/. 0.00",
            font=("Segoe UI", 14, "bold"),
            bg="#f0fdf4",
            fg="#15803d",
        )
        self.lbl_total_estimado.pack(anchor="e")

        # --- Botones de Acción (command=callback fundamental) ---
        btn_box = tk.Frame(self.sales_form_container, bg="white")
        btn_box.pack(fill="x", pady=(4, 0))

        # Botón Registrar Venta obligatorio con command=self.registrar_venta
        btn_registrar_kwargs = {"text": " Registrar Venta", "command": self.registrar_venta}
        if "check" in self._icons:
            btn_registrar_kwargs["image"] = self._icons["check"]
            btn_registrar_kwargs["compound"] = "left"

        self.btn_registrar_venta = ttk.Button(btn_box, **btn_registrar_kwargs)
        self.btn_registrar_venta.pack(fill="x", pady=(0, 6), ipady=3)

        ttk.Button(
            btn_box,
            text="Limpiar Selección",
            command=self._limpiar_formulario_venta,
        ).pack(fill="x")

        # Contenedor derecho: Listado de Ventas en Treeview
        self.sales_table_container = tk.LabelFrame(
            self.sales_section,
            text=" Historial de Ventas Registradas (ventas.json) ",
            bg="white",
            fg="#0f172a",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=10,
            relief="solid",
            borderwidth=1,
        )
        self.sales_table_container.pack(side="left", fill="both", expand=True)

        columns = ("codigo", "fecha", "usuario", "producto", "cantidad", "precio_unitario", "total")
        self.ventas_tree = ttk.Treeview(
            self.sales_table_container,
            columns=columns,
            show="headings",
            height=18,
        )

        self.ventas_tree.heading("codigo", text="Código")
        self.ventas_tree.heading("fecha", text="Fecha y Hora")
        self.ventas_tree.heading("usuario", text="Cliente / Usuario")
        self.ventas_tree.heading("producto", text="Producto Vendido")
        self.ventas_tree.heading("cantidad", text="Cant.")
        self.ventas_tree.heading("precio_unitario", text="P. Unitario")
        self.ventas_tree.heading("total", text="Total")

        self.ventas_tree.column("codigo", width=75, anchor="center")
        self.ventas_tree.column("fecha", width=140, anchor="center")
        self.ventas_tree.column("usuario", width=130, anchor="w")
        self.ventas_tree.column("producto", width=190, anchor="w")
        self.ventas_tree.column("cantidad", width=65, anchor="center")
        self.ventas_tree.column("precio_unitario", width=90, anchor="center")
        self.ventas_tree.column("total", width=95, anchor="center")

        ventas_scroll = ttk.Scrollbar(self.sales_table_container, orient="vertical", command=self.ventas_tree.yview)
        self.ventas_tree.configure(yscrollcommand=ventas_scroll.set)
        self.ventas_tree.pack(side="left", fill="both", expand=True)
        ventas_scroll.pack(side="right", fill="y")

        # Barra de resumen de la tabla
        self.ventas_summary_bar = tk.Frame(self.sales_table_container, bg="white", pady=6)
        self.ventas_summary_bar.pack(fill="x", side="bottom")

        self.lbl_ventas_resumen = tk.Label(
            self.ventas_summary_bar,
            text="Total Ventas: 0 | Recaudación Acumulada: S/. 0.00",
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
        """Carga en los select box los usuarios y productos con detalles completos."""
        usuarios = self.restaurante_servicio.listar_usuarios()
        user_values = [
            f"{u.usuario} - {u.nombre} ({u.correo})"
            for u in usuarios
        ]
        self.combo_usuario["values"] = user_values

        productos = self.restaurante_servicio.listar_productos()
        prod_values = [
            f"{p.codigo} - {p.nombre} | S/. {p.precio:.2f} | Stock: {p.stock}"
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
            self.lbl_cli_nombre.config(text=f"Nombre: {usuario.nombre}")
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
            self.lbl_prod_precio.config(text=f"Precio: S/. {producto.precio:.2f}")
            self.lbl_prod_stock.config(text=f"Stock Disponible: {producto.stock} unidades")
        else:
            self.lbl_prod_codigo.config(text="Código: -")
            self.lbl_prod_nombre.config(text="Nombre: -")
            self.lbl_prod_cat.config(text="Categoría: -")
            self.lbl_prod_precio.config(text="Precio: S/. 0.00")
            self.lbl_prod_stock.config(text="Stock Disponible: 0")

        self._recalcular_total_venta()

    def _recalcular_total_venta(self) -> None:
        prod_code = self._extraer_codigo_producto_combo()
        producto = self.restaurante_servicio.buscar_producto(prod_code)
        if not producto:
            self.lbl_total_estimado.config(text="S/. 0.00")
            return

        try:
            cant = int(self.venta_cantidad_var.get().strip())
            if cant <= 0:
                self.lbl_total_estimado.config(text="S/. 0.00")
                return
            total = cant * producto.precio
            self.lbl_total_estimado.config(text=f"S/. {total:.2f}")
        except ValueError:
            self.lbl_total_estimado.config(text="S/. 0.00")

    def registrar_venta(self) -> None:
        """
        CALLBACK DEL BOTÓN 'Registrar Venta' (command=self.registrar_venta).
        Obtiene las selecciones de la UI, delega la operación a RestauranteServicio,
        actualiza la vista y notifica al usuario.
        """
        user_key = self._extraer_clave_usuario_combo()
        prod_code = self._extraer_codigo_producto_combo()
        cant_str = self.venta_cantidad_var.get().strip()

        if not user_key:
            self._mostrar_estado("Debe seleccionar un cliente/usuario para registrar la venta.", error=True)
            return

        if not prod_code:
            self._mostrar_estado("Debe seleccionar un producto para registrar la venta.", error=True)
            return

        try:
            cant = int(cant_str)
        except ValueError:
            self._mostrar_estado("La cantidad debe ser un número entero válido.", error=True)
            return

        # Delegar la operación completa a la capa de servicio
        exito, mensaje, venta = self.restaurante_servicio.registrar_venta(
            usuario_clave=user_key,
            producto_codigo=prod_code,
            cantidad=cant,
        )

        if not exito:
            self._mostrar_estado(mensaje, error=True)
            return

        # Actualizar visualmente la tabla de ventas, comboboxes y fichas
        self._actualizar_tabla_ventas()
        self._actualizar_tabla()
        self._recargar_comboboxes_venta()
        self._on_producto_cambiado()
        self._mostrar_estado(mensaje)

        # Restablecer cantidad a 1
        self.venta_cantidad_var.set("1")

    def _actualizar_tabla_ventas(self) -> None:
        if not hasattr(self, "ventas_tree"):
            return

        for item in self.ventas_tree.get_children():
            self.ventas_tree.delete(item)

        ventas = self.restaurante_servicio.listar_ventas()
        total_acumulado = 0.0

        for v in ventas:
            total_acumulado += v.total
            self.ventas_tree.insert(
                "",
                tk.END,
                values=(
                    v.codigo,
                    v.fecha,
                    v.usuario,
                    v.producto_nombre,
                    v.cantidad,
                    f"S/. {v.precio_unitario:.2f}",
                    f"S/. {v.total:.2f}",
                ),
            )

        if not ventas:
            self.ventas_tree.insert("", tk.END, values=("-", "-", "No hay ventas registradas", "-", "-", "-", "-"))

        if hasattr(self, "lbl_ventas_resumen"):
            self.lbl_ventas_resumen.config(
                text=f"Total Ventas: {len(ventas)} | Recaudación Acumulada: S/. {total_acumulado:.2f}"
            )

    def _limpiar_formulario_venta(self) -> None:
        self.venta_usuario_sel.set("")
        self.venta_producto_sel.set("")
        self.venta_cantidad_var.set("1")
        self._on_usuario_cambiado()
        self._on_producto_cambiado()
        self._mostrar_estado("Formulario de venta restablecido.")

    # ==================================================================
    # 3. SECCIÓN PRODUCTOS
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
            ("Precio (S/.)", self.precio_var),
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
                    f"S/. {p.precio:.2f}",
                    p.stock,
                ),
            )

        if not productos:
            self.tree.insert("", tk.END, values=("-", "No hay productos", "-", "-", "-"))

    def consultar_producto(self) -> None:
        codigo = self.codigo_var.get().strip()
        if not codigo:
            self._mostrar_estado("Debe ingresar el código para consultar.", error=True)
            return

        producto = self.restaurante_servicio.buscar_producto(codigo)
        if producto is None:
            self._mostrar_estado(f"No existe un producto con código {codigo}.", error=True)
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
            self._mostrar_estado("Complete todos los campos con valores numéricos válidos.", error=True)
            return

        if not codigo or not nombre or not categoria:
            self._mostrar_estado("Código, nombre y categoría son campos obligatorios.", error=True)
            return

        try:
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
    # 4. SECCIÓN USUARIOS
    # ==================================================================
    def _construir_seccion_usuarios(self) -> None:
        self.user_section = tk.Frame(self.workspace, bg="#edf2ff")

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

        self.user_list_container = tk.LabelFrame(
            self.user_section,
            text=" Usuarios Registrados ",
            bg="white",
            fg="#0f172a",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=10,
            relief="solid",
            borderwidth=1,
        )
        self.user_list_container.pack(side="left", fill="both", expand=True)

        campos = [
            ("Usuario", self.usuario_var),
            ("Contraseña", self.password_var),
            ("Nombre", self.user_nombre_var),
            ("Correo", self.user_correo_var),
        ]

        for label_text, variable in campos:
            label = tk.Label(self.user_form_container, text=f"{label_text}:", font=("Segoe UI", 9, "bold"), bg="white", fg="#374151", anchor="w")
            label.pack(fill="x", pady=(0, 2))
            if label_text == "Contraseña":
                entry = ttk.Entry(self.user_form_container, textvariable=variable, show="*", width=30, font=("Segoe UI", 10))
            else:
                entry = ttk.Entry(self.user_form_container, textvariable=variable, width=30, font=("Segoe UI", 10))
            entry.pack(fill="x", pady=(0, 8))
            if label_text == "Usuario":
                self.user_usuario_entry = entry

        btn_usr_frame = tk.Frame(self.user_form_container, bg="white")
        btn_usr_frame.pack(fill="x", pady=(6, 0))

        ttk.Button(btn_usr_frame, text="Registrar Usuario", command=self.registrar_usuario).pack(fill="x", pady=(0, 6))
        ttk.Button(btn_usr_frame, text="Cargar por Usuario", command=self.consultar_usuario).pack(fill="x", pady=(0, 6))
        ttk.Button(btn_usr_frame, text="Actualizar Usuario", command=self.actualizar_usuario).pack(fill="x", pady=(0, 6))
        ttk.Button(btn_usr_frame, text="Eliminar Usuario", command=self.eliminar_usuario).pack(fill="x", pady=(0, 6))
        ttk.Button(btn_usr_frame, text="Limpiar Campos", command=self._limpiar_formulario_usuario).pack(fill="x")

        columns = ("usuario", "nombre", "correo")
        self.user_tree = ttk.Treeview(self.user_list_container, columns=columns, show="headings", height=18)
        self.user_tree.heading("usuario", text="Usuario")
        self.user_tree.heading("nombre", text="Nombre Completo")
        self.user_tree.heading("correo", text="Correo Electrónico")

        self.user_tree.column("usuario", width=120, anchor="center")
        self.user_tree.column("nombre", width=190, anchor="w")
        self.user_tree.column("correo", width=220, anchor="w")

        user_scroll = ttk.Scrollbar(self.user_list_container, orient="vertical", command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=user_scroll.set)
        self.user_tree.pack(side="left", fill="both", expand=True)
        user_scroll.pack(side="right", fill="y")

    def mostrar_usuarios(self) -> None:
        self._mostrar_usuarios_lista()
        self._mostrar_seccion(self.user_section)
        self._mostrar_estado("Sección de usuarios activa.")

    def _mostrar_usuarios_lista(self) -> None:
        if not hasattr(self, "user_tree"):
            return
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)

        usuarios = self.restaurante_servicio.listar_usuarios()
        for u in usuarios:
            self.user_tree.insert("", tk.END, values=(u.usuario, u.nombre, u.correo))

        if not usuarios:
            self.user_tree.insert("", tk.END, values=("-", "No hay usuarios", "-"))

    def consultar_usuario(self) -> None:
        usuario = self.usuario_var.get().strip()
        if not usuario:
            self._mostrar_estado("Debe ingresar el nombre de usuario para consultar.", error=True)
            return

        usuario_obj = self.restaurante_servicio.buscar_usuario(usuario)
        if usuario_obj is None:
            self._mostrar_estado(f"No existe el usuario '{usuario}'.", error=True)
            return

        self.usuario_var.set(usuario_obj.usuario)
        self.password_var.set(usuario_obj.password)
        self.user_nombre_var.set(usuario_obj.nombre)
        self.user_correo_var.set(usuario_obj.correo)
        self._mostrar_estado(f"Usuario '{usuario_obj.usuario}' cargado correctamente.")

    def registrar_usuario(self) -> None:
        usuario = self.usuario_var.get().strip()
        password = self.password_var.get().strip()
        nombre = self.user_nombre_var.get().strip()
        correo = self.user_correo_var.get().strip()

        if not usuario or not password or not nombre:
            self._mostrar_estado("Usuario, contraseña y nombre son campos obligatorios.", error=True)
            return

        try:
            usuario_obj = Usuario(usuario=usuario, password=password, nombre=nombre, correo=correo)
            if not self.restaurante_servicio.registrar_usuario(usuario_obj):
                self._mostrar_estado(f"El usuario '{usuario}' ya se encuentra registrado.", error=True)
                return
        except ValueError as exc:
            self._mostrar_estado(str(exc), error=True)
            return

        self._mostrar_usuarios_lista()
        self._recargar_comboboxes_venta()
        self._limpiar_formulario_usuario()
        self._mostrar_estado(f"Usuario '{usuario}' registrado correctamente.")

    def actualizar_usuario(self) -> None:
        usuario = self.usuario_var.get().strip()
        if not usuario:
            self._mostrar_estado("Ingrese el usuario a actualizar.", error=True)
            return

        if self.restaurante_servicio.buscar_usuario(usuario) is None:
            self._mostrar_estado(f"No existe el usuario '{usuario}'.", error=True)
            return

        password = self.password_var.get().strip() or None
        nombre = self.user_nombre_var.get().strip() or None
        correo = self.user_correo_var.get().strip() or None

        if self.restaurante_servicio.actualizar_usuario(usuario, password=password, nombre=nombre, correo=correo):
            self._mostrar_usuarios_lista()
            self._recargar_comboboxes_venta()
            self._mostrar_estado(f"Usuario '{usuario}' actualizado exitosamente.")
        else:
            self._mostrar_estado(f"No se pudo actualizar el usuario '{usuario}'.", error=True)

    def eliminar_usuario(self) -> None:
        usuario = self.usuario_var.get().strip()
        if not usuario:
            self._mostrar_estado("Ingrese el usuario a eliminar.", error=True)
            return

        if self.restaurante_servicio.eliminar_usuario(usuario):
            self._mostrar_usuarios_lista()
            self._recargar_comboboxes_venta()
            self._limpiar_formulario_usuario()
            self._mostrar_estado(f"Usuario '{usuario}' eliminado satisfactoriamente.")
        else:
            self._mostrar_estado(f"No existe el usuario '{usuario}'.", error=True)

    def _limpiar_formulario_usuario(self) -> None:
        self.usuario_var.set("")
        self.password_var.set("")
        self.user_nombre_var.set("")
        self.user_correo_var.set("")
        if hasattr(self, "user_usuario_entry"):
            self.user_usuario_entry.focus_set()

    # ==================================================================
    # 5. REFRESCAR TODO EL SISTEMA
    # ==================================================================
    def refrescar_todo(self) -> None:
        self._actualizar_tabla()
        self._mostrar_usuarios_lista()
        self._actualizar_tabla_ventas()
        self._recargar_comboboxes_venta()
        self._limpiar_formulario()
        self._limpiar_formulario_usuario()
        self._limpiar_formulario_venta()
        self.mostrar_inicio()
