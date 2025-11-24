# Mi Billetera - Sistema de Gestión Financiera
**Mi Billetera** es una aplicación de escritorio desarrollada en Python diseñada para gestionar tus finanzas personales de manera simple. Este proyecto permite registrar ingresos y gastos, visualizar el saldo en tiempo real y consultar la cotización del Dólar Blue mediante una API externa.

## Requisitos del Sistema
Para ejecutar este sistema correctamente, necesitas tener instalado lo siguiente:

### Software Base
* **Python 3.10 o superior**
* **MySQL Server**: Necesario para la base de datos (puedes usar XAMPP, WAMP o MySQL Workbench).

### Librerías de Python
El proyecto utiliza librerías externas para la interfaz gráfica, la conexión a datos y consulta de contización del dólar. Se pueden instalar ejecutando el siguiente comando en la terminal:
pip install customtkinter pymysql requests

* **customtkinter**: Para la interfaz gráfica moderna.
* **pymysql**: Para la conexión con la base de datos MySQL.
* **requests**: Para consultar la API del Dólar Blue.

## Configuración de la Base de Datos

Antes de iniciar la aplicación, asegúrate de crear en tu gestor de base de datos (que puede ser Workbench) una base de datos nueva llamada "finanzas". El programa creará automáticamente la tabla de transacciones al inciarse.

### Credenciales por defecto
El sistema está configurado para usar:
* **Host:** 127.0.0.1
* **Usuario:** root
* **Contraseña:** root

**Importante:** Si tu configuración de MySQL tiene una contraseña diferente o un puerto distinto al 3306, debes editar las variables al inicio del archivo "billetera_main.py".

## Instrucciones de Ejecución
Una vez instalados los requisitos y configurada la base de datos:
1. Descarga o clona este repositorio.
2. Abre la terminal en la carpeta del proyecto.
3. Ejecuta el archivo principal llamado "billetera_main.py" para correr el programa.

## Funcionalidades Principales

### Dashboard Interactivo
* **Saldo Total:** Visualización inmediata del dinero disponible en cuenta.
* **Resumen de Movimientos:** Tarjetas visuales separadas que muestran el total acumulado de **Ingresos** (Color Verde) y **Gastos** (Color Rojo).
* **Cotización Dólar Blue:** Consulta en tiempo real los valores de **Compra** y **Venta** a través de una API externa (`dolarapi.com`), con un botón de actualización manual (↻).

### Gestión de Transacciones (CRUD)
* **Nuevo Registro:** Botón verde "+ Nuevo Registro" que abre un formulario emergente (Modal) para cargar operaciones.
    * **Campos:** Tipo (Ingreso/Gasto), Monto, Fecha (autocompletada), Categoría y Descripción.
* **Listado Visual:** Tabla moderna centralizada que muestra todas las operaciones ordenadas por fecha, con colores distintivos para ingresos y gastos.
* **Edición y Eliminado:** Al hacer clic izquierdo sobre una fila de la tabla, se despliega un menú contextual que permite:
    * **Editar:** Modificar los datos de una transacción existente.
    * **Eliminar:** Borrar el registro de la base de datos permanentemente.

### Respaldo Automático (Backup)
* El sistema genera y actualiza automáticamente un archivo **"Transacciones.txt"** en la carpeta del proyecto cada vez que se realiza un cambio (ingreso, eliminación o modificación), sirviendo como copia de seguridad local de tu base de datos.

## Estructura del Proyecto
A continuación se detalla la función de cada módulo del sistema:
* **"billetera_main.py"**: Punto de entrada de la aplicación. Configura la conexión a la base de datos e inicia la interfaz gráfica.
* **"billetera_gui.py"**: Contiene toda la lógica de la Interfaz Gráfica de Usuario (GUI). Define las ventanas, estilos, tablas, botones y la interacción con el usuario usando "customtkinter".
* **"clase_billetera.py"**: Actúa como controlador principal. Conecta la interfaz gráfica con la base de datos y gestiona la lógica (validaciones, llamadas a backup).
* **"billetera_db.py"**: Capa de acceso a datos. Maneja las consultas SQL directas (Insertar, Borrar, Actualizar, Leer) utilizando "pymysql".
* **"movimientos.py"**: Módulo auxiliar encargado de generar y escribir el respaldo en el archivo de texto "Transacciones.txt".

## Autor
**Matías Juárez** - *Academia de Desarrollo 2025*
