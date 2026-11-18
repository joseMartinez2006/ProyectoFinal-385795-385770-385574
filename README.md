# ProyectoFinal-385795-385770-385574

# Blog Manager

Aplicación de escritorio desarrollada en Python que permite administrar un blog mediante una base de datos orientada a grafos Neo4j.

## Tecnologías utilizadas

- Python
- Tkinter
- Neo4j
- Cypher
- Neo4j Python Driver
- python-dotenv

## Estructura del proyecto

```text
ProyectoFinal/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── auth.py
│   └── blog.py
├── cypher/
│   └── blog.cypher
├── screenshots/
├── requirements.txt
├── .env.example
├── .env
├── .gitignore
└── README.md
```

## Requisitos previos

- Python 3 instalado.
- Una instancia de Neo4j disponible.
- Conexión a Internet para conectarse a Neo4j AuraDB.

## Instalación

1. Descargar o clonar este repositorio.
2. Abrir una terminal en la carpeta principal del proyecto.
3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración de la base de datos

1. Crear una instancia de Neo4j AuraDB o utilizar una instancia compatible.
2. Copiar el archivo `.env.example` y crear un archivo llamado `.env` en la raíz del proyecto.
3. Configurar las credenciales de conexión:

```env
NEO4J_URI=
NEO4J_USER=neo4j
NEO4J_PASSWORD=

ADMIN_NAME=Administrador
ADMIN_EMAIL=admin@blog.com
ADMIN_PASSWORD=
```

4. Completar los valores con los datos correspondientes a la instancia de Neo4j y la cuenta de administrador.

**Importante:** El archivo `.env` contiene información privada y no debe compartirse ni subirse al repositorio.

## Configuración inicial de Neo4j

Ejecutar el contenido del archivo `cypher/blog.cypher` en Neo4j Browser para crear las restricciones necesarias en la base de datos.

## Ejecución

Desde la carpeta principal del proyecto, ejecutar:

```bash
python app/main.py
```

La aplicación abrirá una ventana de escritorio desde la cual se podrá iniciar sesión o registrar un usuario.

## Funcionalidades

- Registro e inicio de sesión de usuarios.
- Administración de artículos.
- Creación, consulta, modificación y eliminación de comentarios.
- Administración de etiquetas.
- Administración de categorías.
- Control de permisos según el tipo de usuario.

## Roles de usuario

**Administrador**
- Puede administrar artículos y comentarios.
- Puede modificar y eliminar etiquetas y categorías.
- Tiene permisos de administración.

**Usuario**
- Puede consultar artículos.
- Puede crear artículos y comentarios.
- Puede modificar o eliminar sus propios artículos y comentarios.
- Puede crear etiquetas y categorías.