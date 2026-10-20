# Gestión de datos de los aprendices

API REST sencilla construida con **FastAPI** y **MongoDB** para registrar, consultar, actualizar y eliminar aprendices. Incluye una interfaz de consola (CLI) para consumirla y está desplegada en **Render**.

- **API en producción:** https://t1-fastapi.onrender.com
- **Documentación interactiva (Swagger):** https://t1-fastapi.onrender.com/docs
- **Repositorio:** https://github.com/johndaviddiax-ai/t1_fastapi

> La API está en el plan gratuito de Render: si lleva un rato sin uso, la primera petición puede tardar entre 30 y 60 segundos en responder.

---

## Tecnologías utilizadas

| Herramienta | Para qué se usa |
|---|---|
| Python 3 | Lenguaje principal |
| FastAPI | Framework para construir la API |
| Uvicorn | Servidor ASGI que ejecuta la aplicación |
| Pydantic | Modelos y validación de datos |
| email-validator | Validación del formato del correo electrónico |
| PyMongo | Conexión con la base de datos |
| MongoDB | Base de datos NoSQL donde se guardan los aprendices |
| Requests | Consumo de la API desde la interfaz de consola |
| Pytest / HTTPX | Pruebas de la API (carpeta `test`) |
| Git y GitHub | Control de versiones y repositorio |
| Render | Despliegue de la API en la nube |
| Visual Studio Code | Editor de código |

---

## Estructura del proyecto

```
t1_api/
├── data/                  # Datos del proyecto
├── src/
│   ├── models/
│   │   ├── database.py    # Conexión con MongoDB
│   │   └── model.py       # Modelos Pydantic (TraineeModel, TraineeUpdateModel)
│   ├── templates/
│   │   └── controllers.py # Lógica de negocio: operaciones CRUD sobre la base de datos
│   ├── views/
│   │   └── views.py       # Interfaz de consola (CLI) para consumir la API
│   └── main.py            # Aplicación FastAPI y definición de las rutas
├── test/
│   └── test_main.py       # Pruebas de la API
├── venv/                  # Entorno virtual (no se sube a GitHub)
├── .env                   # Variables de entorno (no se sube a GitHub)
├── .gitignore             # Archivos y carpetas que Git ignora
├── README.md              # Este archivo
├── requirements.txt       # Dependencias del proyecto
└── structure.sh           # Script para generar la estructura de carpetas
```

### Cómo se organiza el código

- **`models/`**: define cómo son los datos (`model.py`) y cómo se conecta a la base de datos (`database.py`).
- **`templates/controllers.py`**: contiene las funciones que crean, leen, actualizan y eliminan aprendices en MongoDB.
- **`main.py`**: recibe las peticiones HTTP, llama a los controladores y devuelve la respuesta.
- **`views/views.py`**: menú en consola que hace las peticiones a la API.

---

## Modelo de datos

Cada aprendiz tiene los siguientes campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `document` | texto | Documento de identidad (único) |
| `firstname` | texto | Nombres |
| `lastname` | texto | Apellidos |
| `email` | correo | Correo electrónico (se valida el formato) |
| `age` | entero | Edad |
| `program` | texto | Programa de formación |
| `record_number` | texto | Número de ficha |

Ejemplo:

```json
{
  "document": "1234567890",
  "firstname": "Juan",
  "lastname": "Pérez",
  "email": "juan@gmail.com",
  "age": 20,
  "program": "Análisis y desarrollo de software",
  "record_number": "2900000"
}
```

---

## Endpoints

| Método | Ruta | Descripción | Respuesta |
|---|---|---|---|
| GET | `/` | Mensaje de bienvenida | 200 |
| POST | `/trainee/` | Registrar un nuevo aprendiz | 201 |
| GET | `/trainee/` | Listar todos los aprendices | 200 |
| GET | `/trainee/{id}` | Obtener un aprendiz por su id | 200 / 404 |
| PUT | `/trainee/{id}` | Actualizar los datos de un aprendiz | 200 / 404 |
| DELETE | `/trainee/{id}` | Eliminar un aprendiz | 200 / 404 |

Códigos de error frecuentes:

- **400**: ya existe un aprendiz con ese documento.
- **404**: aprendiz no encontrado.
- **422**: datos inválidos (por ejemplo, un correo mal escrito).

---

## Instalación y ejecución local

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/johndaviddiax-ai/t1_fastapi.git
   cd t1_fastapi
   ```

2. **Crear y activar el entorno virtual**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux / Mac
   source venv/bin/activate
   ```

3. **Instalar las dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Crear el archivo `.env`** en la raíz del proyecto con las variables de entorno que usa `database.py` (por ejemplo, la cadena de conexión a MongoDB):

   ```env
   MONGO_URI=tu_cadena_de_conexion
   ```

   > Ajusta el nombre de la variable al que use tu código.

5. **Iniciar el servidor**

   ```bash
   uvicorn src.main:app --reload
   ```

   La API queda disponible en http://127.0.0.1:8000 y la documentación en http://127.0.0.1:8000/docs.

---

## Interfaz de consola (CLI)

Permite crear, listar, buscar, actualizar y eliminar aprendices desde la terminal, sin usar Swagger.

```bash
pip install requests
python src/views/views.py
```

Por defecto consume la API desplegada en Render. Para usar la API local, cambia la variable `BASE_URL` al inicio del archivo:

```python
BASE_URL = "http://127.0.0.1:8000/trainee"
```

---

## Pruebas

```bash
pytest
```

---

## Despliegue en Render

1. Subir el código a GitHub.
2. Crear un **Web Service** en Render conectado al repositorio.
3. Configurar:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
4. En **Environment**, agregar las mismas variables del archivo `.env` (Render no lee ese archivo porque no se sube a GitHub).

### Problemas que se presentaron

- **`Error loading ASGI app. Could not import module "main"`**: ocurre cuando el comando de inicio no coincide con la ubicación de `main.py`. Como el archivo está dentro de `src/`, el comando correcto es `uvicorn src.main:app`.
- **Error 404 desde la CLI**: las rutas de la API están en singular (`/trainee`), no `/trainees`.
- **Error 422 al crear un aprendiz**: el correo tiene un formato inválido (por ejemplo, una `ñ` en lugar del punto: `algo@gmailñcom`).

---

## Autor

Proyecto desarrollado por **John David Diaz Ficha: 3494620** como práctica de desarrollo de APIs con FastAPI.