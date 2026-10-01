# Restaurante App - Semana 16: Manejo de Eventos en Tablas, Formularios y Gestión de Roles

**Estudiante:** Erick Yamberla  
**Materia:** Programación Orientada a Objetos  
**Semana:** 16 - Manejo de Eventos Avanzado en Tkinter (`bind`, eventos virtuales, atajos de teclado y callbacks)

---

## Propósito de la Semana 16

El objetivo central de esta práctica es aplicar de manera rigurosa y práctica el **manejo de eventos** en interfaces gráficas de usuario con Python y Tkinter. En esta etapa, el contexto del restaurante evoluciona al expandir la sección de **Gestión de Usuarios**, utilizándola como escenario para demostrar cómo diferentes interacciones (selección en tabla, teclas de atajo o cambios en selectores desplegables) activan callbacks mediante `bind()` sin concentrar ni acoplar la lógica de negocio dentro de la vista.

Se evidencia de forma estricta el flujo arquitectónico:
$$\text{Interacción del usuario} \longrightarrow \text{Evento} \longrightarrow \text{bind()} \longrightarrow \text{Callback} \longrightarrow \text{Servicio} \longrightarrow \text{Persistencia} \longrightarrow \text{Respuesta Visual}$$

---

## Evolución sobre la Semana 15

Partiendo de la base de la Semana 15 (autenticación, navegación modular, catálogo de productos y registro de ventas persistentes), en la Semana 16 se desarrollaron las siguientes evoluciones clave:

1. **Evolución del Módulo de Usuarios:**
   - La sección de Usuarios pasó de una visualización básica a un **CRUD completo** (Registrar, Consultar, Actualizar y Eliminar) directamente operable desde la interfaz gráfica.
2. **Incorporación de Roles en el Modelo Usuario:**
   - Se añadió el atributo `rol` al modelo `Usuario` (`modelos/usuario.py`) y a la persistencia (`datos/usuarios.json`), soportando tres perfiles diferenciados: **`Administrador`**, **`Empleado`** y **`Cliente`**.
3. **Control de Acceso y Seguridad de Sesión:**
   - Únicamente los usuarios con rol de **Administrador** pueden acceder a la gestión administrativa de usuarios. Para cuentas de Empleado o Cliente, el botón se deshabilita y se restringe el acceso con advertencias visuales.
   - **Protección de cuenta activa:** `RestauranteServicio` impide la eliminación accidental de la cuenta administrativa que se encuentra autenticada en la sesión actual.
4. **Manejo de Eventos con `bind()` vs `command=`:**
   - Implementación de eventos virtuales de `ttk` (`<<TreeviewSelect>>`, `<<ComboboxSelected>>`) y eventos de teclado (`<Return>`, `<Escape>`).
   - Diferenciación clara entre los botones de acción principal vinculados mediante `command=` y los escuchadores de interacción vinculados mediante `bind()`.
5. **Reutilización y Desacoplamiento:**
   - Los callbacks de eventos no duplican lógica; por ejemplo, `<Return>` reutiliza directamente el método `registrar_usuario()`, y `<Escape>` reutiliza `_limpiar_formulario_usuario()`.
   - La tabla Treeview no almacena datos sensibles como contraseñas; utiliza el identificador seleccionado para consultar el objeto mediante `RestauranteServicio`.
   - Toda validación y persistencia reside exclusivamente en `RestauranteServicio` y `ArchivoServicio`.

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

## Modelo de Dominio y Atributo Rol

El modelo `Usuario` (`modelos/usuario.py`) representa a los diferentes actores del restaurante:

- **`id`**: Identificador correlativo del usuario (ej. `USR-001`, `USR-002`).
- **`usuario`**: Nombre de usuario único para credenciales de acceso.
- **`password`**: Contraseña de autenticación (gestionada de forma segura fuera de la tabla pública).
- **`nombre`**: Nombre completo del titular.
- **`correo`**: Dirección de correo electrónico de contacto.
- **`rol`**: Rol asignado dentro del sistema (`Administrador`, `Empleado` o `Cliente`).

### Roles del Sistema

| Rol | Atribuciones y Privilegios en el Sistema |
| :--- | :--- |
| **`Administrador`** | Control total del sistema: gestión de carta de productos, ventas, panel de estadísticas y acceso exclusivo a la **Gestión de Usuarios** (CRUD). |
| **`Empleado`** | Operación diaria del restaurante: consulta de catálogo de productos y registro de órdenes de venta. Acceso a gestión de usuarios bloqueado. |
| **`Cliente`** | Usuario registrado para fidelización, consulta de datos y registro de consumos. Acceso administrativo bloqueado. |

---

## Flujo de Interacción y Manejo de Eventos

La interfaz gráfica captura las interacciones del usuario y delega el procesamiento sin contener reglas de negocio ni manipulación de archivos JSON:

```text
               USUARIO INTERACTÚA CON LA UI
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
 Selección en Tabla    Tecla <Return>     Cambio de Rol
<<TreeviewSelect>>       en Entrada    <<ComboboxSelected>>
        │                   │                   │
        ▼                   ▼                   ▼
  bind(callback)      bind(callback)      bind(callback)
        │                   │                   │
        ▼                   ▼                   ▼
 Obtiene Identif.     Reutiliza método     Actualiza ficha
 de fila seleccionada registrar_usuario()  y estado de rol
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                   RestauranteServicio
           (Validaciones y Reglas de Negocio)
                            ▼
                      Persistencia
                    (usuarios.json)
                            ▼
                    Respuesta Visual
        (Actualización Treeview, Formulario y Barra de Estado)
```

---

## Eventos Implementados en la Aplicación

### 1. `<<TreeviewSelect>>` (Evento Virtual de Tabla)
- **Mecanismo:** Asociado al `Treeview` de usuarios mediante:
  ```python
  self.user_tree.bind("<<TreeviewSelect>>", self._on_treeview_usuario_select)
  ```
- **Flujo:** Al hacer clic sobre cualquier fila del listado de usuarios, el callback captura el identificador público (`id`), consulta `RestauranteServicio.buscar_usuario(id)` y carga automáticamente todos los datos del usuario en los campos del formulario.
- **Seguridad:** La tabla Treeview no muestra contraseñas; los datos sensibles son recuperados directamente desde la capa de servicio.

### 2. `<<ComboboxSelected>>` (Evento Virtual de Selector de Rol)
- **Mecanismo:** Asociado al `ttk.Combobox` de roles mediante:
  ```python
  self.user_rol_combo.bind("<<ComboboxSelected>>", self._on_combobox_rol_selected)
  ```
- **Flujo:** Al elegir entre `Administrador`, `Empleado` o `Cliente`, se activa un callback que responde en tiempo real actualizando una etiqueta descriptiva en el formulario y la barra de estado con los privilegios del rol.

### 3. `<Return>` (Evento de Teclado - Confirmar Registro)
- **Mecanismo:** Asociado a las entradas de texto del formulario mediante:
  ```python
  entry.bind("<Return>", self._on_return_registrar_usuario)
  ```
- **Flujo:** Permite presionar la tecla **Enter** para ejecutar el registro del usuario. Reutiliza el método `registrar_usuario()`, evitando duplicidad de código.

### 4. `<Escape>` (Evento de Teclado - Limpiar y Deseleccionar)
- **Mecanismo:** Asociado al formulario y a la tabla mediante:
  ```python
  widget.bind("<Escape>", self._on_escape_limpiar_usuario)
  ```
- **Flujo:** Permite presionar la tecla **Esc** para cancelar la selección en el Treeview, vaciar los campos del formulario, restablecer el rol a su valor por defecto (`Cliente`) y devolver el foco al campo inicial. Reutiliza `_limpiar_formulario_usuario()`.

### 5. Botones de Acción con `command=`
- Los botones principales de la interfaz utilizan el mecanismo estándar de Tkinter:
  - **Registrar:** `command=self.registrar_usuario`
  - **Actualizar:** `command=self.actualizar_usuario`
  - **Eliminar:** `command=self.eliminar_usuario` (con confirmación modal `askyesno` y protección de la sesión activa)
  - **Limpiar:** `command=self._limpiar_formulario_usuario`

### Diferencia Conceptual: `command=` vs `bind()`

| Característica | `command=` | `bind()` |
| :--- | :--- | :--- |
| **Origen** | Exclusivo de botones o controles interactivos nativos (`Button`, `Checkbutton`). | Aplicable a cualquier widget (`Treeview`, `Entry`, `Combobox`, `Frame`, `Window`). |
| **Tipo de Evento** | Vincula únicamente la acción predeterminada de activación/clic. | Permite capturar eventos específicos: teclado (`<Return>`, `<Escape>`), ratón (`<Button-1>`), focos (`<FocusIn>`) y eventos virtuales (`<<TreeviewSelect>>`, `<<ComboboxSelected>>`). |
| **Firma del Callback** | No recibe argumentos obligatorios: `callback()`. | Recibe obligatoriamente el objeto del evento: `callback(event)`. |
| **Propósito en la App** | Disparar acciones deliberadas de guardado, actualización o borrado. | Responder de forma inmediata a la interacción contextual (selección en tabla, teclas rápidas o cambios en selectores). |

---

## Persistencia de Datos

Toda la información se mantiene sincronizada en la carpeta `restaurante_app/datos/`:
- `usuarios.json`: Almacena el catálogo de usuarios, credenciales, datos de contacto y roles (`Administrador`, `Empleado`, `Cliente`).
- `productos.json`: Catálogo de platillos, precios y existencias en inventario.
- `ventas.json`: Registro histórico de todas las órdenes efectuadas en el restaurante.

---

## Credenciales de Acceso para Pruebas

Para validar el control de acceso y las restricciones por rol, se disponen las siguientes cuentas:

| Usuario | Contraseña | Nombre Completo | Rol Asignado | Acceso a Gestión de Usuarios |
| :--- | :--- | :--- | :--- | :--- |
| `admin` | `admin123` | Administrador General | **Administrador** | **Permitido** (Acceso completo) |
| `empleado` | `1234` | Empleado de Turno | **Empleado** | **Denegado** (Botón bloqueado) |
| `carlos` | `carlos456` | Carlos Gómez | **Cliente** | **Denegado** (Botón bloqueado) |
| `erick` | `erick2026` | Erick Yamberla | **Cliente** | **Denegado** (Botón bloqueado) |
| `maria` | `maria789` | María López | **Cliente** | **Denegado** (Botón bloqueado) |
| `juan` | `juan321` | Juan Pérez | **Empleado** | **Denegado** (Botón bloqueado) |
| `ana` | `ana654` | Ana Torres | **Cliente** | **Denegado** (Botón bloqueado) |

---

## Instrucciones para Ejecutar la Aplicación

1. **Requisitos:**
   - Python 3.10 o superior (con soporte estándar de Tkinter).

2. **Ejecución desde la raíz del proyecto:**
   ```bash
   python PARCIAL_2/SEMANA_16/restaurante_app/main.py
   ```

3. **Ejecución desde la carpeta de la Semana 16:**
   ```bash
   cd PARCIAL_2/SEMANA_16
   python restaurante_app/main.py
   ```

---

## Comprobación Mínima de Funcionamiento

Para comprobar el cumplimiento de los requerimientos de la Semana 16, siga esta guía de verificación:

1. **Inicio de sesión como Administrador:**
   - Inicie sesión con `admin` y `admin123`.
   - Observe en la barra superior el indicador: `👤 admin (Administrador General) | Rol: Administrador`.
   - Compruebe que el botón **"Usuarios"** se encuentra habilitado.
2. **Navegación a Usuarios:**
   - Haga clic en **"Usuarios"**. Verifique que el Treeview liste los 7 usuarios con Identificador, Nombre, Usuario, Rol y Correo.
3. **Comprobación de `<<TreeviewSelect>>`:**
   - Haga clic sobre cualquier usuario en la tabla. Verifique que sus datos se carguen instantáneamente en el formulario sin exponer contraseñas en la tabla.
4. **Comprobación de `<<ComboboxSelected>>`:**
   - En el formulario, cambie el rol en el Combobox entre `Cliente`, `Empleado` y `Administrador`. Observe cómo la etiqueta explicativa y la barra de estado inferior describen las atribuciones de dicho rol.
5. **Comprobación de atajo `<Escape>`:**
   - Presione la tecla **Esc** estando en cualquier campo del formulario o sobre la tabla. Verifique que el formulario se limpie y la fila deje de estar seleccionada.
6. **Comprobación de atajo `<Return>` (Registro):**
   - Ingrese los datos de un nuevo usuario (ej. usuario: `sofia`, contraseña: `123`, nombre: `Sofía Castro`, rol: `Cliente`).
   - Estando en cualquiera de los campos de texto, presione **Enter**. Compruebe que el usuario se registre exitosamente y aparezca en la tabla Treeview.
7. **Comprobación de Actualizar:**
   - Seleccione el usuario recién registrado en la tabla, modifique su nombre o rol y presione el botón **"Actualizar Usuario"**. Verifique que los cambios se reflejen en la tabla.
8. **Comprobación de Eliminar y Protección de Administrador Activo:**
   - Seleccione al usuario `admin` en la tabla e intente eliminarlo con el botón **"Eliminar Usuario"**. Verifique que el sistema bloquee la operación indicando que no es posible eliminar la cuenta en sesión activa.
   - Seleccione el usuario de prueba creado (`sofia`), presione **"Eliminar Usuario"**, confirme el cuadro de diálogo modal y compruebe su eliminación de la tabla.
9. **Comprobación de Restricción para no Administradores:**
   - Cierre sesión mediante el botón **"Cerrar sesión"**.
   - Inicie sesión con el usuario `empleado` (`1234`) o `carlos` (`carlos456`).
   - Observe que en la barra superior el botón **"Usuarios"** se encuentra deshabilitado, impidiendo el acceso a la administración de usuarios.
   - Verifique que las secciones **Inicio**, **Ventas** y **Productos** continúan operando con total normalidad.
10. **Comprobación de Persistencia:**
    - Cierre la aplicación por completo y vuelva a ejecutarla para verificar que las modificaciones persisten en `usuarios.json`.
