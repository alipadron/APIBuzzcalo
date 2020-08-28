# APIBuzzcalo

![python3](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=for-the-badge&logo=appveyor )

![postgres](https://img.shields.io/badge/DBMS-Postgres-blue?style=for-the-badge&logo=appveyor)

## Descripción de la aplicación:

API, útil para mostrar el reporte minimalista del 
contenido dentro de la base de dato que mantiene un extractor de datos (no especificado en este repositorio) externo a este proyecto, diponible bajo
licencias de *buzzcalo.com*.

### Lista de Dependencias:

    python-dotenv==0.14.0
    psycopg2-binary==2.8.5
    psycopg2==2.8.5
    Flask>=1.1.1
    flask_cors>=3.0.8
    
### Herramientas necesarias:

- Instalar herramientas:
  - postgres
  - python3
  - pip

### Pasos para la instalación:

    # Clonar el repositorio
    $: git clone xxx.git
    
    # Cambiar al directorio del proyecto
    $: cd APIBuzzcalo

    # Crear un archivo para las variables de entorno, con el nombre '.env'
    $: nano .env

    # Usar el siguiente formato
    # Variables de entorno

      # -- Inicio --
      # Postgres
      pg_host=localhost
      pg_database=db_name
      pg_user=jhon
      pg_password=1234

      # Flask
      SECRET_KEY=xx
      # -- Fin --

    # Instalar dependencias
    $: pip3 install -r requeriments.txt

    # Ejecutar el punto de entrada
    $: python3 app.py

    # Ir a la dirección local del host (localhost), y usar el puerto 8000
    # y probar el endpoint '/buzzcalo'

    # Requisitos para probar el endpoint 'wget', también puedes probarlo
    # dirigiéndoto el siguiente enlace:

    enlace: http://127.0.0.1:8000/

    $: wget http://127.0.0.1:8000/info
    # Si la repuesta es un mensaje de similar a este:

      {
        "info"    : "API para el servicio de extracción de buzzcalo.com", 
        "status"  : "0K",
        "version" : "v1"
      }

### Vistas disponibles:
- dominio.com/

### Endpoints disponibles:
- [GET, POST] dominio.com/info
- [GET]       dominio.com/buzzcalo


#### **DISCLAIMER**: Este proyecto está bajo el dominio de *buzzcalo.com*, y por tanto él reserva el derecho de usabilidad (este repositorio se moverá de lugar en caso de ser necesario).
