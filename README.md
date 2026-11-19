# ProyectoFinal-385795-385770-385574

# Sistema de Administración de Blog con Neo4j

## 1. Descripción del proyecto

Este proyecto consiste en una aplicación de escritorio desarrollada en Python que permite administrar el contenido de un blog mediante una base de datos orientada a grafos en Neo4j.

La aplicación cuenta con una interfaz gráfica desarrollada con Tkinter y permite gestionar usuarios, artículos, comentarios, etiquetas y categorías.

El sistema implementa autenticación de usuarios y permisos de acuerdo con el rol y la autoría del contenido.

## 2. Tecnologías utilizadas

- **Python:** lenguaje de programación principal.
- **Tkinter:** desarrollo de la interfaz gráfica.
- **Neo4j AuraDB:** almacenamiento y administración de los datos.
- **Cypher:** lenguaje de consultas para Neo4j.
- **Neo4j Python Driver:** conexión entre Python y Neo4j.
- **python-dotenv:** lectura de variables de configuración desde el archivo `.env`.

## 3. Estructura del proyecto

```text
ProyectoFinal-385795-385770-385574/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── auth.py
│   └── blog.py
│
├── cypher/
│   └── blog.cypher
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Descripción de los archivos

- `main.py`: contiene la interfaz gráfica y las opciones de interacción.
- `database.py`: administra la conexión con Neo4j.
- `auth.py`: contiene las funciones de registro, inicio de sesión y creación de administradores.
- `blog.py`: implementa las operaciones de artículos, comentarios, etiquetas y categorías.
- `blog.cypher`: contiene las restricciones de unicidad necesarias para la base de datos.
- `requirements.txt`: lista las dependencias de Python.
- `.env.example`: plantilla para configurar las credenciales y datos del administrador.
- `.gitignore`: evita subir archivos privados y temporales al repositorio.

## 4. Requisitos previos

Antes de ejecutar el proyecto se necesita:

1. Python 3.10 o superior.
2. Una instancia de Neo4j AuraDB.
3. Conexión a Internet.
4. Las dependencias de Python especificadas en `requirements.txt`.

En Windows se puede comprobar la instalación de Python con:

```bash
py --version
```

## 5. Configuración de Neo4j AuraDB

### 5.1 Crear una instancia

1. Ingresar a [Neo4j Aura](https://console.neo4j.io/).
2. Crear una cuenta o iniciar sesión.
3. Crear una instancia de Neo4j AuraDB.
4. Guardar las credenciales de acceso generadas.
5. Obtener la dirección de conexión de la instancia.

Se necesitarán los siguientes datos:

- URI de conexión, normalmente con formato `neo4j+s://...`.
- Usuario de la base de datos.
- Contraseña de la base de datos.

### 5.2 Crear las restricciones

Una vez creada la instancia:

1. Abrir Neo4j Aura.
2. Ingresar a la herramienta Query.
3. Abrir el archivo `cypher/blog.cypher` del proyecto.
4. Copiar y ejecutar las consultas en Neo4j.

Estas consultas crean restricciones de unicidad para evitar registros duplicados en:

- Correo electrónico de usuarios.
- Identificadores de artículos.
- Identificadores de comentarios.
- Nombres de etiquetas.
- Nombres de categorías.

Para verificar que se hayan creado correctamente, ejecutar:

```cypher
SHOW CONSTRAINTS;
```

Deben aparecer las cinco restricciones del proyecto.

## 6. Instalación del proyecto

### 6.1 Descargar el repositorio

Se puede descargar el proyecto desde GitHub:

[Repositorio del proyecto](https://github.com/joseMartinez2006/ProyectoFinal-385795-385770-385574)

En GitHub, seleccionar **Code → Download ZIP** y extraer el contenido en una carpeta del equipo.

También se puede clonar el repositorio:

```bash
git clone https://github.com/joseMartinez2006/ProyectoFinal-385795-385770-385574.git
```

### 6.2 Instalar las dependencias

Abrir una terminal en la carpeta principal del proyecto y ejecutar:

```bash
py -m pip install -r requirements.txt
```

Este comando instala las bibliotecas necesarias para la conexión con Neo4j y la configuración del proyecto.

## 7. Configuración del archivo .env

Por seguridad, el archivo `.env` no se encuentra incluido en el repositorio. Cada usuario debe crearlo.

1. Buscar el archivo `.env.example` en la carpeta principal.
2. Crear una copia.
3. Cambiar el nombre de la copia a `.env`.
4. Abrir el archivo y completar los datos correspondientes.

El contenido debe tener el siguiente formato:

```env
NEO4J_URI=neo4j+s://DIRECCION_DE_TU_INSTANCIA
NEO4J_USER=neo4j
NEO4J_PASSWORD=CONTRASEÑA_DE_NEO4J

ADMIN_NAME=Administrador
ADMIN_EMAIL=admin@blog.com
ADMIN_PASSWORD=CONTRASEÑA_DEL_ADMINISTRADOR
```

Reemplazar los valores de ejemplo por los datos propios.

**Importante:** existen dos contraseñas diferentes:

- `NEO4J_PASSWORD`: contraseña para conectarse a la base de datos.
- `ADMIN_PASSWORD`: contraseña que tendrá el administrador de la aplicación.

No compartir el archivo `.env` ni subirlo a GitHub.

## 8. Crear el usuario administrador

Antes de iniciar la aplicación por primera vez, se debe crear un administrador.

La función `create_admin()` se encuentra en `app/auth.py` y recibe el nombre, correo electrónico y contraseña del administrador.

Desde la carpeta principal del proyecto, ejecutar:

```bash
py -c "import sys; sys.path.insert(0, 'app'); from auth import create_admin; from dotenv import dotenv_values; c=dotenv_values('.env'); print(create_admin(c['ADMIN_NAME'], c['ADMIN_EMAIL'], c['ADMIN_PASSWORD']))"
```

La función utiliza los datos del archivo `.env` y registra al administrador en Neo4j.

Si la operación se realiza correctamente, se obtiene el resultado `True`.

**Nota:** este procedimiento debe realizarse al configurar una base de datos nueva. Si ya existe un usuario con ese correo electrónico, la función no actualiza automáticamente su contraseña ni su rol. Para una configuración inicial limpia, utilizar una cuenta de administrador que todavía no exista en la base de datos.

## 9. Ejecutar la aplicación

Una vez configurada la base de datos, instaladas las dependencias y creado el administrador, ejecutar desde la carpeta principal:

```bash
py app\main.py
```

Se abrirá la ventana de inicio de sesión.

Ingresar con el correo electrónico y la contraseña establecidos para el administrador.

## 10. Funcionalidades del sistema

### 10.1 Usuarios

- Registro de nuevos usuarios.
- Inicio de sesión.
- Validación de credenciales.
- Identificación del rol del usuario.

### 10.2 Artículos

- Consultar artículos.
- Crear artículos.
- Modificar artículos.
- Eliminar artículos.

### 10.3 Comentarios

- Consultar comentarios asociados a un artículo.
- Agregar comentarios.
- Modificar comentarios propios.
- Eliminar comentarios propios.

### 10.4 Etiquetas y categorías

- Crear etiquetas.
- Consultar etiquetas.
- Modificar etiquetas.
- Eliminar etiquetas.
- Crear y administrar categorías.

## 11. Roles y permisos

El sistema contempla dos roles principales:

### Administrador

- Puede consultar, crear, modificar y eliminar artículos.
- Puede administrar todos los comentarios.
- Puede crear, modificar y eliminar etiquetas y categorías.
- Puede consultar el contenido registrado.

### Usuario

- Puede consultar artículos.
- Puede crear artículos.
- Puede modificar y eliminar sus propios artículos.
- Puede crear comentarios.
- Puede modificar y eliminar sus propios comentarios.
- Puede crear etiquetas y categorías.

Las operaciones de modificación y eliminación validan la autoría del contenido o el rol del usuario.

## 12. Modelo de datos

La base de datos utiliza nodos y relaciones para representar la información del blog.

Entre los principales nodos se encuentran:

- `User`: usuarios del sistema.
- `Article`: artículos publicados.
- `Comment`: comentarios.
- `Tag`: etiquetas.
- `Category`: categorías.

Las relaciones permiten asociar usuarios con sus artículos y comentarios, así como relacionar artículos con comentarios, etiquetas y categorías.

Algunos ejemplos de relaciones son:

- `WROTE`: identifica quién escribió un artículo o comentario.
- `HAS_COMMENT`: relaciona un artículo con sus comentarios.
- `HAS_TAG`: relaciona un artículo con sus etiquetas.
- `HAS_CATEGORY`: relaciona un artículo con sus categorías.

## 13. Solución de problemas

### Error de conexión con Neo4j

Verificar que:

- La instancia de AuraDB esté disponible.
- El URI sea correcto.
- El usuario y la contraseña de Neo4j sean válidos.
- El equipo tenga conexión a Internet.

### Error al importar módulos

Comprobar que la terminal esté ubicada en la carpeta principal del proyecto y que las dependencias estén instaladas.

### Error al iniciar sesión

Verificar que el administrador haya sido creado correctamente y que se estén utilizando el correo y la contraseña correspondientes.

### No aparecen las restricciones

Ejecutar nuevamente las consultas del archivo `cypher/blog.cypher` y comprobar el resultado con:

```cypher
SHOW CONSTRAINTS;
```

## 14. Seguridad

- Las credenciales de Neo4j se almacenan en `.env`.
- El archivo `.env` está excluido del control de versiones mediante `.gitignore`.
- Las contraseñas de los usuarios se almacenan mediante hash SHA-256.
- Las operaciones de modificación y eliminación verifican los permisos del usuario.
- Cada instalación debe utilizar sus propias credenciales de conexión y administrador.

## 15. Integrantes

Jose Fernando Martinez Pacheco - 385795
Carlos Gonzalez Carrera - 385574
Elio Castillo Reyes - 385770