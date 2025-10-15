# 📚 BookManager API

**BookManager** es una aplicación RESTful desarrollada con **Django + Django REST Framework** que permite gestionar una biblioteca digital.  
Permite crear, listar, actualizar y eliminar libros, con autenticación basada en JWT y documentación interactiva vía Swagger.

---

## 🚀 Características principales

- CRUD completo de libros.
- Autenticación JWT (login y obtención de token).
- Documentación interactiva Swagger UI.
- Integración con **MongoDB Atlas** como base de datos principal.
- Desplegado en **Google Cloud Run** (capa gratuita).
- Configuración lista para Docker y despliegue continuo.
- Docker compose para ambiente de desarrollo

---

## 🧱 Tecnologías utilizadas

| Componente           | Tecnología                           |
| -------------------- | ------------------------------------ |
| Lenguaje             | Python 3.12                          |
| Framework backend    | Django 5 + Django REST Framework     |
| Autenticación        | SimpleJWT                            |
| Documentación API    | drf-spectacular                      |
| Base de datos        | MongoDB (MongoDB Atlas)              |
| Infraestructura      | Google Cloud Run + Artifact Registry |
| Contenedor           | Docker                               |
| Servidor WSGI        | Gunicorn                             |
| Control de versiones | Git + GitHub                         |

---

## 🧩 Estructura del proyecto

Se organizo el proyecto usando arquitectura hexagonal de la siguiente manera:

```bash
library-system/
├── books/                     # App principal con modelos, vistas y rutas
│   ├── migrations/
│   ├── application/            # Capa de aplicación
│   ├── domain/                 # Capa de dominio
│   ├── infrastructure/         # Capa de infraestructura
│   ├── interfaces/             # Entrypoints (controladores, vistas, etc.)
│   ├── apps.py
│   ├── admin.py
│   └── tests.py
├── bookmanager/                # Configuración principal de Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py

```

## 🔗 Endpoints principales

URL_BASE: [http://localhost:8080](http://localhost:8080)

### 🔒 Autenticación

| Método | Endpoint      | Descripción                             |
| ------ | ------------- | --------------------------------------- |
| `POST` | `/api/login/` | Obtiene el token JWT (access y refresh) |

---

### 📚 Libros

| Método   | Endpoint                               | Descripción                                                                |
| -------- | -------------------------------------- | -------------------------------------------------------------------------- |
| `GET`    | `/api/books/`                          | Lista todos los libros (paginado)                                          |
| `POST`   | `/api/books/`                          | Crea un nuevo libro                                                        |
| `GET`    | `/api/books/{id}/`                     | Obtiene detalles de un libro                                               |
| `PATCH`  | `/api/books/{id}/`                     | Actualiza un libro existente                                               |
| `DELETE` | `/api/books/{id}/`                     | Elimina un libro                                                           |
| `GET`    | `/api/books/average-price?year={year}` | Calcula el **precio promedio** de los libros publicados en el año indicado |

---

### 🧾 Documentación

| Tipo         | Endpoint                  |
| ------------ | ------------------------- |
| Swagger UI   | `/api/schema/swagger-ui/` |
| Redoc        | `/api/schema/redoc/`      |
| OpenAPI JSON | `/api/schema/`            |

Swagger URL [http://localhost:8080/api/docs](http://localhost:8080/api/docs)

## ⚙️ Variables de entorno

| Variable        | Descripción                          | Ejemplo                                                   |
| --------------- | ------------------------------------ | --------------------------------------------------------- |
| `MONGO_URI`     | URI de conexión a MongoDB            | `mongodb+srv://user:pass@cluster.mongodb.net/bookmanager` |
| `MONGO_DB_NAME` | Nombre de la base de datos           | `bookmanager`                                             |
| `SECRET_KEY`    | Llave secreta Django                 | `clave-secreta`                                           |
| `DEBUG`         | Activa modo debug                    | `True` / `False`                                          |
| `PORT`          | Puerto en el que corre el contenedor | `8080`                                                    |

---

## 🐳 Despliegue local con Docker

```bash
# 1. Construir la imagen
docker-compose up -d

# 2. Ejecutar pruebas unitarias (Opcional)
docker-compose exec web python manage.py test

# 3. Colecciones y environments de postman disponibles en el folder apicollections
```
