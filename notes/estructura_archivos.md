# Estructura del proyecto Django

## Archivos generados

## __init__.py 
Indica que la carpeta creada es un módulo de python.

## settings.py 
Define todas las configuraciones del proyecto

- ##### BASE_DIR
  Define la ubicación del proyecto
- ##### SECRET_KEY
  Es para el hashing de las contraseñas y sesiones en la DB
- ##### DEBUG
  Define si el proyecto sigue en desarrollo (False para enviar a produccion)
- ##### ALLOWED_HOSTS
  Host permitidos a interactuar con el proyecto
- ##### INSTALLED_APPS
  Todas las apps ligadas al proyecto
- ##### MIDDLEWARE
  Similar a INSTALLED_APPS
- ##### ROOT_URLCONF
  Nuestro módulo de entrada de url (ubicación principal del url)
- ##### TEMPLATES 
  El Template System es una manera de mostrar los datos usando HTML, incluye un poco de logica de programación que permite más flexibilidad en la UI
- ##### WSGI_APPLICATION
    Ubicacion del principal deployment
- ##### DATABASES 
  configuracion y conexion a DB
- ##### AUTH_PASSWORD_VALIDATORS 
  Validar contraseñas, si se usa la app de autenticación, que la contraseña pase por las validaciones predefinidas:
  - Valores de contraseña no similares a los valores de usuario
  - Que tenga la minima longitud
  - Validar la contraseña con un diccionario de contraseñas comunes
  - que la contraseña no sea numérica
- ##### LANGUAGE_CODE 
  Lenguaje en que se interactua la app
- ##### TIME_ZONE 
  Sistema horario en que corre la app
- ##### USE_I18N
  Libreria de traducción
- ##### USE_L10N
  Libreria de traducción
- ##### USE_TZ 
  libreria de zona horaria
- ##### STATIC_URL
  Define la ubicación de archivos estáticos como css, js, img

## urls.py
Define el punto de entrada para todas las peticiones que lleguen
## wsgi.py
Se usa para el deployment a produccion
## manage.py 
Es uno que no debes tocar y permite ejecutar todos los comandos (como django-admin)
- ##### startapp 
  para crear una nueva app en nuestro módulo de Django
  ```shell
  $ python manage.py startapp nombreapp 
  ```
  Trata de que los nombres siempre sean en plural

- ##### migrate
  para aplicar cambios a una db
  ```shell
  $ python manage.py migrate
  ```
- ##### makemigrations
  para añadir y  modificar modelos en la DB y reflejarlo en un archivo
  ```shell
  $ python manage.py makemigrations
  ```
- ##### runserver
  para poner a correr el servidor
  ```shell
  $ python manage.py runserver
  ```
  