# Models

## Conexión con la DataBase
El modelo en Django usa diferentes opciones para conectarse con multiples DB relacionales, para la creación de tablas, Django usa la técnica de ORM (Object Relational Mapper), una abstracción del manejo de datos usando POO
##Crear el Modelo
Crea la class en el models.py que debe heredar de models.Models. Ejemplo:
```python
from django.db import models as m

class User(m.Model):
    """User Model"""
    
    # unique = True, el valor no puede repetirse
    email = m.EmailField(unique=True)  
    password = m.CharField(max_length=100)

    first_name = m.CharField(max_length=25)
    last_name = m.CharField(max_length=25)
    
    # Valor por defecto
    is_admin = m.BooleanField(default=False) 
    
    # Que pueda  estar vacia
    bio = m.TextField(blank=True) 
    
    # blank, permite valores vacios; null, permite valores nulos
    birthdate = m.DateField(blank=True, null=True)  

    # Que se agregue automaticamente al momento de crearse la instancia
    created = m.DateTimeField(auto_now_add=True)  
    modified = m.DateTimeField(auto_now=True)  # Guardar la fecha de la última vez que se editó

```

Guardar los cambios usando

```shell
$ python manage.py makemigrations
```

Y luego incluirlos o confirmarlos con 
```shell
$ python manage.py migrate
```

## Grabar Datos
Se puede hacer con el Shell de Django con el comandos
```shell
$ python manage.py shell
```
Y allí escribir el script con los datos, o escribiendo el script en un archivo aparte
```shell
>>> from posts.models import User
# objects es la interfaz que nos permite crear o traer datos
>>> edkar = User.objects.create(
...     email='chachati28@gmail.com',
...     password='1234567',
...     first_name='Edkar',
...     last_name='Chachati'
... )
# Ojo pelao con las comillas que sean simples o explota
>>>

```
Tambien puedes hacerlo por partes, como Jack el Destripador
````shell
>>>from posts.models import User
>>> peter = User() # Se crea el objeto
>>> peter.email = 'peterchiguire@chigui.com'
>>> peter.pk
>>> peter.password = 'super_chiguire123'
>>> peter.first_name='Peter'
>>> peter.last_name='chiguire'
>>> peter.bio="cutest Chiguire ever"
>>> peter.save() # Para guardar los cambios
````
Para eliminar uno de la DataBase
```shell
>>> peter.delete()
(1, {'posts.User': 1}) # Borró  un usuario de la aplicacion 'posts.User'
>>>
```

Ejemplo de Script para guardar varios usuarios 

```python
from datetime import date

users = [
    {
        'email': 'cvander@platzi.com',
        'first_name': 'Christian',
        'last_name': 'Van der Henst',
        'password': '1234567',
        'is_admin': True
    },
    {
        'email': 'freddier@platzi.com',
        'first_name': 'Freddy',
        'last_name': 'Vega',
        'password': '987654321'
    },
    {
        'email': 'yesica@platzi.com',
        'first_name': 'Yésica',
        'last_name': 'Cortés',
        'password': 'qwerty',
        'birthdate': date(1990, 12,19)
    },
    {
        'email': 'arturo@platzi.com',
        'first_name': 'Arturo',
        'last_name': 'Martínez',
        'password': 'msicomputer',
        'is_admin': True,
        'birthdate': date(1981, 11, 6),
        'bio': "Lorem ipsum dolor sit amet. Mucho texto"
    }
]

from posts.models import User

for user in users:
    obj = User(**user)
    obj.save()

# Puedes copypastearlo en la terminal
```
Buscar un objeto en la base de datos
```shell
# Get solo trae un elemento si hay mas de uno con la condicion suelta exception
>>> user = User.objects.get(email= 'cvander@platzi.com')
>>> user
<User: User object (3)>
>>> type(user)
<class 'posts.models.User'>
>>> user.first_name
'Christian'
```
Todos los objetos de una DataBase
```shell
>>> users = User.objects.all()

```
Obtener todos los objetos que cumplan una condicion de una base de datos.
Filtrar por condiciones
```shell
# Todos los usuarios cuyo email termine en '@platzi.com'
# Filter permite varios objetos en retorno
>>> all_users = User.objects.filter(email__endswith='@platzi.com')
>>> all_users
<QuerySet [<User: User object (3)>, <User: User object (4)>, <User: User object (5)>, <User: User object (6)>]>
```
Actualizar Datos de objetos en la Base de Datos
```shell
>>> platzi_users = User.objects.filter(email__endswith = '@platzi.com').update(is_admin = True)
```
Crear un SuperUsuario
```
python3 manage.py createsuperuser
```
Puedes usar los modelos que te traen las aplicaciones por defecto de Django
```shell
>>> from django.contrib.auth.models import User
>>> u = User.objects.create_user(username='edkar', password='admin123')
>>> u
<User: edkar>
>>> u.pk
1
>>> u.password
'pbkdf2_sha256$216000$SfT6wPZZPMKS$CX3ATQmFAgi1OsNANsWaYXnk5d4gDgkB7y1NlPL54iU='
>>>    
```
Como puedes ver, la contraseña se guarda encriptada, pero al momento de revisar la DB tienden a faltar muchos campos útiles y necesarios, asi que se para añadirlos se debe implementar usuarios personalizados
## Implementación de Usuarios personalizados
- ### Usando el Modelo Proxy
```python
from django.contrib.auth.models import User
from django.db import models as m


# Create your models here.
class Profile(m.Model):
    """Proxy model uses Abstract class User and added needed info"""
    # Crea un objeto en la clase User y con ese ID creamos otra tabla con los new fields si se elimina realiza efecto de SQL cascade
    user = m.OneToOneField(User, on_delete=m.CASCADE)  

    # new fields
    website = m.URLField(max_length=250, blank=True)
    biography = m.TextField(blank=True)
    phone_number = m.CharField(max_length=20, blank=True)
    profile_picture = m.ImageField(
        upload_to="users/pictures",
        blank=True, 
        null=True
    )
    created = m.DateTimeField(auto_now_add=True)
    modified = m.DateTimeField(auto_now=True)
```
- ### Extendiendo de la clase Abstracta de User existente
    ```CHECK DOCUMENTATION```