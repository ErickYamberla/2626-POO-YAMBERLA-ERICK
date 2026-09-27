# Restaurante App - Semana 15: Fundamentos de Manejo de Eventos y Gestión de Ventas

**Estudiante:** Erick Yamberla  
**Materia:** Programación Orientada a Objetos  
**Semana:** 15 - Manejo de Eventos en Interfaces Gráficas con Tkinter  

---

## Propósito de la Semana 15

El objetivo central de esta práctica es comprender y aplicar los **fundamentos básicos del manejo de eventos** en entornos gráficos con Python y Tkinter. En esta etapa, el contexto práctico del restaurante evoluciona al integrar un módulo de **Ventas**, demostrando cómo un componente interactivo activa un callback mediante el parámetro `command=` y cómo este delega la lógica de negocio a la capa de servicios (`RestauranteServicio`) y la persistencia a archivos JSON (`ventas.json`), sin saturar ni acoplar la interfaz de usuario con la lógica del dominio.

---

## Evolución sobre la Semana 14

Partiendo de la base desarrollada en la Semana 14 (autenticación, navegación modular, consulta de usuarios y gestión de productos), en la Semana 15 se implementaron las siguientes evoluciones clave:

1. **Incorporación del Módulo de Ventas:**
   - Se añadió la pestaña y sección interactiva **Ventas** dentro del panel principal (`MainView`).
   - Se creó el modelo `Venta` (`modelos/venta.py`) que vincula a un cliente/usuario con un producto, registrando código de operación, cantidad, precio unitario, total calculado y fecha/hora exacta.
2. **Flujo de Eventos Desacoplado:**
   - Implementación del botón **"Registrar Venta"** vinculado mediante `command=self.registrar_venta`.
   - El callback coordina la captura de datos de la interfaz y delega la validación, actualización de stock y persistencia a `RestauranteServicio`.
3. **Persistencia en `ventas.json`:**
   - Se extendió `ArchivoServicio` para serializar y deserializar las transacciones en `datos/ventas.json`, asegurando que al reiniciar la aplicación se conserven todas las operaciones realizadas.
4. **Experiencia de Usuario Enriquecida:**
   - **Selectores informativos (`ttk.Combobox`):** Muestran el detalle completo de usuarios (código, nombre, correo) y de productos (código, nombre, categoría, precio y stock actual).
   - **Fichas dinámicas de cliente y producto:** Al seleccionar un usuario o producto en los selectores, se actualizan paneles informativos con los datos específicos y se recalcula el total a pagar en tiempo real.
   - **Historial en Treeview:** Tabla visual que lista las ventas registradas con sus columnas formateadas (Código, Fecha y Hora, Cliente/Usuario, Producto Vendido, Cantidad, P. Unitario y Total).
   - **Credenciales visibles en Login:** Se incorporó un panel informativo en `LoginView` con las credenciales de acceso para evitar olvidos al iniciar sesión.
   - **Uso obligatorio de la carpeta `assets/`:** Se integró el logotipo del restaurante (`logo.png`) y un conjunto de íconos temáticos (`icon_app.png`, `icon_inicio.png`, `icon_ventas.png`, `icon_productos.png`, `icon_usuarios.png`, `icon_logout.png`, `icon_check.png`) que aportan consistencia visual a la interfaz.
   - **Ampliación de datos:** Se expandió el catálogo inicial a 7 usuarios y 7 productos representativos del restaurante.

---

## Estructura del Repositorio

```text
Repositorio GitHub
├── restaurante_app/
│   ├── datos/
│   │   ├── productos.json
│   │   ├── usuarios.json
│   │   └── ventas.json
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── producto.py
│   │   ├── usuario.py
│   │   └── venta.py
│   ├── servicios/
│   │   ├── __init__.py
│   │   ├── archivo_servicio.py
│   │   └── restaurante_servicio.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── login_view.py
│   │   └── main_view.py
│   ├── assets/              (obligatorio: íconos, logo/logotipo y recursos visuales)
│   └── main.py
└── README.md
```

---

## Fundamento de Manejo de Eventos

La arquitectura de la aplicación evidencia con claridad el ciclo de eventos:

```text
USUARIO (Selecciona cliente, producto, cantidad e interactúa con la UI)
   ↓
BOTÓN "Registrar Venta"
   ↓
command=self.registrar_venta  (Referencia al callback, sin invocarlo con paréntesis)
   ↓
CALLBACK (Obtiene entradas de la UI, valida formato básico y solicita la operación)
   ↓
RestauranteServicio.registrar_venta() (Valida reglas de negocio: usuario existe, producto existe, stock suficiente)
   ↓
PERSISTENCIA (Descuenta stock en 'productos.json' y almacena la venta en 'ventas.json')
   ↓
RESPUESTA VISUAL (Actualización automática de Treeview de ventas, stock en tabla de productos y barra de estado)
```

> **Regla de oro aplicada:** La interfaz de usuario (`MainView`) no escribe ni lee directamente archivos JSON, ni ejecuta lógica contable de stock; toda operación es delegada a `RestauranteServicio`.

---

## Persistencia de Datos

Los datos del sistema se gestionan a través de la carpeta `restaurante_app/datos/`:
- `usuarios.json`: Conserva los usuarios del sistema, sus credenciales y datos de contacto.
- `productos.json`: Conserva la carta de productos, categorías, precios y stock disponible.
- `ventas.json`: Almacena el historial permanente de ventas registradas.

---

## Credenciales de Acceso para Pruebas

Para mayor facilidad de uso, las credenciales están detalladas en un panel dentro de la ventana de login:

| Usuario | Contraseña | Nombre Completo | Rol / Perfil |
| :--- | :--- | :--- | :--- |
| `admin` | `admin123` | Administrador General | Administrador |
| `carlos` | `carlos456` | Carlos Gómez | Cliente Registrado |
| `empleado` | `1234` | Empleado de Turno | Operador |
| `erick` | `erick2026` | Erick Yamberla | Cliente Registrado |
| `maria` | `maria789` | María López | Cliente Registrado |
| `juan` | `juan321` | Juan Pérez | Cliente Registrado |
| `ana` | `ana654` | Ana Torres | Cliente Registrada |

---

## Instrucciones para Ejecutar la Aplicación

1. **Requisitos:**
   - Python 3.10 o superior (incluye Tkinter estándar).

2. **Ejecución desde la raíz del proyecto:**
   ```bash
   python PARCIAL_2/SEMANA_15/restaurante_app/main.py
   ```

3. **Ejecución desde la carpeta `PARCIAL_2/SEMANA_15`:**
   ```bash
   python restaurante_app/main.py
   ```

4. **Flujo de prueba recomendado:**
   - Inicie sesión con el usuario `admin` y contraseña `admin123`.
   - Navegue a la sección **Ventas** desde la barra superior.
   - Seleccione un cliente en el primer selector desplegable y observe la ficha de datos del cliente.
   - Seleccione un producto en el segundo selector desplegable y verifique la ficha técnica y stock disponible.
   - Ajuste la cantidad y confirme el cálculo del total estimado.
   - Presione el botón **"Registrar Venta"** para activar el evento `command=`.
   - Observe la confirmación en la barra de estado inferior y el nuevo registro en la tabla Treeview de ventas.
   - Navegue a **Productos** para comprobar que el stock del producto disminuyó según la cantidad vendida.
   - Reinicie la aplicación para verificar que los datos persisten en `ventas.json`.
