# Restaurante App - Semana 13

Estudiante: Erick Yamberla

Este repositorio corresponde a una base gráfica del proyecto restaurante_app desarrollada durante la Semana 13. La finalidad de esta entrega es aprender a integrar Programación Orientada a Objetos (POO) con interfaces gráficas usando Tkinter, manteniendo una estructura modular y clara, en lugar de concentrar toda la lógica en un solo archivo.

## Credenciales de prueba

Para recordar fácilmente el acceso de prueba de la aplicación, se pueden usar estas credenciales:

- Usuario: admin
- Contraseña: admin123

También existe un segundo usuario de ejemplo:

- Usuario: carlos
- Contraseña: carlos456

Estas credenciales se cargan desde el archivo JSON de usuarios dentro de la carpeta datos/.

## ¿Qué estamos aprendiendo aquí?

Este proyecto está pensado como un ejercicio didáctico para comprender cómo se organizan las aplicaciones más profesionales:

- Los modelos representan las entidades del dominio del problema.
- Los servicios contienen la lógica de negocio y el acceso a datos.
- La interfaz gráfica se separa en vistas, para no mezclar UI con reglas del sistema.
- El punto de entrada main.py conecta todo y controla el flujo de la aplicación.

Con esto, se aplica una estructura que facilita el mantenimiento del código y hace más sencillo ampliar la aplicación con nuevas funcionalidades en futuras semanas.

## Propósito del proyecto

Esta nueva base del proyecto restaurante_app tiene como objetivo adaptar la estructura del ejemplo docente para trabajar con el dominio del restaurante, utilizando modelos, servicios, archivos JSON y una interfaz gráfica con Tkinter.

La aplicación inicia con una pantalla de acceso simulada. Cuando el usuario ingresa credenciales válidas, se abre la vista principal del restaurante. Desde allí se puede consultar la información base de productos y usuarios cargados desde archivos JSON, sin que la interfaz lea directamente los archivos ni tenga lógica de validación mezclada con la UI.

La versión de esta semana es una base gráfica inicial. No se intenta mover toda la lógica de consola anterior en una sola entrega; primero se consolida la organización correcta y la estructura del proyecto, y luego se irán incorporando más funciones del restaurante conforme avance la unidad.

## Estructura de carpetas y archivos

La estructura del proyecto se organiza en capas, siguiendo el mismo criterio del proyecto docente:

restaurante_app/
├── datos/
│   ├── productos.json
│   └── usuarios.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md

### Descripción de cada carpeta

- datos/: guarda la información base del sistema en archivos JSON.
- modelos/: define las entidades del dominio: Producto y Usuario.
- servicios/: encapsula la carga de datos y las reglas de validación del acceso y consulta.
- ui/: contiene las vistas gráficas de la aplicación, como el login y el panel principal.
- main.py: es el punto de entrada que prepara la ventana, crea los servicios y controla el cambio entre pantallas.

## Flujo de la aplicación

El flujo mínimo de la aplicación es el siguiente:

1. Se ejecuta main.py.
2. Se prepara la ventana principal de Tkinter.
3. Se crea una instancia de RestauranteServicio para cargar los datos de JSON.
4. Se muestra la vista de LoginView.
5. El usuario ingresa usuario y contraseña.
6. El servicio valida la información.
7. Si las credenciales son correctas, se cambia a MainView.
8. La vista principal permite consultar productos y usuarios registrados.
9. Si el usuario cierra sesión, vuelve al login sin cerrar la ventana principal.

## Vistas implementadas

### LoginView

La vista de inicio sirve como acceso simulado al sistema. Incluye:

- campo para usuario
- campo para contraseña
- botón de ingreso
- mensajes de validación para campos vacíos o credenciales incorrectas

### MainView

La vista principal muestra el panel del restaurante y permite:

- consultar productos registrados
- consultar usuarios registrados
- indicar opciones futuras como Ventas como funcionalidad pendiente
- cerrar sesión y regresar a la pantalla de acceso

## Pasos para ejecutar main.py

Para correr la aplicación desde la raíz del proyecto, se puede ejecutar:

python PARCIAL_2/SEMANA_13/restaurante_app/main.py

O bien, si te encuentras dentro de la carpeta SEMANA_13:

python restaurante_app/main.py

El archivo principal crea la única ventana de Tkinter, prepara los servicios y controla la navegación entre login y panel principal.

## Objetivo de aprendizaje de esta semana

Esta actividad busca comprender la estructura modular del ejemplo docente y adaptarla al dominio del restaurante. La intención es aprender a trabajar con:

- clases y objetos de POO
- capas de modelo, servicio y vista
- persistencia local mediante JSON
- interfaces gráficas con Tkinter
- una ventana principal y flujo de navegación dentro de la misma aplicación

## Nota final

Este README cumple con la descripción requerida para la Semana 13: presenta el propósito de la nueva base, explica la estructura de carpetas y archivos, describe el flujo de la aplicación, detalla las vistas implementadas y muestra los pasos necesarios para ejecutar main.py.

## Conceptos didácticos de apoyo

### 1. Programación Orientada a Objetos (POO)

La POO ayuda a modelar problemas reales con clases y objetos. En este proyecto:

- Producto representa cada artículo del restaurante.
- Usuario representa a una persona que puede acceder al sistema.
- Cada clase encapsula sus atributos y comportamiento.

Esto permite que el código sea más ordenado, reutilizable y comprensible. En vez de trabajar con listas sueltas o datos dispersos, cada entidad tiene sentido y responsabilidades definidas.

### 2. Separación de responsabilidades

La organización del código se basa en una idea muy importante:

- modelos/: define qué cosas existen en el sistema.
- servicios/: define qué acciones puede hacer el sistema.
- ui/: define cómo se presenta la información al usuario.
- main.py: hace de conector y arranca la aplicación.

Esta separación es clave para aprender a programar de forma más profesional. Si todo está mezclado, el proyecto crece difícil de mantener.

### 3. Interfaces gráficas con Tkinter

Tkinter es la biblioteca estándar de Python para crear interfaces gráficas. Permite construir ventanas, botones, entradas, etiquetas y otros componentes de forma bastante sencilla.

En este proyecto se usa:

- tk.Tk() para crear la ventana principal.
- ttk.Entry para campos de texto.
- ttk.Button para acciones.
- tk.Label para mensajes e información.
- tk.Text para visualizar contenido en la vista principal.

En Tkinter, la aplicación trabaja con un ciclo de eventos. Eso significa que la interfaz queda esperando a que el usuario interactúe con botones, entradas o ventanas. Cuando sucede una acción, se ejecuta el código asociado a ese evento.

## Estructura esperada del repositorio

Repositorio GitHub
├── restaurante_app/
│   ├── datos/
│   │   ├── productos.json
│   │   └── usuarios.json
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── producto.py
│   │   └── usuario.py
│   ├── servicios/
│   │   ├── __init__.py
│   │   ├── archivo_servicio.py
│   │   └── restaurante_servicio.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── login_view.py
│   │   └── main_view.py
│   └── main.py
└── README.md

## Organización de la aplicación

- modelos/: representa las entidades del sistema, como Producto y Usuario.
- servicios/: concentra la carga y persistencia de datos desde archivos JSON y la lógica de validación del restaurante.
- ui/: contiene las pantallas de ingreso y panel principal con Tkinter.
- main.py: prepara la ventana principal, crea las dependencias y controla el cambio entre vistas.
- datos/: almacena la información local de productos y usuarios.

## Flujo de la aplicación

1. Se inicia la aplicación desde main.py.
2. La pantalla de login se muestra primero.
3. El usuario ingresa usuario y contraseña.
4. RestauranteServicio valida las credenciales.
5. Si son correctas, se abre la interfaz principal.
6. Desde la vista principal se pueden consultar productos y usuarios.
7. La opción de cerrar sesión regresa al login sin cerrar la ventana principal.

## Vistas implementadas

- LoginView: formulario de acceso con usuario, contraseña, mensaje de error y botón para ingresar.
- MainView: panel principal con opciones para consultar productos, ver usuarios, mostrar ventas pendientes y cerrar sesión.

## Datos iniciales

Los archivos JSON dentro de la carpeta datos/ contienen información base para simular el funcionamiento del sistema. La vista principal consulta esa información mediante el servicio del restaurante; no se recomienda acceder directamente al archivo desde la interfaz gráfica ni mezclar la lectura de datos con la capa visual.

## Cómo ejecutar la aplicación

Desde la raíz del proyecto, ejecute:

python PARCIAL_2/SEMANA_13/restaurante_app/main.py

O bien, ubicándose dentro de la carpeta SEMANA_13 y ejecutando:

python restaurante_app/main.py

## Aprendizaje recomendado para seguir avanzando

Si estás aprendiendo a programar con POO e interfaces gráficas, te recomiendo seguir estos pasos:

- Practicar la creación de clases pequeñas y concretas.
- Separar modelo, lógica y vista en cada proyecto nuevo.
- Intentar nombrar bien las clases y métodos para que el código se entienda solo.
- Probar primero la lógica del negocio sin interfaz gráfica.
- Luego conectar esa lógica con Tkinter con ventanas simples.
- Repetir el proceso con pequeñas mejoras: validaciones, mensajes, botones, listas y paneles.

## Nota importante

Esta versión corresponde a la base gráfica de la Semana 13. Se mantiene una estructura clara y modular, y la aplicación queda preparada para ser ampliada con más funcionalidades del restaurante en las siguientes etapas de la unidad. La idea es aprender a construir proyectos ordenados, pensados con clases y con una interfaz visual que responde a eventos reales del usuario.

## Cierre personal

Este proyecto representa una primera experiencia concreta al combinar POO y GUI con Tkinter. Es una base sólida para seguir aprendiendo, entendiendo que cada componente del sistema tiene un propósito y que la práctica constante ayuda a desarrollar mejores habilidades como programador.
